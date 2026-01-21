"""
Скрипт для запуска REST сервера (FastAPI)
"""
import sys
import os
import uvicorn

# Добавляем корневую директорию проекта в путь
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

if __name__ == "__main__":
    uvicorn.run(
        "app.src.rest_server:app",
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
