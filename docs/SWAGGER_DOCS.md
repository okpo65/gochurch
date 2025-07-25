# GoChurch Community Server - Swagger Documentation

## 📚 API Documentation Access

The GoChurch Community Server provides comprehensive API documentation through multiple interfaces:

### **Swagger UI (Interactive)**
- **URL**: `http://localhost:8000/docs`
- **Features**: Interactive API testing, request/response examples, schema validation
- **Best for**: Testing endpoints, understanding request/response formats

### **ReDoc (Clean Documentation)**
- **URL**: `http://localhost:8000/redoc`
- **Features**: Clean, readable documentation with detailed descriptions
- **Best for**: Reading comprehensive API documentation

### **OpenAPI JSON Schema**
- **URL**: `http://localhost:8000/openapi.json`
- **Features**: Raw OpenAPI 3.0 specification
- **Best for**: Generating client SDKs, importing into other tools

## 🎯 Documentation Features

### **Comprehensive Endpoint Documentation**
Each endpoint includes:
- **Summary**: Brief description of what the endpoint does
- **Description**: Detailed explanation with usage notes
- **Parameters**: All path, query, and body parameters with types and examples
- **Request Examples**: Sample JSON payloads for POST/PUT requests
- **Response Examples**: Sample responses with all possible status codes
- **Error Responses**: Detailed error scenarios (404, 400, etc.)

### **Schema Documentation**
All data models include:
- **Field Descriptions**: Clear explanation of each field
- **Data Types**: Proper typing (UUID, string, integer, etc.)
- **Validation Rules**: Field length limits, required fields, etc.
- **Example Values**: Realistic sample data for testing

### **Interactive Testing**
The Swagger UI allows you to:
- **Try It Out**: Execute API calls directly from the documentation
- **Authentication**: Test protected endpoints (when auth is implemented)
- **Response Inspection**: View actual API responses
- **Schema Validation**: Automatic request validation

## 📋 API Structure Overview

### **Tags Organization**
The API is organized into logical groups:

#### **👥 Users**
- User account management
- Profile creation and updates
- User-church associations

#### **⛪ Churches**
- Church directory management
- Contact information maintenance
- Church-user relationships

#### **📋 Boards**
- Discussion board creation
- Post management within boards
- Comment threads and interactions
- Post tagging system

#### **🔍 Identity Verification**
- Photo-based verification requests
- Admin review workflow
- Status tracking and updates

#### **📊 Action Logs**
- User interaction tracking
- Like/bookmark/view logging
- Action count aggregation

## 🚀 Getting Started with the API

### **1. Start the Server**
```bash
./start.sh
```

### **2. Access Documentation**
Open your browser to:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### **3. Basic Workflow**
1. **Create a Church**: `POST /churches/`
2. **Create a User**: `POST /users/`
3. **Create a Profile**: `POST /users/profiles/`
4. **Create a Board**: `POST /boards/`
5. **Create a Post**: `POST /boards/{board_id}/posts`
6. **Add Comments**: `POST /boards/posts/{post_id}/comments`
7. **Track Actions**: `POST /actions/toggle`

## 💡 Example API Usage

### **Creating a Complete User**
```bash
# 1. Create a church
curl -X POST "http://localhost:8000/churches/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "First Baptist Church",
    "address": "123 Main St, Anytown, USA",
    "phone_number": "+1-555-0123"
  }'

# 2. Create a user
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "is_blocked": false,
    "is_admin": false
  }'

# 3. Create a profile
curl -X POST "http://localhost:8000/users/profiles/" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "nickname": "john_doe",
    "church_id": "550e8400-e29b-41d4-a716-446655440001"
  }'
```

### **Creating Discussion Content**
```bash
# 1. Create a board
curl -X POST "http://localhost:8000/boards/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "General Discussion",
    "description": "Community discussions and announcements"
  }'

# 2. Create a post
curl -X POST "http://localhost:8000/boards/550e8400-e29b-41d4-a716-446655440003/posts?author_id=550e8400-e29b-41d4-a716-446655440000" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Welcome!",
    "contents": "Welcome to our community board!"
  }'

# 3. Like the post
curl -X POST "http://localhost:8000/actions/toggle?user_id=550e8400-e29b-41d4-a716-446655440000&action_type=like&target_type=post&target_id=550e8400-e29b-41d4-a716-446655440004"
```

## 🔧 Advanced Features

### **UUID Handling**
- All IDs are UUIDs (e.g., `550e8400-e29b-41d4-a716-446655440000`)
- UUIDs are automatically generated by PostgreSQL
- Use proper UUID format in requests

### **Pagination**
Most list endpoints support pagination:
- `skip`: Number of items to skip
- `limit`: Maximum items to return (usually max 100)

### **Error Handling**
Standard HTTP status codes:
- `200`: Success
- `201`: Created
- `400`: Bad Request (validation errors)
- `404`: Not Found
- `422`: Unprocessable Entity (schema validation)

### **Response Formats**
All responses are JSON with consistent structure:
```json
{
  "id": "uuid",
  "field1": "value1",
  "field2": "value2",
  "created_at": "2024-01-15T10:30:00Z"
}
```

## 📖 Documentation Best Practices

### **For Developers**
1. **Read the Descriptions**: Each endpoint has detailed usage notes
2. **Check Examples**: Use provided examples as templates
3. **Validate Schemas**: Pay attention to required fields and data types
4. **Test Interactively**: Use Swagger UI to test before implementing

### **For API Consumers**
1. **Use Proper UUIDs**: Ensure UUID format is correct
2. **Handle Errors**: Implement proper error handling for all status codes
3. **Respect Limits**: Follow pagination limits and rate limits
4. **Validate Input**: Use the schema information to validate requests

## 🎨 Customization

The documentation is automatically generated from:
- **FastAPI decorators**: Endpoint descriptions and metadata
- **Pydantic schemas**: Request/response models with examples
- **Custom OpenAPI schema**: Enhanced with contact info, servers, and tags

To modify documentation:
1. Update endpoint decorators in router files
2. Enhance Pydantic schemas with Field descriptions
3. Modify the custom OpenAPI function in `main.py`

## 🚀 Production Considerations

### **Documentation Security**
- Consider disabling `/docs` and `/redoc` in production
- Keep `/openapi.json` for client generation
- Use environment variables to control documentation access

### **Performance**
- Documentation generation is cached
- No performance impact on API endpoints
- Consider CDN for static documentation assets

This comprehensive documentation system ensures that developers can easily understand, test, and integrate with the GoChurch Community Server API.
