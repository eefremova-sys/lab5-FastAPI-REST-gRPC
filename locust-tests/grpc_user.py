"""
Locust тесты для gRPC API глоссария
"""
import grpc
import sys
import os
import random
import string
import time
from locust import User, task, between, events

# Добавляем путь к сгенерированным proto файлам
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    from app.generated import glossary_pb2 as pb
    from app.generated import glossary_pb2_grpc as pb_grpc
except ImportError:
    # Альтернативный путь импорта
    root_dir = os.path.join(os.path.dirname(__file__), '..')
    root_dir = os.path.abspath(root_dir)
    if root_dir not in sys.path:
        sys.path.insert(0, root_dir)
    from app.generated import glossary_pb2 as pb
    from app.generated import glossary_pb2_grpc as pb_grpc

# Существующие термины для тестирования
EXISTING_TERMS = ['usability_test', 'heuristic_evaluation', 'a_b_testing']

def generate_random_entry():
    """
    Генерирует случайную запись для тестирования операций создания
    """
    random_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return {
        "name": f"term_{random_id}",
        "description": f"Test description for term_{random_id}",
        "reference": f"https://example.com/{random_id}"
    }

def generate_random_keyword():
    """
    Генерирует случайный ключ для нового термина
    """
    return f"test_{''.join(random.choices(string.ascii_lowercase + string.digits, k=6))}"

class GlossaryGrpcUser(User):
    """
    Locust пользователь для нагрузочного тестирования gRPC сервиса глоссария
    """
    wait_time = between(1, 3)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.my_created_terms = []
        self.channel = grpc.insecure_channel('localhost:50051')
        self.stub = pb_grpc.GlossaryServiceStub(self.channel)
    
    def _send_request_metrics(self, name, func, *args, **kwargs):
        """
        Вспомогательный метод для отправки метрик в Locust
        """
        start_time = time.time()
        try:
            func(*args, **kwargs)
            total_time = max(1, int((time.time() - start_time) * 1000))
            events.request.fire(
                request_type="grpc",
                name=name,
                response_time=total_time,
                response_length=0,
                exception=None,
            )
        except grpc.RpcError as e:
            total_time = max(1, int((time.time() - start_time) * 1000))
            # Некоторые ошибки не считаем критичными (например, NOT_FOUND для тестов)
            if e.code() == grpc.StatusCode.NOT_FOUND:
                events.request.fire(
                    request_type="grpc",
                    name=name,
                    response_time=total_time,
                    response_length=0,
                    exception=None,
                )
            else:
                events.request.fire(
                    request_type="grpc",
                    name=name,
                    response_time=total_time,
                    response_length=0,
                    exception=e,
                )
        except Exception as e:
            total_time = max(1, int((time.time() - start_time) * 1000))
            events.request.fire(
                request_type="grpc",
                name=name,
                response_time=total_time,
                response_length=0,
                exception=e,
            )
            raise
    
    @task(5)
    def get_all_entries(self):
        """Получить все записи - самая частая операция"""
        self._send_request_metrics(
            "gRPC Get All Entries",
            self.stub.AllEntries,
            pb.GetAllRequest()
        )
    
    @task(3)
    def get_entry(self):
        """Получить одну запись"""
        term_key = random.choice(EXISTING_TERMS)
        self._send_request_metrics(
            "gRPC Get Entry",
            self.stub.GetEntry,
            pb.GetEntryRequest(key=term_key)
        )
    
    @task(2)
    def create_entry(self):
        """Создать новый термин"""
        new_entry_data = generate_random_entry()
        keyword = generate_random_keyword()
        
        entry = pb.Entry(
            name=new_entry_data["name"],
            description=new_entry_data["description"],
            reference=new_entry_data["reference"]
        )
        
        self._send_request_metrics(
            "gRPC Create Entry",
            self.stub.PostEntry,
            pb.PostEntryRequest(key=keyword, entry=entry)
        )
        self.my_created_terms.append(keyword)
    
    @task(1)
    def modify_entry(self):
        """Обновить термины, созданные этим пользователем"""
        if not self.my_created_terms:
            return
        
        term_to_update = random.choice(self.my_created_terms)
        
        self._send_request_metrics(
            "gRPC Modify Entry",
            self.stub.ModifyEntry,
            pb.ModifyEntryRequest(
                key=term_to_update,
                description=f"Updated description for {term_to_update}",
                reference=f"https://updated.com/{term_to_update}"
            )
        )
    
    @task(1)
    def delete_entry(self):
        """Удалить термины, созданные этим пользователем"""
        if not self.my_created_terms:
            return
        
        term_to_delete = random.choice(self.my_created_terms)
        
        self._send_request_metrics(
            "gRPC Delete Entry",
            self.stub.DeleteEntry,
            pb.DeleteEntryRequest(key=term_to_delete)
        )
        if term_to_delete in self.my_created_terms:
            self.my_created_terms.remove(term_to_delete)
    
    def on_stop(self):
        """Закрыть соединение при остановке пользователя"""
        if hasattr(self, 'channel'):
            self.channel.close()
