"""
Locust тесты для REST API глоссария
"""
import random
import string
from locust import HttpUser, task, between

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

class GlossaryRestUser(HttpUser):
    """
    Locust пользователь для нагрузочного тестирования REST сервиса глоссария
    """
    wait_time = between(1, 3)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.my_created_terms = []
    
    @task(5)
    def get_all_entries(self):
        """Получить все записи - самая частая операция"""
        with self.client.get("/", catch_response=True, name="REST Get All Entries") as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed with status {response.status_code}")
    
    @task(3)
    def get_entry(self):
        """Получить одну запись"""
        term_key = random.choice(EXISTING_TERMS)
        with self.client.get(f"/entry/{term_key}", catch_response=True, name="REST Get Entry") as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 404:
                response.success()
            else:
                response.failure(f"Failed with status {response.status_code}")
    
    @task(2)
    def create_entry(self):
        """Создать новый термин"""
        new_entry = generate_random_entry()
        keyword = generate_random_keyword()
        
        with self.client.post(
            f"/entry/{keyword}", 
            json=new_entry, 
            catch_response=True, 
            name="REST Create Entry"
        ) as response:
            if response.status_code == 200:
                response.success()
                self.my_created_terms.append(keyword)
            elif response.status_code == 400:
                response.success()
            else:
                response.failure(f"Failed with status {response.status_code}")
    
    @task(1)
    def modify_entry(self):
        """Обновить термины, созданные этим пользователем"""
        if not self.my_created_terms:
            return
        
        term_to_update = random.choice(self.my_created_terms)
        update_data = {
            "description": f"Updated description for {term_to_update}",
            "reference": f"https://updated.com/{term_to_update}"
        }
        
        with self.client.put(
            f"/entry/{term_to_update}", 
            json=update_data, 
            catch_response=True, 
            name="REST Modify Entry"
        ) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 404:
                response.success()
                if term_to_update in self.my_created_terms:
                    self.my_created_terms.remove(term_to_update)
            else:
                response.failure(f"Failed with status {response.status_code}")
    
    @task(1)
    def delete_entry(self):
        """Удалить термины, созданные этим пользователем"""
        if not self.my_created_terms:
            return
        
        term_to_delete = random.choice(self.my_created_terms)
        
        with self.client.delete(
            f"/entry/{term_to_delete}", 
            catch_response=True, 
            name="REST Delete Entry"
        ) as response:
            if response.status_code == 200:
                response.success()
                if term_to_delete in self.my_created_terms:
                    self.my_created_terms.remove(term_to_delete)
            elif response.status_code == 404:
                response.success()
                if term_to_delete in self.my_created_terms:
                    self.my_created_terms.remove(term_to_delete)
            else:
                response.failure(f"Failed with status {response.status_code}")
