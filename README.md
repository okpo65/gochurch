# GoChurch Community Server

A comprehensive church community platform built with FastAPI, featuring UUID-based architecture, identity verification, and comprehensive action logging.

## 🚀 **Quick Start**

```bash
# 1. Install dependencies
poetry install

# 2. Setup environment
cp .env.example .env
# Edit .env with your database credentials

# 3. Setup database and generate sample data
python scripts/run_dev_tests.py

# 4. Start the server
./start.sh

# 5. Visit API documentation
open http://localhost:8000/docs
```

## 📁 **Project Structure**

```
gochurch/
├── main.py                    # FastAPI application
├── database.py                # Database configuration
├── start.sh                   # Server startup script
├── app/                       # Application modules
│   ├── user/                  # User management
│   ├── church/                # Church directory
│   ├── community/             # Boards & posts
│   ├── verification/          # Identity verification
│   └── action/                # Action logging
├── config/                    # Configuration files
├── workers/                   # Background tasks (Celery)
├── tests/                     # Test suite
├── scripts/                   # Utility scripts
├── docs/                      # Documentation
└── ops/                       # Docker deployment
```

## 🏗️ **Key Features**

### **UUID-Based Architecture**
- All primary keys use PostgreSQL UUIDs
- Enhanced security and scalability
- Proper foreign key relationships

### **Church Management**
- Church directory with contact information
- User profiles linked to churches
- Identity verification system

### **Community Platform**
- Discussion boards for organized conversations
- Rich post content with engagement tracking
- Nested comment system
- Post tagging and categorization

### **Identity Verification**
- Photo-based verification requests
- Admin review workflow
- Church-specific verification

### **Action Logging**
- Comprehensive user interaction tracking
- Support for: view, like, bookmark, report
- Toggle-based actions (like/unlike)
- Action count aggregation

## 📊 **Database Schema**

Based on PostgreSQL with UUID extension:
- **users** - Basic user information with admin/blocked flags
- **profiles** - Extended user profiles with church association
- **churches** - Church directory
- **boards** - Discussion boards
- **posts** - User posts with engagement metrics
- **comments** - Nested comment system
- **identity_verifications** - Photo-based verification
- **action_logs** - User interaction tracking

## 🧪 **Testing**

### **Automated Tests**
```bash
# Run all tests (isolated test database)
python scripts/run_tests.py

# Run specific test suites
pytest tests/test_users.py -v
pytest tests/test_community.py -v
```

### **Manual API Testing**
```bash
# Generate sample data in main database
python scripts/run_dev_tests.py

# Test all endpoints manually
python scripts/test_api_manually.py

# Or use Swagger UI
open http://localhost:8000/docs
```

## 📋 **API Endpoints**

### **Users & Profiles**
- `POST /users/` - Create user
- `GET /users/` - List users
- `POST /users/profiles/` - Create profile
- `GET /users/{user_id}/profile` - Get user profile

### **Churches**
- `POST /churches/` - Create church
- `GET /churches/` - List churches
- `GET /churches/{church_id}` - Get church details

### **Community**
- `POST /boards/` - Create discussion board
- `GET /boards/{board_id}/posts` - Get posts in board
- `POST /boards/{board_id}/posts` - Create post
- `POST /boards/posts/{post_id}/comments` - Add comment

### **Identity Verification**
- `POST /verifications/` - Submit verification
- `GET /verifications/pending` - Get pending verifications
- `PUT /verifications/{id}/status` - Update verification status

### **Action Logs**
- `POST /actions/toggle` - Toggle action (like/unlike)
- `GET /actions/user/{user_id}` - Get user actions
- `GET /actions/count/{target_type}/{target_id}/{action_type}` - Get action count

## 🔧 **Development**

### **Environment Setup**
```bash
# Install Python 3.11
pyenv install 3.11.0
pyenv local 3.11.0

# Install dependencies
poetry install

# Setup database
python scripts/setup_db.py
```

### **Database Migration**
```bash
# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head
```

### **Sample Data**
```bash
# Generate via API
curl -X POST "http://localhost:8000/generate-sample-data"

# Generate directly
python -c "from workers.tasks.sample_data import generate_all_sample_data; generate_all_sample_data()"

# Cleanup
curl -X POST "http://localhost:8000/cleanup-data"
```

## 🐳 **Docker Deployment**

```bash
# Development
cd ops && ./dev.sh

# Production
cd ops && ./deploy.sh
```

## 📚 **Documentation**

- **[Project Structure](PROJECT_STRUCTURE.md)** - Detailed file organization
- **[API Documentation](docs/SWAGGER_DOCS.md)** - Swagger and API usage
- **[Testing Guide](docs/TESTING_GUIDE.md)** - Comprehensive testing instructions
- **[UUID Schema Guide](docs/README_UUID_SCHEMA.md)** - Database schema details
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and solutions

## 🛠️ **Technology Stack**

- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Database with UUID support
- **SQLAlchemy** - ORM with Alembic migrations
- **Celery** - Background task processing
- **Redis** - Message broker and caching
- **Pydantic** - Data validation and serialization
- **pytest** - Testing framework
- **Docker** - Containerization

## 🔐 **Security Features**

- UUID primary keys prevent enumeration attacks
- Input validation with Pydantic schemas
- SQL injection protection with SQLAlchemy ORM
- Proper foreign key constraints
- Environment-based configuration

## 🎯 **Getting Help**

1. **Check documentation** in `docs/` folder
2. **Run tests** to validate setup
3. **Use Swagger UI** for API exploration
4. **Check troubleshooting guide** for common issues

## 📄 **License**

MIT License - see LICENSE file for details.

---

**GoChurch Community Server** - Building stronger church communities through technology.
