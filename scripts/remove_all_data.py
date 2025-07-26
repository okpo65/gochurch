#!/usr/bin/env python3
"""
Script to remove all data from database tables
This script will delete all records from all tables while preserving the table structure
"""

import sys
import os
from pathlib import Path
from sqlalchemy import create_engine, text, MetaData, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from database import SessionLocal, engine
from app.models import (
    User, Profile, Church, Board, Post, PostTag, Comment,
    IdentityVerification, ActionLog
)

def get_table_dependencies():
    """
    Define the order in which tables should be cleared to respect foreign key constraints.
    Tables with foreign keys should be cleared before their referenced tables.
    """
    return [
        # Tables with foreign keys (clear first)
        'action_logs',
        'identity_verifications', 
        'comments',
        'post_tags',
        'posts',
        'profiles',
        
        # Tables with no dependencies or only self-references (clear last)
        'boards',
        'users',
        'churches',
        
        # System tables (if any)
        'task_results'
    ]

def truncate_all_tables(db_session, confirm=True):
    """
    Truncate all tables in the correct order to avoid foreign key constraint violations
    
    Args:
        db_session: Database session
        confirm: Whether to ask for confirmation before proceeding
    """
    
    if confirm:
        print("⚠️  WARNING: This will delete ALL data from ALL tables!")
        print("This action cannot be undone.")
        response = input("\nAre you sure you want to continue? (yes/no): ").lower().strip()
        
        if response not in ['yes', 'y']:
            print("❌ Operation cancelled.")
            return False
    
    print("\n🗑️  Starting data removal process...")
    
    # Get list of tables in dependency order
    tables_to_clear = get_table_dependencies()
    
    try:
        # Disable foreign key checks temporarily (PostgreSQL)
        print("🔓 Temporarily disabling foreign key constraints...")
        db_session.execute(text("SET session_replication_role = replica;"))
        
        cleared_count = 0
        total_records_deleted = 0
        
        for table_name in tables_to_clear:
            try:
                # Check if table exists
                inspector = inspect(engine)
                if table_name not in inspector.get_table_names():
                    print(f"⏭️  Skipping {table_name} (table doesn't exist)")
                    continue
                
                # Get count before deletion
                count_result = db_session.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                record_count = count_result.scalar()
                
                if record_count > 0:
                    # Truncate the table (faster than DELETE for large tables)
                    db_session.execute(text(f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE"))
                    print(f"✅ Cleared {table_name}: {record_count} records deleted")
                    total_records_deleted += record_count
                else:
                    print(f"⏭️  {table_name}: already empty")
                
                cleared_count += 1
                
            except SQLAlchemyError as e:
                print(f"⚠️  Warning: Could not clear {table_name}: {str(e)}")
                continue
        
        # Re-enable foreign key checks
        print("🔒 Re-enabling foreign key constraints...")
        db_session.execute(text("SET session_replication_role = DEFAULT;"))
        
        # Commit all changes
        db_session.commit()
        
        print(f"\n🎉 Data removal completed successfully!")
        print(f"📊 Summary:")
        print(f"   - Tables processed: {cleared_count}")
        print(f"   - Total records deleted: {total_records_deleted}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during data removal: {str(e)}")
        db_session.rollback()
        
        # Make sure to re-enable foreign key checks even if there's an error
        try:
            db_session.execute(text("SET session_replication_role = DEFAULT;"))
            db_session.commit()
        except:
            pass
            
        return False

def delete_all_records(db_session, confirm=True):
    """
    Alternative method: Delete all records using ORM models
    This is slower but more controlled than TRUNCATE
    
    Args:
        db_session: Database session
        confirm: Whether to ask for confirmation before proceeding
    """
    
    if confirm:
        print("⚠️  WARNING: This will delete ALL data from ALL tables!")
        print("This action cannot be undone.")
        response = input("\nAre you sure you want to continue? (yes/no): ").lower().strip()
        
        if response not in ['yes', 'y']:
            print("❌ Operation cancelled.")
            return False
    
    print("\n🗑️  Starting data removal process using ORM...")
    
    # Define models in dependency order (foreign key dependencies first)
    models_to_clear = [
        (ActionLog, "action_logs"),
        (IdentityVerification, "identity_verifications"),
        (Comment, "comments"),
        (PostTag, "post_tags"),
        (Post, "posts"),
        (Profile, "profiles"),
        (Board, "boards"),
        (User, "users"),
        (Church, "churches"),
    ]
    
    try:
        total_records_deleted = 0
        
        for model_class, table_name in models_to_clear:
            # Count records before deletion
            record_count = db_session.query(model_class).count()
            
            if record_count > 0:
                # Delete all records
                deleted = db_session.query(model_class).delete()
                print(f"✅ Cleared {table_name}: {deleted} records deleted")
                total_records_deleted += deleted
            else:
                print(f"⏭️  {table_name}: already empty")
        
        # Commit all changes
        db_session.commit()
        
        print(f"\n🎉 Data removal completed successfully!")
        print(f"📊 Total records deleted: {total_records_deleted}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during data removal: {str(e)}")
        db_session.rollback()
        return False

def verify_tables_empty(db_session):
    """
    Verify that all tables are empty after cleanup
    
    Args:
        db_session: Database session
    """
    print("\n🔍 Verifying tables are empty...")
    
    tables_to_check = [
        ('users', User),
        ('churches', Church),
        ('profiles', Profile),
        ('boards', Board),
        ('posts', Post),
        ('post_tags', PostTag),
        ('comments', Comment),
        ('identity_verifications', IdentityVerification),
        ('action_logs', ActionLog),
    ]
    
    all_empty = True
    
    for table_name, model_class in tables_to_check:
        try:
            count = db_session.query(model_class).count()
            if count == 0:
                print(f"✅ {table_name}: empty")
            else:
                print(f"❌ {table_name}: still has {count} records")
                all_empty = False
        except Exception as e:
            print(f"⚠️  Could not check {table_name}: {str(e)}")
    
    if all_empty:
        print("\n🎉 All tables are empty!")
    else:
        print("\n⚠️  Some tables still contain data.")
    
    return all_empty

def main():
    """Main function to handle command line arguments and execute cleanup"""
    
    print("🗑️  GoChurch Database Cleanup Tool")
    print("=" * 50)
    
    # Parse command line arguments
    force_mode = '--force' in sys.argv or '-f' in sys.argv
    use_orm = '--orm' in sys.argv
    verify_only = '--verify' in sys.argv
    
    if '--help' in sys.argv or '-h' in sys.argv:
        print("""
Usage: python scripts/remove_all_data.py [OPTIONS]

Options:
  --force, -f     Skip confirmation prompt
  --orm          Use ORM delete instead of TRUNCATE (slower but safer)
  --verify       Only verify if tables are empty, don't delete anything
  --help, -h     Show this help message

Examples:
  python scripts/remove_all_data.py                    # Interactive mode
  python scripts/remove_all_data.py --force            # Skip confirmation
  python scripts/remove_all_data.py --orm --force      # Use ORM with no confirmation
  python scripts/remove_all_data.py --verify           # Just check if tables are empty
        """)
        return True
    
    # Create database session
    db_session = SessionLocal()
    
    try:
        if verify_only:
            # Just verify tables are empty
            verify_tables_empty(db_session)
            return True
        
        # Choose cleanup method
        if use_orm:
            print("🔧 Using ORM-based deletion (slower but safer)")
            success = delete_all_records(db_session, confirm=not force_mode)
        else:
            print("🔧 Using TRUNCATE-based deletion (faster)")
            success = truncate_all_tables(db_session, confirm=not force_mode)
        
        if success:
            # Verify cleanup was successful
            verify_tables_empty(db_session)
            
            print("\n💡 Next steps:")
            print("   - Generate new sample data: python scripts/generate_sample_data.py")
            print("   - Or run development tests: python scripts/run_dev_tests.py")
            print("   - Or start fresh with the API: ./start.sh")
        
        return success
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation interrupted by user.")
        return False
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        db_session.close()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
