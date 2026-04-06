@echo off
echo Starting Agentic Mobile CS API, Streamlit UI, and Redis ...

:: 0. Start Redis (Requirement for performance logging)
:: If you have Redis installed via WSL or separate executable, ensure it's in your PATH.
echo [INFO] Attempting to start Redis server...
start "Redis Server" cmd /c "redis-server"

:: Start FastAPI Backend (Takes ~30 seconds to load)
echo [INFO] FastAPI Server will take ~30 seconds to start.
start "FastAPI Server" cmd /K "set PYTHONPATH=. && .venv\Scripts\python.exe -m uvicorn entrypoint.main:app --host 0.0.0.0 --port 8000 --reload"

echo [INFO] Please wait until "Application startup complete" appears.

:: Start Streamlit UI
start "Streamlit UI" cmd /K "set PYTHONPATH=. && .venv\Scripts\python.exe -m streamlit run frontend/app.py"

echo All services are started in separate windows!
