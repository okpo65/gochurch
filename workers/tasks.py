import time
from workers.celery_app import celery_app


@celery_app.task
def add_numbers(a: int, b: int):
    """Simple task to add two numbers with a delay"""
    time.sleep(2)  # Simulate some work
    result = a + b
    return {"result": result, "message": f"{a} + {b} = {result}"}


@celery_app.task
def process_data(data: str):
    """Simple task to process data with a delay"""
    time.sleep(3)  # Simulate some work
    processed = data.upper()
    return {"original": data, "processed": processed, "length": len(data)}


@celery_app.task
def generate_sample_data():
    """Generate sample data for the database"""
    try:
        from workers.tasks.sample_data import generate_all_sample_data
        result = generate_all_sample_data()
        return {
            "status": "success",
            "message": "Sample data generated successfully",
            "data": result
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to generate sample data: {str(e)}"
        }


@celery_app.task
def cleanup_old_data():
    """Clean up old test data (useful for development)"""
    try:
        from sqlalchemy.orm import sessionmaker
        from database import engine
        from sqlalchemy import text
        
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Delete all data in reverse dependency order
        tables = [
            "action_logs",
            "post_tags", 
            "comments",
            "posts",
            "boards",
            "identity_verifications",
            "profiles",
            "users",
            "churches"
        ]
        
        deleted_counts = {}
        for table in tables:
            result = db.execute(text(f"DELETE FROM {table}"))
            deleted_counts[table] = result.rowcount
        
        db.commit()
        db.close()
        
        return {
            "status": "success",
            "message": "Old data cleaned up successfully",
            "deleted": deleted_counts
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to cleanup data: {str(e)}"
        }
