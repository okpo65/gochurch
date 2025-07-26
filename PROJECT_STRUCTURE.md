# GoChurch Community Server - Project Structure

## 📁 **Organized Directory Structure**

```
gochurch/
├── 📄 Core Application Files
│   ├── main.py                    # FastAPI application entry point
│   ├── database.py                # Database configuration and models
│   ├── start.sh                   # Server startup script
│   ├── .env                       # Environment variables (not in git)
│   ├── .env.example               # Environment template
│   ├── .gitignore                 # Git ignore rules
│   ├── .python-version            # Python version for pyenv
│   ├── pyproject.toml             # Poetry dependencies
│   ├── poetry.lock                # Poetry lock file
│   └── README.md                  # Main project documentation
│
├── 🏗️ app/                        # Main application modules
│   ├── user/                      # User management
│   │   ├── models.py              # User and Profile models
│   │   ├── schemas.py             # Pydantic schemas
│   │   ├── service.py             # Business logic
│   │   └── router.py              # API endpoints
│   ├── church/                    # Church management
│   ├── community/                 # Boards, posts, comments
│   ├── verification/              # Identity verification
│   └── action/                    # Action logging
│
├── ⚙️ config/                     # Configuration files
│   ├── config.py                  # Application configuration
│   ├── alembic.ini                # Database migration config
│   └── alembic/                   # Database migrations
│       ├── versions/              # Migration files
│       ├── env.py                 # Alembic environment
│       └── script.py.mako         # Migration template
│
├── 🔄 workers/                    # Background task processing
│   ├── celery_app.py              # Celery configuration
│   ├── tasks.py                   # Celery tasks
│   └── tasks/                     # Task modules
│       └── sample_data.py         # Sample data generation
│
├── 🧪 tests/                      # Test suite
│   ├── conftest.py                # Test configuration
│   ├── test_users.py              # User API tests
│   ├── test_churches.py           # Church API tests
│   ├── test_community.py          # Community API tests
│   ├── test_verification_actions.py # Verification tests
│   └── test_sample_data.py        # Sample data tests
│
├── 🛠️ scripts/                   # Utility scripts
│   ├── setup_db.py                # Database setup
│   ├── setup_environment.sh       # Environment setup
│   ├── migrate_to_uuid_schema.py  # UUID migration
│   ├── setup_uuid_alternative.py  # Alternative UUID setup
│   ├── migrate_to_modular.py       # Legacy migration
│   ├── run_tests.py               # Test runner (isolated DB)
│   ├── run_dev_tests.py           # Development test runner
│   └── test_api_manually.py       # Manual API testing
│
├── 📚 docs/                       # Documentation
│   ├── README_NEW.md              # Updated README
│   ├── README_UUID_SCHEMA.md      # UUID schema guide
│   ├── SWAGGER_DOCS.md            # API documentation guide
│   ├── TESTING_GUIDE.md           # Testing instructions
│   └── TROUBLESHOOTING.md         # Common issues & solutions
│
└── 🚀 ops/                        # Deployment & operations
    ├── docker-compose.yml         # Production Docker setup
    ├── docker-compose.dev.yml     # Development Docker setup
    ├── Dockerfile                 # Production Docker image
    ├── Dockerfile.dev             # Development Docker image
    ├── deploy.sh                  # Production deployment
    ├── dev.sh                     # Development deployment
    ├── .env.docker                # Docker environment template
    └── README.md                  # Docker deployment guide
```

## 🎯 **Key Files & Their Purpose**

### **Core Application**
- **`main.py`** - FastAPI app with all routes and Swagger documentation
- **`database.py`** - SQLAlchemy models and database connection
- **`start.sh`** - One-command server startup (Celery + FastAPI)

### **Application Modules (`app/`)**
- **Modular structure** - Each feature has its own folder
- **Consistent pattern** - models.py, schemas.py, service.py, router.py
- **UUID-based** - All models use PostgreSQL UUIDs

### **Configuration (`config/`)**
- **`config.py`** - Centralized settings management
- **`alembic/`** - Database migration system
- **Environment-based** - Different configs for dev/prod

### **Background Workers (`workers/`)**
- **`celery_app.py`** - Celery configuration for async tasks
- **`tasks.py`** - Task definitions (sample data, cleanup)
- **`tasks/sample_data.py`** - Comprehensive sample data generation

### **Testing (`tests/`)**
- **Comprehensive coverage** - 120+ test functions
- **Isolated testing** - Uses separate test database
- **API testing** - Tests all endpoints with realistic data

### **Scripts (`scripts/`)**
- **Setup scripts** - Database and environment setup
- **Migration scripts** - UUID schema migration
- **Test runners** - Different testing approaches
- **Manual testing** - API endpoint validation

### **Documentation (`docs/`)**
- **Multiple guides** - Setup, testing, troubleshooting
- **API documentation** - Swagger and usage guides
- **Schema documentation** - Database structure explanation

## 🚀 **Quick Start Commands**

### **Development Setup**
```bash
# 1. Install dependencies
poetry install

# 2. Setup database
python scripts/setup_db.py

# 3. Generate sample data
python scripts/run_dev_tests.py

# 4. Start server
./start.sh
```

### **Testing**
```bash
# Unit tests (isolated DB)
python scripts/run_tests.py

# Manual API testing
python scripts/test_api_manually.py
```

### **Documentation**
```bash
# View API docs
open http://localhost:8000/docs

# Read guides
open docs/TESTING_GUIDE.md
open docs/SWAGGER_DOCS.md
```

## 📋 **File Organization Benefits**

### **✅ Clear Separation**
- **Core files** in root for easy access
- **Feature modules** grouped logically
- **Utilities** separated from application code
- **Documentation** centralized

### **✅ Easy Navigation**
- **Consistent naming** across modules
- **Logical grouping** by functionality
- **Clear file purposes** with descriptive names

### **✅ Scalability**
- **Modular structure** allows easy feature addition
- **Separated concerns** make maintenance easier
- **Configuration centralized** for environment management

### **✅ Development Workflow**
- **Scripts** for common tasks
- **Tests** organized by feature
- **Documentation** for all aspects
- **Docker** for deployment

## 🔧 **Import Path Updates**
