from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from sqlalchemy.orm import Session
from workers.celery_app import celery_app
from database import get_db, create_tables, TaskResult
from config.config import settings
import json

# Import routers
from app.user.router import router as user_router
from app.community.router import router as community_router
from app.church.router import router as church_router
from app.verification.router import router as verification_router
from app.action.router import router as action_router

# Create tables on startup
create_tables()

# Custom OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="GoChurch Community Server API",
        version="2.0.0",
        description="""
## GoChurch Community Server

A comprehensive church community platform built with FastAPI, featuring:

### 🏛️ **Core Features**
- **Integer-based Architecture** - Enhanced performance with integer primary keys
- **Church Management** - Directory of churches with contact information
- **Identity Verification** - Photo-based verification system with admin review
- **Discussion Boards** - Organized discussion boards for community engagement
- **Post & Comment System** - Rich content sharing with nested comments
- **Action Logging** - Track user interactions (views, likes, bookmarks, reports)

### 🔐 **Security**
- Integer primary keys with auto-increment
- Proper foreign key constraints with CASCADE deletes
- Input validation with Pydantic schemas
- SQL injection protection with SQLAlchemy ORM
- CORS middleware for cross-origin requests

### 📊 **Database Schema**
Based on PostgreSQL with integer primary keys, featuring:
- Users with admin/blocked status
- User profiles linked to churches
- Identity verification workflow
- Hierarchical board/post/comment structure
- Comprehensive action logging

### 🚀 **Getting Started**
1. Create a user: `POST /users/`
2. Create a profile: `POST /users/profiles/`
3. Create a church: `POST /churches/`
4. Create a board: `POST /boards/`
5. Start posting: `POST /boards/{board_id}/posts`

### 📝 **API Usage**
All endpoints use integer identifiers. Example ID: `1`

For detailed examples and usage patterns, see the individual endpoint documentation below.
        """,
        routes=app.routes,
        tags=[
            {
                "name": "users",
                "description": "User management operations. Handle user creation, updates, and profile management."
            },
            {
                "name": "churches", 
                "description": "Church directory management. Maintain church information and contact details."
            },
            {
                "name": "boards",
                "description": "Discussion board operations. Create and manage community discussion boards, posts, and comments."
            },
            {
                "name": "identity-verification",
                "description": "Identity verification system. Handle photo-based verification requests and admin reviews."
            },
            {
                "name": "action-logs",
                "description": "User action tracking. Log and manage user interactions like views, likes, bookmarks, and reports."
            },
            {
                "name": "development",
                "description": "Development and testing endpoints for sample data generation and cleanup."
            },
            {
                "name": "legacy",
                "description": "Legacy Celery task endpoints for backward compatibility."
            }
        ]
    )
    
    # Add custom info
    openapi_schema["info"]["contact"] = {
        "name": "GoChurch Development Team",
        "email": "dev@gochurch.com"
    }
    
    openapi_schema["info"]["license"] = {
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    }
    
    # Add servers
    openapi_schema["servers"] = [
        {
            "url": "http://localhost:8000",
            "description": "Development server"
        },
        {
            "url": "http://3.39.195.204:8000",
            "description": "Production server"
        }
    ]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app = FastAPI(
    title="GoChurch Community Server API", 
    version="2.0.0",
    debug=settings.DEBUG,
    description="A church community platform with boards, posts, and identity verification",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set custom OpenAPI schema
app.openapi = custom_openapi

# Include routers
app.include_router(user_router)
app.include_router(community_router)
app.include_router(church_router)
app.include_router(verification_router)
app.include_router(action_router)


@app.get("/", 
         summary="API Information",
         description="Get basic information about the GoChurch Community Server API",
         response_description="API information and available endpoints",
         tags=["root"])
def read_root():
    return {
        "message": "GoChurch Community Server is running!",
        "version": "2.0.0",
        "environment": settings.ENVIRONMENT,
        "cors_enabled": True,
        "documentation": {
            "swagger_ui": "/docs",
            "redoc": "/redoc",
            "openapi_json": "/openapi.json"
        },
        "endpoints": {
            "users": {
                "path": "/users",
                "description": "User management and profiles"
            },
            "churches": {
                "path": "/churches", 
                "description": "Church directory management"
            },
            "boards": {
                "path": "/boards",
                "description": "Discussion boards, posts, and comments"
            },
            "verifications": {
                "path": "/verifications",
                "description": "Identity verification system"
            },
            "actions": {
                "path": "/actions",
                "description": "User action logging (likes, views, etc.)"
            }
        },
        "features": [
            "Integer-based primary keys for enhanced performance",
            "Church management and directory",
            "Identity verification with photo upload",
            "Hierarchical board and post system",
            "Comprehensive action logging",
            "User profiles with church association",
            "Nested comment threads",
            "Post tagging system",
            "CORS enabled for cross-origin requests"
        ],
        "database": {
            "type": "PostgreSQL",
            "primary_keys": "Integer (auto-increment)"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
