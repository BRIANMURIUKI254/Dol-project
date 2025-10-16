# Days of Light (DOL) Church Platform

A comprehensive platform for Days of Light (DOL) Church, featuring a modern frontend and a robust backend API.

## Project Structure

- `backend/` - Django REST Framework backend API
- `frontend/` - React-based frontend application

## Features

### Backend (Django REST Framework)
- JWT Authentication
- Role-based access control
- Houses management
- Events management
- Sermons and playlists
- File uploads with Cloudinary
- Comprehensive API documentation

### Frontend (React)
- Modern, responsive UI
- User authentication flows
- Interactive dashboard
- Event management
- Media library
- Admin panel

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 16+
- PostgreSQL
- Cloudinary account (for file uploads)

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on `.env.example` and update with your configuration.

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser_custom --email admin@dol.org --username admin
   ```

7. (Optional) Load sample data:
   ```bash
   python manage.py seed_data
   ```

8. Start the development server:
   ```bash
   python manage.py runserver
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env` file based on `.env.example` and update with your configuration.

4. Start the development server:
   ```bash
   npm start
   ```

## Development

### Backend
- Run tests: `python manage.py test`
- Generate migrations: `python manage.py makemigrations`
- Apply migrations: `python manage.py migrate`
- Create superuser: `python manage.py createsuperuser_custom`

### Frontend
- Start dev server: `npm start`
- Run tests: `npm test`
- Build for production: `npm run build`

## Deployment

### Backend
For production deployment, it's recommended to use:
- Gunicorn or uWSGI as the application server
- Nginx as the reverse proxy
- PostgreSQL as the database
- Environment variables for configuration

Example Gunicorn command:
```bash
gunicorn --bind 0.0.0.0:8000 core.wsgi:application
```

### Frontend
Build the frontend for production:
```bash
npm run build
```

Then serve the static files using a web server like Nginx or a CDN.

## API Documentation

Once the backend server is running, you can access the API documentation at:
- Swagger UI: http://localhost:8000/api/docs/swagger/
- ReDoc: http://localhost:8000/api/docs/redoc/

## License

This project is licensed under the MIT License - see the [LICENSE](backend/LICENSE) file for details.
