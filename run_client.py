"""
Скрипт для запуска gRPC клиента
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.src.client_main import run

if __name__ == "__main__":
    import sys
    address = sys.argv[1] if len(sys.argv) > 1 else "localhost:50051"
    run(address)
