# Task Manager Backend

This is a Django-based backend for a Task Manager application. It provides APIs for managing tasks and integrates with an AI module for advanced features.

## Features
- Task management (CRUD)
- Django REST Framework APIs
- SQLite database (default)
- Modular app structure

## Project Structure
```
task-manager/
  backend/
    manage.py
    requirements.txt
    task_engine/      # Django project settings
    tasks/            # Main app for task management
```

## Getting Started

### Prerequisites
- Python 3.8+
- pip

### Setup
1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd task-manager/backend
   ```
2. (Optional) Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Apply migrations:
   ```bash
   python manage.py migrate
   ```
5. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Usage
- Access the API at `http://127.0.0.1:8000/`
- Admin panel: `http://127.0.0.1:8000/admin/`

## Development
- Main app code is in `backend/tasks/`
- Add new features in separate Django apps as needed.

## Contributing
1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

## License
Specify your license here (e.g., MIT, Apache 2.0, etc.)

## Notes
- Ensure you do **not** commit `db.sqlite3` or `venv/` to version control. Add them to `.gitignore` if not already present.
- For production, use a more robust database and configure environment variables for sensitive settings.
