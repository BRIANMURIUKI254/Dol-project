# File Storage System

A comprehensive file storage system for Django with support for both local storage and Cloudinary integration.

## Features

- **Dual Storage Strategy**: Images and videos are stored on Cloudinary, documents are stored locally
- **File Validation**: Size limits, type checking, and security validation
- **Metadata Tracking**: Complete file information including uploader, timestamps, and access control
- **RESTful API**: Full CRUD operations with proper authentication and permissions
- **Admin Interface**: Django admin integration with file previews and management
- **Security**: Private file access control and signed URLs for sensitive content

## Installation

1. Add the app to your `INSTALLED_APPS` in `settings.py`:
```python
INSTALLED_APPS = [
    # ... other apps
    'apps.file_storage',
]
```

2. Configure Cloudinary in your `settings.py`:
```python
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
    'SECURE': True,
}
```

3. Run migrations:
```bash
python manage.py makemigrations file_storage
python manage.py migrate
```

## API Endpoints

### Upload File
**POST** `/api/files/upload/`

Upload a new file to the system.

**Headers:**
```
Authorization: Bearer <your_jwt_token>
Content-Type: multipart/form-data
```

**Form Data:**
- `file`: The file to upload (required)
- `description`: Optional description (optional)
- `is_public`: Whether file should be public (default: true)

**Example cURL:**
```bash
curl -X POST "http://localhost:8000/api/files/upload/" \
  -H "Authorization: Bearer your_jwt_token" \
  -F "file=@/path/to/your/file.jpg" \
  -F "description=Profile picture" \
  -F "is_public=true"
```

**Response:**
```json
{
  "success": true,
  "message": "File uploaded successfully",
  "file_data": {
    "file_id": 1,
    "file_name": "profile.jpg",
    "file_reference": "550e8400-e29b-41d4-a716-446655440000",
    "mime_type": "image/jpeg",
    "storage_location": "cloudinary",
    "file_url": "https://res.cloudinary.com/your-cloud/image/upload/v1234567890/profile.jpg",
    "file_size": 245760,
    "uploaded_at": "2024-01-15T10:30:00Z",
    "uploaded_by": 1,
    "uploaded_by_username": "john_doe",
    "is_public": true,
    "description": "Profile picture",
    "file_extension": ".jpg",
    "is_image": true,
    "is_video": false,
    "is_document": false,
    "absolute_url": "/api/files/550e8400-e29b-41d4-a716-446655440000/",
    "download_url": "/api/files/550e8400-e29b-41d4-a716-446655440000/serve/"
  },
  "file_reference": "550e8400-e29b-41d4-a716-446655440000",
  "file_url": "https://res.cloudinary.com/your-cloud/image/upload/v1234567890/profile.jpg"
}
```

### Get File Information
**GET** `/api/files/{file_reference}/`

Retrieve file metadata by file reference.

**Example cURL:**
```bash
curl -X GET "http://localhost:8000/api/files/550e8400-e29b-41d4-a716-446655440000/" \
  -H "Authorization: Bearer your_jwt_token"
```

**Response:**
```json
{
  "success": true,
  "file_data": {
    "file_id": 1,
    "file_name": "profile.jpg",
    "file_reference": "550e8400-e29b-41d4-a716-446655440000",
    "mime_type": "image/jpeg",
    "storage_location": "cloudinary",
    "file_url": "https://res.cloudinary.com/your-cloud/image/upload/v1234567890/profile.jpg",
    "file_size": 245760,
    "uploaded_at": "2024-01-15T10:30:00Z",
    "uploaded_by": 1,
    "uploaded_by_username": "john_doe",
    "is_public": true,
    "description": "Profile picture",
    "file_extension": ".jpg",
    "is_image": true,
    "is_video": false,
    "is_document": false,
    "absolute_url": "/api/files/550e8400-e29b-41d4-a716-446655440000/",
    "download_url": "/api/files/550e8400-e29b-41d4-a716-446655440000/serve/"
  }
}
```

### Serve File
**GET** `/api/files/{file_reference}/serve/`

Serve the actual file content. For Cloudinary files, this redirects to the Cloudinary URL. For local files, it serves the file content directly.

**Example cURL:**
```bash
curl -X GET "http://localhost:8000/api/files/550e8400-e29b-41d4-a716-446655440000/serve/" \
  -H "Authorization: Bearer your_jwt_token"
```

### List User Files
**GET** `/api/files/files/`

List all files uploaded by the authenticated user.

**Query Parameters:**
- `storage_location`: Filter by storage location (`local` or `cloudinary`)
- `mime_type`: Filter by MIME type (e.g., `image/`, `video/`, `application/pdf`)
- `is_public`: Filter by public status (`true` or `false`)

**Example cURL:**
```bash
curl -X GET "http://localhost:8000/api/files/files/?storage_location=cloudinary&mime_type=image/" \
  -H "Authorization: Bearer your_jwt_token"
```

