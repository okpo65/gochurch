from fastapi import FastAPI, Depends
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
- **UUID-based Architecture** - Enhanced security with UUID primary keys
- **Church Management** - Directory of churches with contact information
- **Identity Verification** - Photo-based verification system with admin review
- **Discussion Boards** - Organized discussion boards for community engagement
- **Post & Comment System** - Rich content sharing with nested comments
- **Action Logging** - Track user interactions (views, likes, bookmarks, reports)

### 🔐 **Security**
- UUID primary keys prevent enumeration attacks
- Proper foreign key constraints with CASCADE deletes
- Input validation with Pydantic schemas
- SQL injection protection with SQLAlchemy ORM

### 📊 **Database Schema**
Based on PostgreSQL with UUID extension, featuring:
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
All endpoints use UUID identifiers. Example UUID: `550e8400-e29b-41d4-a716-446655440000`

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
            "url": "https://api.gochurch.com",
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
            "UUID-based primary keys for enhanced security",
            "Church management and directory",
            "Identity verification with photo upload",
            "Hierarchical board and post system",
            "Comprehensive action logging",
            "User profiles with church association",
            "Nested comment threads",
            "Post tagging system"
        ],
        "database": {
            "type": "PostgreSQL",
            "uuid_extension": "uuid-ossp",
            "primary_keys": "UUID v4"
        }
    }


@app.post("/add")
def add_task(a: int, b: int, db: Session = Depends(get_db)):
    """Add two numbers using Celery task"""
    task = add_numbers.delay(a, b)
    
    # Save task info to database
    db_task = TaskResult(
        task_id=task.id,
        task_type="add_numbers",
        status="PENDING"
    )
    db.add(db_task)
    db.commit()
    
    return {"task_id": task.id, "status": "Task submitted"}


@app.post("/process")
def process_task(data: str, db: Session = Depends(get_db)):
    """Process data using Celery task"""
    task = process_data.delay(data)
    
    # Save task info to database
    db_task = TaskResult(
        task_id=task.id,
        task_type="process_data",
        status="PENDING"
    )
    db.add(db_task)
    db.commit()
    
    return {"task_id": task.id, "status": "Task submitted"}


@app.get("/task/{task_id}")
def get_task_result(task_id: str, db: Session = Depends(get_db)):
    """Get task result by task ID"""
    task = celery_app.AsyncResult(task_id)
    
    # Update database record
    db_task = db.query(TaskResult).filter(TaskResult.task_id == task_id).first()
    
    if task.state == "PENDING":
        result = {"task_id": task_id, "status": "PENDING", "result": None}
    elif task.state == "SUCCESS":
        result = {"task_id": task_id, "status": "SUCCESS", "result": task.result}
        if db_task:
            db_task.status = "SUCCESS"
            db_task.result = json.dumps(task.result)
            db.commit()
    else:
        result = {"task_id": task_id, "status": task.state, "result": str(task.info)}
        if db_task:
            db_task.status = task.state
            db_task.result = str(task.info)
            db.commit()
    
    return result


@app.get("/tasks")
def get_all_tasks(db: Session = Depends(get_db)):
    """Get all tasks from database"""
    tasks = db.query(TaskResult).all()
    return {"tasks": tasks}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
# Development endpoints for sample data
@app.post("/generate-sample-data",
          summary="Generate sample data",
          description="Generate comprehensive sample data for testing and development purposes.",
          tags=["development"],
          response_description="Task submission confirmation")
def generate_sample_data_task(db: Session = Depends(get_db)):
    task = generate_sample_data.delay()
    
    # Save task to database
    db_task = TaskResult(
        task_id=task.id,
        task_type="generate_sample_data",
        status="PENDING",
        result=None
    )
    db.add(db_task)
    db.commit()
    
    return {"task_id": task.id, "status": "Sample data generation started", "message": "This will create churches, users, posts, and other sample data"}


@app.post("/cleanup-data",
          summary="Cleanup test data",
          description="Remove all test data from the database. Use with caution!",
          tags=["development"],
          response_description="Task submission confirmation")
def cleanup_data_task(db: Session = Depends(get_db)):
    task = cleanup_old_data.delay()
    
    # Save task to database
    db_task = TaskResult(
        task_id=task.id,
        task_type="cleanup_old_data",
        status="PENDING",
        result=None
    )
    db.add(db_task)
    db.commit()
    
    return {"task_id": task.id, "status": "Data cleanup started", "message": "This will remove all data from the database"}


# Legacy endpoints (keeping for backward compatibility)
@app.post("/add",
          summary="Add two numbers (Legacy)",
          description="Legacy Celery task endpoint for adding two numbers. Kept for backward compatibility.",
          tags=["legacy"],
          response_description="Task submission confirmation")
def add_task(a: int, b: int, db: Session = Depends(get_db)):
    task = add_numbers.delay(a, b)
    
    # Save task to database
    db_task = TaskResult(
        task_id=task.id,
        task_type="add_numbers",
        status="PENDING",
        result=None
    )
    db.add(db_task)
    db.commit()
    
    return {"task_id": task.id, "status": "Task submitted"}


@app.post("/process",
          summary="Process data (Legacy)",
          description="Legacy Celery task endpoint for processing text data. Kept for backward compatibility.",
          tags=["legacy"],
          response_description="Task submission confirmation")
def process_task(data: str, db: Session = Depends(get_db)):
    task = process_data.delay(data)
    
    # Save task to database
    db_task = TaskResult(
        task_id=task.id,
        task_type="process_data",
        status="PENDING",
        result=None
    )
    db.add(db_task)
    db.commit()
    
    return {"task_id": task.id, "status": "Task submitted"}


@app.get("/task/{task_id}",
         summary="Get task result (Legacy)",
         description="Get the result of a Celery task by its ID. Legacy endpoint for backward compatibility.",
         tags=["legacy"],
         response_description="Task status and result")
def get_task_result(task_id: str, db: Session = Depends(get_db)):
    # Get result from Celery
    result = celery_app.AsyncResult(task_id)
    
    # Update database record
    db_task = db.query(TaskResult).filter(TaskResult.task_id == task_id).first()
    
    if result.state == "PENDING":
        response = {"task_id": task_id, "status": "PENDING", "result": None}
    elif result.state == "SUCCESS":
        response = {"task_id": task_id, "status": "SUCCESS", "result": result.result}
        if db_task:
            db_task.status = "SUCCESS"
            db_task.result = json.dumps(result.result)
            db.commit()
    else:
        response = {"task_id": task_id, "status": result.state, "result": str(result.info)}
        if db_task:
            db_task.status = result.state
            db_task.result = str(result.info)
            db.commit()
    
    return response


@app.get("/tasks",
         summary="Get all tasks (Legacy)",
         description="Get all Celery tasks from the database. Legacy endpoint for backward compatibility.",
         tags=["legacy"],
         response_description="List of all tasks")
def get_all_tasks(db: Session = Depends(get_db)):
    tasks = db.query(TaskResult).all()
    return {"tasks": tasks}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
