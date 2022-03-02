## Back-end del módulo de indicadores para UMMEG

# linux/MacOS
export FLASK_ENV=development
python3 manage.py runserver -h 0.0.0.0 -p 5000

# Windows PowerShell
$env:FLASK_ENV = "development"
python3 manage.py runserver -h 0.0.0.0 -p 5000