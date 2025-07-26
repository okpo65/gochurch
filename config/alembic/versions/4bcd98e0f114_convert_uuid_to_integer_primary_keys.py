"""Convert UUID to Integer primary keys

Revision ID: 4bcd98e0f114
Revises: 281fb5104bfe
Create Date: 2025-07-26 21:14:10.204945

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '4bcd98e0f114'
down_revision = '281fb5104bfe'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Convert all UUID primary keys and foreign keys to Integer"""
    
    # Drop existing tables with UUID structure (if they exist)
    # This is a destructive operation - all data will be lost
    
    # Drop tables in reverse dependency order
    op.execute("DROP TABLE IF EXISTS action_logs CASCADE")
    op.execute("DROP TABLE IF EXISTS identity_verifications CASCADE")
    op.execute("DROP TABLE IF EXISTS comments CASCADE")
    op.execute("DROP TABLE IF EXISTS post_tags CASCADE")
    op.execute("DROP TABLE IF EXISTS posts CASCADE")
    op.execute("DROP TABLE IF EXISTS boards CASCADE")
    op.execute("DROP TABLE IF EXISTS profiles CASCADE")
    op.execute("DROP TABLE IF EXISTS users CASCADE")
    op.execute("DROP TABLE IF EXISTS churches CASCADE")
    
    # Create churches table with integer ID
    op.create_table('churches',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, index=True),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('address', sa.Text()),
        sa.Column('phone_number', sa.String(20))
    )
    
    # Create users table with integer ID
    op.create_table('users',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, index=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('is_blocked', sa.Boolean(), nullable=False, default=False),
        sa.Column('is_admin', sa.Boolean(), nullable=False, default=False)
    )
    
    # Create profiles table with integer IDs
    op.create_table('profiles',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, index=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('nickname', sa.String(100)),
        sa.Column('thumbnail', sa.Text()),
        sa.Column('church_id', sa.Integer(), sa.ForeignKey('churches.id'))
    )
    
    # Create boards table with integer ID
    op.create_table('boards',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, index=True),
        sa.Column('title', sa.Text(), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now())
    )
    
    # Create posts table with integer IDs
    op.create_table('posts',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, index=True),
        sa.Column('board_id', sa.Integer(), sa.ForeignKey('boards.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('author_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False, index=True),
        sa.Column('title', sa.Text(), nullable=False),
        sa.Column('contents', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True)),
        sa.Column('like_count', sa.Integer(), nullable=False, default=0),
        sa.Column('comment_count', sa.Integer(), nullable=False, default=0),
        sa.Column('view_count', sa.Integer(), nullable=False, default=0)
    )
    
    # Create post_tags table with integer foreign key
    op.create_table('post_tags',
        sa.Column('post_id', sa.Integer(), sa.ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('tag', sa.Text(), primary_key=True)
    )
    
    # Create comments table with integer IDs
    op.create_table('comments',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, index=True),
        sa.Column('post_id', sa.Integer(), sa.ForeignKey('posts.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('author_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False, index=True),
        sa.Column('contents', sa.Text(), nullable=False),
        sa.Column('parent_id', sa.Integer(), sa.ForeignKey('comments.id')),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now())
    )
    
    # Create identity_verifications table with integer IDs
    op.create_table('identity_verifications',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, index=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('photo_url', sa.Text(), nullable=False),
        sa.Column('church_id', sa.Integer(), sa.ForeignKey('churches.id')),
        sa.Column('status', sa.String(20), nullable=False),
        sa.Column('reviewed_by', sa.Integer(), sa.ForeignKey('users.id')),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('reviewed_at', sa.DateTime(timezone=True)),
        sa.CheckConstraint("status IN ('pending', 'approved', 'rejected')", name='check_status')
    )
    
    # Create action_logs table with integer IDs
    op.create_table('action_logs',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, index=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('action_type', sa.String(50), nullable=False),
        sa.Column('target_type', sa.String(50), nullable=False),
        sa.Column('target_id', sa.Integer(), nullable=False),
        sa.Column('is_on', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint("action_type IN ('view', 'like', 'bookmark', 'report')", name='check_action_type'),
        sa.CheckConstraint("target_type IN ('post', 'comment')", name='check_target_type')
    )
    
    # Create the target index for action_logs
    op.create_index('idx_action_logs_target', 'action_logs', ['target_type', 'target_id'])


def downgrade() -> None:
    """Revert back to UUID primary keys"""
    
    # Drop all integer-based tables
    op.execute("DROP TABLE IF EXISTS action_logs CASCADE")
    op.execute("DROP TABLE IF EXISTS identity_verifications CASCADE")
    op.execute("DROP TABLE IF EXISTS comments CASCADE")
    op.execute("DROP TABLE IF EXISTS post_tags CASCADE")
    op.execute("DROP TABLE IF EXISTS posts CASCADE")
    op.execute("DROP TABLE IF EXISTS boards CASCADE")
    op.execute("DROP TABLE IF EXISTS profiles CASCADE")
    op.execute("DROP TABLE IF EXISTS users CASCADE")
    op.execute("DROP TABLE IF EXISTS churches CASCADE")
    
    # Recreate with UUID columns (original structure)
    op.create_table('churches',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, index=True),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('address', sa.Text()),
        sa.Column('phone_number', sa.String(20))
    )
    
    op.create_table('users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, index=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('is_blocked', sa.Boolean(), nullable=False, default=False),
        sa.Column('is_admin', sa.Boolean(), nullable=False, default=False)
    )
    
    op.create_table('profiles',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, index=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('nickname', sa.String(100)),
        sa.Column('thumbnail', sa.Text()),
        sa.Column('church_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('churches.id'))
    )
    
    op.create_table('boards',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, index=True),
        sa.Column('title', sa.Text(), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now())
    )
    
    op.create_table('posts',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, index=True),
        sa.Column('board_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('boards.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('author_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False, index=True),
        sa.Column('title', sa.Text(), nullable=False),
        sa.Column('contents', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True)),
        sa.Column('like_count', sa.Integer(), nullable=False, default=0),
        sa.Column('comment_count', sa.Integer(), nullable=False, default=0),
        sa.Column('view_count', sa.Integer(), nullable=False, default=0)
    )
    
    op.create_table('post_tags',
        sa.Column('post_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('tag', sa.Text(), primary_key=True)
    )
    
    op.create_table('comments',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, index=True),
        sa.Column('post_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('posts.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('author_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False, index=True),
        sa.Column('contents', sa.Text(), nullable=False),
        sa.Column('parent_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('comments.id')),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now())
    )
    
    op.create_table('identity_verifications',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, index=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('photo_url', sa.Text(), nullable=False),
        sa.Column('church_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('churches.id')),
        sa.Column('status', sa.String(20), nullable=False),
        sa.Column('reviewed_by', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id')),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('reviewed_at', sa.DateTime(timezone=True)),
        sa.CheckConstraint("status IN ('pending', 'approved', 'rejected')", name='check_status')
    )
    
    op.create_table('action_logs',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, index=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('action_type', sa.String(50), nullable=False),
        sa.Column('target_type', sa.String(50), nullable=False),
        sa.Column('target_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('is_on', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint("action_type IN ('view', 'like', 'bookmark', 'report')", name='check_action_type'),
        sa.CheckConstraint("target_type IN ('post', 'comment')", name='check_target_type')
    )
    
    op.create_index('idx_action_logs_target', 'action_logs', ['target_type', 'target_id'])