**Response:**
```json
{
  "success": true,
  "files": [
    {
      "file_id": 1,
      "file_name": "profile.jpg",
      "file_reference": "550e8400-e29b-41d4-a716-446655440000",
      "mime_type": "image/jpeg",
      "storage_location": "cloudinary",
      "file_size": 245760,
      "uploaded_at": "2024-01-15T10:30:00Z",
      "uploaded_by_username": "john_doe",
      "is_public": true
    }
  ],
  "count": 1
}
```

### Delete File
**DELETE** `/api/files/{file_reference}/delete/`

Delete a file and its database record. Only the file owner or admin can delete files.

**Example cURL:**
```bash
curl -X DELETE "http://localhost:8000/api/files/550e8400-e29b-41d4-a716-446655440000/delete/" \
  -H "Authorization: Bearer your_jwt_token"
```

**Response:**
```json
{
  "success": true,
  "message": "File deleted successfully"
}
```

### File Statistics
**GET** `/api/files/stats/`

Get file storage statistics.

**Example cURL:**
```bash
curl -X GET "http://localhost:8000/api/files/stats/"
```

**Response:**
```json
{
  "success": true,
  "stats": {
    "total_files": 150,
    "by_storage": {
      "local": 75,
      "cloudinary": 75
    },
    "by_type": {
      "images": 60,
      "videos": 15,
      "documents": 75
    },
    "total_size": 1048576000
  }
}
```

## File Types and Storage Strategy

### Cloudinary Storage (Images & Videos)
- **Images**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.webp`, `.svg`
- **Videos**: `.mp4`, `.avi`, `.mov`, `.wmv`, `.flv`, `.webm`, `.mkv`

### Local Storage (Documents & Archives)
- **Documents**: `.pdf`, `.doc`, `.docx`, `.xls`, `.xlsx`, `.ppt`, `.pptx`, `.txt`
- **Archives**: `.zip`, `.rar`, `.7z`, `.tar`, `.gz`

## Security Features

1. **File Type Validation**: Only allowed file types can be uploaded
2. **Size Limits**: Maximum file size of 50MB
3. **Access Control**: Private files require authentication
4. **Owner Permissions**: Only file owners or admins can delete files
5. **Secure URLs**: Cloudinary URLs use HTTPS

## Error Handling

All API endpoints return consistent error responses:

```json
{
  "success": false,
  "message": "Error description",
  "errors": ["Detailed error message"]
}
```

Common HTTP status codes:
- `200`: Success
- `201`: Created (file upload)
- `400`: Bad Request (validation errors)
- `401`: Unauthorized (authentication required)
- `403`: Forbidden (permission denied)
- `404`: Not Found (file not found)
- `500`: Internal Server Error

## Django Admin Integration

The file storage system includes a comprehensive Django admin interface:

- View all uploaded files with metadata
- Filter by storage location, file type, and uploader
- Preview images and videos directly in the admin
- Manage file permissions and descriptions
- Delete files with proper cleanup

Access the admin at `/admin/` and look for the "File Storage" section.

## Database Model

The `StoredFile` model includes:

- `file_id`: Auto-incrementing primary key
- `file_name`: Original filename
- `file_reference`: UUID for lookups
- `mime_type`: File MIME type
- `storage_location`: Where file is stored (`local` or `cloudinary`)
- `file_url`: Full URL or path to file
- `file_size`: File size in bytes
- `uploaded_at`: Upload timestamp
- `uploaded_by`: User who uploaded the file
- `is_public`: Public access flag
- `description`: Optional file description

## Backup and Maintenance

### SQLite Database Backup
```bash
# Create backup
cp db.sqlite3 db_backup_$(date +%Y%m%d_%H%M%S).sqlite3

# Restore backup
cp db_backup_20240115_103000.sqlite3 db.sqlite3
```

### Cloudinary Backup
Cloudinary automatically handles backups, but you can export metadata:

```python
# Export file metadata
from apps.file_storage.models import StoredFile
import json

files = StoredFile.objects.filter(storage_location='cloudinary')
metadata = []
for file in files:
    metadata.append({
        'file_reference': str(file.file_reference),
        'file_name': file.file_name,
        'file_url': file.file_url,
        'uploaded_at': file.uploaded_at.isoformat(),
    })

with open('cloudinary_metadata.json', 'w') as f:
    json.dump(metadata, f, indent=2)
```

## Performance Considerations

1. **File Size Limits**: 50MB maximum to prevent server overload
2. **Database Indexing**: Proper indexes on frequently queried fields
3. **CDN Usage**: Cloudinary provides global CDN for fast file delivery
4. **Local Storage**: Files organized by year/month for efficient management
5. **Caching**: Consider implementing Redis caching for frequently accessed files

## Troubleshooting

### Common Issues

1. **Cloudinary Upload Fails**
   - Check API credentials in environment variables
   - Verify Cloudinary account limits
   - Check file size and type restrictions

2. **Local File Not Found**
   - Ensure MEDIA_ROOT is properly configured
   - Check file permissions
   - Verify file path in database

3. **Permission Denied**
   - Verify user authentication
   - Check file ownership
   - Ensure proper JWT token

### Debug Mode

Enable debug logging in `settings.py`:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'file_storage.log',
        },
    },
    'loggers': {
        'apps.file_storage': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```
