# GoChurch Community Server

A modular FastAPI server for community management with user authentication, community features, and settings management.

## Project Structure

```
.
├── app/                     # Main application modules
│   ├── user/               # User management module
│   │   ├── __init__.py
│   │   ├── models.py       # User and UserProfile models
│   │   ├── schemas.py      # Pydantic schemas for validation
│   │   ├── service.py      # Business logic layer
│   │   └── router.py       # API endpoints
│   ├── community/          # Community management module
│   │   ├── __init__.py
│   │   ├── models.py       # Community, Post, Comment models
│   │   ├── schemas.py      # Pydantic schemas
│   │   ├── service.py      # Business logic layer
│   │   └── router.py       # API endpoints
│   ├── signin/             # Authentication module
│   │   ├── __init__.py
│   │   ├── schemas.py      # Auth-related schemas
│   │   ├── service.py      # JWT and auth logic
│   │   └── router.py       # Auth endpoints
│   └── settings/           # Settings management module
│       ├── __init__.py
│       ├── models.py       # Settings models
│       ├── schemas.py      # Settings schemas
│       ├── service.py      # Settings business logic
│       └── router.py       # Settings endpoints
├── ops/                    # Docker deployment configurations
├── alembic/               # Database migrations
├── main.py                # FastAPI application entry point
├── database.py            # Database configuration and models
├── config.py              # Configuration management
├── celery_app.py          # Celery configuration
├── tasks.py               # Celery tasks
└── pyproject.toml         # Poetry dependencies
```

## Features

### User Management (`/users`)
- User registration and profile management
- User profile with additional information
- User CRUD operations

### Authentication (`/auth`)
- JWT-based authentication
- Login/logout functionality
- Password change and reset
- Protected endpoints with bearer token

### Community Management (`/communities`)
- Create and manage communities
- Join communities
- Create posts within communities
- Comment on posts
- Voting system for posts and comments

### Settings (`/settings`)
- User-specific settings (privacy, notifications, display)
- System-wide settings (admin only)
- Notification preferences management

## API Endpoints

### Authentication
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout
- `POST /auth/change-password` - Change password
- `POST /auth/forgot-password` - Request password reset
- `POST /auth/reset-password` - Reset password with token
- `GET /auth/me` - Get current user info

### Users
- `POST /users/` - Create user
- `GET /users/` - List users
- `GET /users/{user_id}` - Get user by ID
- `PUT /users/{user_id}` - Update user
- `DELETE /users/{user_id}` - Delete user

### Communities
- `POST /communities/` - Create community
- `GET /communities/` - List communities
- `GET /communities/{community_id}` - Get community
- `PUT /communities/{community_id}` - Update community
- `POST /communities/{community_id}/join` - Join community
- `POST /communities/{community_id}/posts` - Create post
- `GET /communities/{community_id}/posts` - List posts
- `GET /communities/posts/{post_id}` - Get post
- `PUT /communities/posts/{post_id}` - Update post
- `POST /communities/posts/{post_id}/comments` - Create comment
- `GET /communities/posts/{post_id}/comments` - List comments

### Settings
- `GET /settings/user` - Get user settings
- `PUT /settings/user` - Update user settings
- `GET /settings/system` - Get system settings
- `POST /settings/system` - Create system setting (admin)
- `PUT /settings/system/{key}` - Update system setting (admin)
- `DELETE /settings/system/{key}` - Delete system setting (admin)
- `GET /settings/notifications` - Get notification settings
- `POST /settings/notifications` - Create notification setting
- `PUT /settings/notifications/{type}/{category}` - Update notification setting

## Database Models

### User Models
- `User` - Basic user information
- `UserProfile` - Extended user profile data

### Community Models
- `Community` - Community information
- `CommunityMember` - Community membership
- `Post` - Community posts
- `Comment` - Post comments
- `Vote` - Voting on posts/comments

### Settings Models
- `UserSettings` - User-specific settings
- `SystemSettings` - System-wide configuration
- `NotificationSettings` - Notification preferences

## Setup and Installation

### 1. Install Dependencies
```bash
poetry install
```

### 2. Environment Configuration
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 3. Database Setup
```bash
# Create database
python setup_db.py

# Run migrations
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### 4. Run the Application
```bash
# Start all services
./start.sh

# Or manually:
poetry shell
celery -A celery_app worker --loglevel=info &
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Authentication Flow

1. **Register**: Create user via `POST /users/`
2. **Login**: Authenticate via `POST /auth/login` to get JWT token
3. **Access Protected Routes**: Include `Authorization: Bearer <token>` header
4. **Token Validation**: Server validates JWT on each protected request

## Example Usage

### Register a User
```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword",
    "full_name": "John Doe"
  }'
```

### Login
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepassword"
  }'
```

### Create a Community (with auth token)
```bash
curl -X POST "http://localhost:8000/communities/?creator_id=1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tech Discussions",
    "description": "A place to discuss technology",
    "category": "technology"
  }'
```

## Security Features

- Password hashing with bcrypt
- JWT token-based authentication
- Protected routes with dependency injection
- Input validation with Pydantic
- SQL injection protection with SQLAlchemy ORM

## Development

### Adding New Modules
1. Create new directory under `app/`
2. Add `__init__.py`, `models.py`, `schemas.py`, `service.py`, `router.py`
3. Import models in `database.py`
4. Include router in `main.py`
5. Run migration: `alembic revision --autogenerate -m "Add new module"`

### Testing
```bash
# Run tests (when implemented)
pytest

# Check API documentation
# Visit http://localhost:8000/docs
```

## Docker Deployment

See `ops/README.md` for Docker deployment instructions.

## Contributing

1. Follow the modular structure
2. Use proper separation of concerns (models, schemas, services, routers)
3. Add proper error handling
4. Include input validation
5. Write tests for new features
6. Update documentation
