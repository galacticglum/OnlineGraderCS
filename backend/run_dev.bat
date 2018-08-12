@echo off

IF NOT EXIST "venv" (
    echo "Creating virtual environment and installing dependancies"
    virtualenv venv
    call venv/Scripts/activate.bat
    pip install -r requirements.txt
) ELSE (
    call venv/Scripts/activate.bat
)

set FLASK_APP=application.py
set FLASK_DEBUG=1
flask run --debugger --reload
