"""
Скрипт для запуска gRPC сервера
"""
import sys
import os

# Добавляем корневую директорию проекта в путь
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from app.src.server_main import serve

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    serve()
