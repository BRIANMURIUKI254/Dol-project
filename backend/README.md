# Days of Light (D.O.L) Ministry - Backend

This is the backend API for the Days of Light (D.O.L) Ministry website, built with Django REST Framework.

## Features

- **User Authentication**: JWT-based authentication system
- **Ministry Information**: Manage ministry details, leadership, and mission
- **Houses**: Manage house meetings and locations
- **Events**: Create and manage ministry events
- **Sermons**: Upload and manage sermon media
- **Giving**: Handle donations and giving
- **API Documentation**: Auto-generated with drf-spectacular
- **Cloudinary Integration**: For media file storage

## Prerequisites

- Python 3.9+
- PostgreSQL (for production)
- Cloudinary account (for media storage)

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/dol-backend.git
   cd dol-backend
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Update the `.env` file with your configuration.

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## API Documentation

Once the server is running, access the API documentation at:
- Swagger UI: http://localhost:8000/api/docs/
- ReDoc: http://localhost:8000/api/redoc/

## Project Structure

```
dol_backend/
├── apps/
│   ├── accounts/         # User authentication and profiles
│   ├── core/             # Core functionality and base models
│   ├── events/           # Ministry events
│   ├── giving/           # Donations and giving
│   ├── houses/           # House meetings
│   ├── ministry/         # Ministry information
│   └── sermons/          # Sermon media
├── config/              # Project settings
├── static/              # Static files
├── media/               # Media files (user uploads)
├── .env                 # Environment variables
├── .gitignore
├── manage.py
├── README.md
└── requirements.txt
```

## Development

### Running Tests
```bash
python manage.py test
```

### Code Style
This project uses:
- Black for code formatting
- Flake8 for linting
- isort for import sorting

Run these tools before committing:
```bash
black .
isort .
flake8
```

## Deployment

### Production Setup
1. Set `DEBUG=False` in `.env`
2. Configure a production database (PostgreSQL)
3. Set up a production web server (e.g., Gunicorn with Nginx)
4. Set up SSL certificates (e.g., with Let's Encrypt)

### Environment Variables
See `.env.example` for all required environment variables.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
