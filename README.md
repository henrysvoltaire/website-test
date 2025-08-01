# Website Test – Flask To-Do App
A lightweight and fully functional to-do app built with Flask to learn web development in Python. This project demonstrates dynamic routing, form handling, and persistent local storage using JSON.

## Features
- Add and delete tasks
- Mark tasks as completed
- Archive completed tasks
- View and reset archive
- Persistent storage via local JSON file
- Full history/log view of actions
- Reset entire app state (hard reset)
- Dynamic UI rendering with Jinja2
- Styled UI and confirmation prompts

## Getting Started
Clone the repository and set up your environment:

```bash
git clone https://github.com/henrysvoltaire/website-test.git
cd website-test
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Usage
Once the server is running, open your browser and go to:  
(http://localhost:5000)

## File Overview
- `app.py` – Flask app with routing, logic, and data saving
- `templates/index.html` – Main HTML page rendered using Jinja2
- `data.json` – Stores tasks, archive, and task IDs (excluded from GitHub)
- `requirements.txt` – List of Python dependencies

## Notes
- `data.json` is excluded from version control (`.gitignore`) to avoid sharing personal task data.
- You can erase all stored data directly in the UI using the "Reset All Data" button.