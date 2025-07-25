# GoChurch Community Server - UUID Schema

A church community platform built with FastAPI, featuring UUID-based primary keys, identity verification, and comprehensive action logging.

## 🏗️ Database Schema

Based on the PostgreSQL schema with UUID primary keys and proper foreign key relationships:

### Core Tables
- **users** - Basic user information with admin/blocked flags
- **profiles** - Extended user profiles with church association
- **churches** - Church directory with contact information
- **identity_verifications** - Photo-based identity verification system
- **boards** - Discussion boards/categories
- **posts** - User posts within boards
- **post_tags** - Tagging system for posts
- **comments** - Nested comments on posts
- **action_logs** - User actions (views, likes, bookmarks, reports)

## 🚀 Key Features

### UUID-Based Architecture
- All primary keys use PostgreSQL UUID with `uuid_generate_v4()`
- Proper foreign key relationships with CASCADE deletes
- Enhanced security and scalability

### Church Management
- Church directory with contact information
- User profiles linked to churches
- Identity verification tied to church membership

### Identity Verification System
- Photo-based verification requests
- Admin review workflow (pending → approved/rejected)
- Church-specific verification

### Board & Post System
- Hierarchical discussion boards
- Rich post content with view/like/comment tracking
- Tagging system for post categorization
- Nested comment threads

### Action Logging
- Comprehensive user action tracking
- Support for: view, like, bookmark, report
- Toggle-based actions (like/unlike)
- Action count aggregation

## 📋 API Endpoints

### Users & Profiles
```
POST   /users/                    # Create user
GET    /users/                    # List users
GET    /users/{user_id}           # Get user
PUT    /users/{user_id}           # Update user
DELETE /users/{user_id}           # Delete user

POST   /users/profiles/           # Create profile
GET    /users/profiles/{profile_id}  # Get profile
GET    /users/{user_id}/profile   # Get user's profile
PUT    /users/profiles/{profile_id}  # Update profile
DELETE /users/profiles/{profile_id}  # Delete profile
```

### Churches
```
POST   /churches/                 # Create church
GET    /churches/                 # List churches
GET    /churches/{church_id}      # Get church
PUT    /churches/{church_id}      # Update church
DELETE /churches/{church_id}      # Delete church
```

### Boards & Posts
```
POST   /boards/                   # Create board
GET    /boards/                   # List boards
GET    /boards/{board_id}         # Get board
PUT    /boards/{board_id}         # Update board
DELETE /boards/{board_id}         # Delete board

POST   /boards/{board_id}/posts   # Create post
GET    /boards/{board_id}/posts   # List posts in board
GET    /boards/posts/{post_id}    # Get post (increments view count)
PUT    /boards/posts/{post_id}    # Update post

POST   /boards/posts/{post_id}/comments    # Create comment
GET    /boards/posts/{post_id}/comments    # List comments
GET    /boards/comments/{comment_id}       # Get comment
PUT    /boards/comments/{comment_id}       # Update comment

POST   /boards/posts/{post_id}/tags       # Add tag
GET    /boards/posts/{post_id}/tags       # Get tags
DELETE /boards/posts/{post_id}/tags/{tag} # Remove tag
```

### Identity Verification
```
POST   /verifications/            # Submit verification
GET    /verifications/pending     # Get pending verifications
GET    /verifications/status/{status}  # Get by status
GET    /verifications/user/{user_id}   # Get user verifications
GET    /verifications/{verification_id}  # Get verification
PUT    /verifications/{verification_id}/status  # Update status
```

### Action Logs
```
POST   /actions/                  # Create action log
POST   /actions/toggle            # Toggle action (like/unlike)
GET    /actions/user/{user_id}    # Get user actions
GET    /actions/target/{target_type}/{target_id}  # Get target actions
GET    /actions/count/{target_type}/{target_id}/{action_type}  # Get count
GET    /actions/{action_log_id}   # Get action log
```

## 🔧 Setup & Installation

### 1. Install Dependencies
```bash
poetry install
```

### 2. Environment Setup
```bash
cp .env.example .env
# Edit .env with your PostgreSQL configuration
```

### 3. Database Migration
```bash
# Run the UUID schema migration
python migrate_to_uuid_schema.py
```

### 4. Start the Server
```bash
./start.sh
```

## 📊 Database Schema Details

### Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    is_blocked BOOLEAN NOT NULL DEFAULT FALSE,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE
);
```

### Profiles Table
```sql
CREATE TABLE profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    nickname VARCHAR(100),
    thumbnail TEXT,
    church_id UUID REFERENCES churches(id)
);
```

### Action Logs Table
```sql
CREATE TABLE action_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    action_type VARCHAR(50) NOT NULL CHECK (
        action_type IN ('view', 'like', 'bookmark', 'report')
    ),
    target_type VARCHAR(50) NOT NULL CHECK (
        target_type IN ('post', 'comment')
    ),
    target_id UUID NOT NULL,
    is_on BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
```

## 🎯 Usage Examples

### Create a User and Profile
```bash
# Create user
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{"is_blocked": false, "is_admin": false}'

# Create profile for user
curl -X POST "http://localhost:8000/users/profiles/" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "nickname": "john_doe",
    "church_id": "550e8400-e29b-41d4-a716-446655440001"
  }'
```

### Create a Board and Post
```bash
# Create board
curl -X POST "http://localhost:8000/boards/" \
  -H "Content-Type: application/json" \
  -d '{"title": "General Discussion", "description": "General church discussions"}'

# Create post
curl -X POST "http://localhost:8000/boards/{board_id}/posts?author_id={user_id}" \
  -H "Content-Type: application/json" \
  -d '{"title": "Welcome!", "contents": "Welcome to our community board!"}'
```

### Like a Post
```bash
curl -X POST "http://localhost:8000/actions/toggle" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "action_type": "like",
    "target_type": "post", 
    "target_id": "550e8400-e29b-41d4-a716-446655440002"
  }'
```

## 🔐 Security Features

- UUID primary keys prevent enumeration attacks
- Proper foreign key constraints with CASCADE deletes
- Input validation with Pydantic schemas
- SQL injection protection with SQLAlchemy ORM
- Check constraints for enum-like fields

## 🏛️ Architecture

### Modular Structure
```
app/
├── user/          # User and profile management
├── church/        # Church directory
├── community/     # Boards, posts, comments
├── verification/  # Identity verification
└── action/        # Action logging system
```

### Service Layer Pattern
Each module follows the same pattern:
- `models.py` - SQLAlchemy models
- `schemas.py` - Pydantic validation schemas  
- `service.py` - Business logic layer
- `router.py` - FastAPI route handlers

## 🚀 Development

### Adding New Features
1. Create models in appropriate module
2. Add Pydantic schemas for validation
3. Implement business logic in service layer
4. Create API endpoints in router
5. Update database imports in `database.py`
6. Include router in `main.py`

### Testing
```bash
# Start server
./start.sh

# Visit API documentation
open http://localhost:8000/docs
```

## 📈 Performance Considerations

- Indexed foreign key columns
- Optimized queries with proper joins
- UUID generation at database level
- Efficient action log aggregation
- Proper pagination support

This architecture provides a solid foundation for a church community platform with room for future expansion and excellent performance characteristics.
