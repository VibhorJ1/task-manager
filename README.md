# Task Manager Backend

A Django REST API backend for managing tasks, with AI-powered task description generation. This project provides endpoints for creating, updating, listing, and managing tasks, as well as generating smart descriptions using OpenAI.

---

## Features
- Task CRUD (Create, Read, Update, Delete)
- Task status and priority filtering
- Mark tasks as complete
- AI-powered task description generator
- Django admin panel
- Dockerized for easy deployment

---

## Project Structure
```
task-manager/
  backend/
    manage.py
    requirements.txt
    Dockerfile
    task_engine/      # Django project settings
    tasks/            # Main app for task management
```

---

## Getting Started

### Prerequisites
- Python 3.8+
- pip
- Docker (optional, for containerized setup)

### Environment Variables
Create a `.env` file in `backend/` with the following (see `settings.py`):
```
SECRET_KEY='django-insecure-kglvsi*c7=_gic^$-#z2pct*12t57g(gbbh9bmnoequp$x!6sz'
DEBUG=True
ALLOWED_HOSTS=*
OPENAI_API_KEY=your-openai-key
```

---

### Local Development
1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd task-manager/backend
   ```
2. **(Optional) Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```
5. **Run the development server:**
   ```bash
   python manage.py runserver
   ```
6. **Access:**
   - API: [http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/)
   - Admin: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

### Running with Docker
1. **Build the Docker image:**
   ```bash
   cd backend
   docker build -t task-manager-backend .
   ```
2. **Run the container:**
   ```bash
   docker run --env-file .env -p 8000:8000 task-manager-backend
   ```
3. **Access:**
   - API: [http://localhost:8000/api/](http://localhost:8000/api/)
   - Admin: [http://localhost:8000/admin/](http://localhost:8000/admin/)

---

## API Endpoints

All endpoints are prefixed with `/api/`.

### Task Endpoints
| Method | Endpoint                        | Description                                 |
|--------|----------------------------------|---------------------------------------------|
| GET    | /api/tasks/                     | List all tasks (supports filtering)         |
| POST   | /api/tasks/                     | Create a new task                           |
| GET    | /api/tasks/{id}/                | Retrieve a specific task                    |
| PUT    | /api/tasks/{id}/                | Update a task                               |
| PATCH  | /api/tasks/{id}/                | Partially update a task                     |
| DELETE | /api/tasks/{id}/                | Delete a task                               |
| GET    | /api/tasks/status/              | Get tasks grouped by status                 |
| POST   | /api/tasks/{id}/complete/       | Mark a task as completed                    |

#### Filtering
- `GET /api/tasks/?status=completed|upcoming|missed` — Filter by status
- `GET /api/tasks/?priority=low|medium|high|urgent` — Filter by priority

### AI Description Endpoint

**Feature:** Smart Task Description Generator  
**Why:** Writing clear task descriptions helps users break down goals and plan better. However, users often type only short task names. This AI tool converts task titles into rich descriptions automatically.
**Model Used:** OpenAI GPT-3.5-turbo via Chat API

| Method | Endpoint                                 | Description                                 |
|--------|------------------------------------------|---------------------------------------------|
| POST   | /api/tasks/ai/generate-description/      | Generate a task description using OpenAI     |

**Request Body:**
```json
{
  "title": "Your task title"
}
```
**Response:**
```json
{
  "description": "AI-generated description."
}
```

### Admin Panel
- `/admin/` — Django admin interface

---

## Task Model Fields
| Field               | Type         | Description                        |
|---------------------|--------------|------------------------------------|
| id                  | integer      | Unique identifier                  |
| title               | string       | Task title                         |
| description         | string       | Task description                   |
| deadline            | datetime     | Deadline for the task              |
| is_completed        | boolean      | Completion status                  |
| completed_at        | datetime     | When the task was completed        |
| created_at          | datetime     | When the task was created          |
| updated_at          | datetime     | When the task was last updated     |
| priority            | string       | Priority: low, medium, high, urgent|
| status              | string       | Read-only: upcoming, completed, missed |
| time_until_deadline | string       | Read-only: time delta              |
| days_until_deadline | integer      | Read-only: days until deadline     |
| hours_until_deadline| float        | Read-only: hours until deadline    |

---

## Contributing
1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## License
Specify your license here (e.g., MIT, Apache 2.0, etc.)

---

## Notes
- Do **not** commit `db.sqlite3`, `venv/`, or sensitive files. See `.gitignore`.
- For production, use a robust database and configure environment variables securely.
- The AI description endpoint requires a valid OpenAI API key.
