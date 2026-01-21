"""
Скрипт для запуска gRPC сервера
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.src.server_main import serve

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    serve()
