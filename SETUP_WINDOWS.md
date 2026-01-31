# STOPPS ITS (Starter) — Windows Setup

## Recommended versions
- Python **3.11.x** (avoid Python 3.13 for now)
- pip latest
- Virtual environment per project

## Setup
```powershell
cd stoppsDjangoApp-main
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

If you use CMD instead of PowerShell:
```bat
venv\Scripts\activate
```
