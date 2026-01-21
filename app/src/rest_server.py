"""
REST сервер для глоссария терминов на FastAPI
"""
from fastapi import FastAPI, HTTPException
from typing import Dict

try:
    from app.src.models import Entry, ModifyEntry
    from app.src.glossary import glossary
except ImportError:
    import sys
    import os
    root_dir = os.path.join(os.path.dirname(__file__), '../..')
    root_dir = os.path.abspath(root_dir)
    if root_dir not in sys.path:
        sys.path.insert(0, root_dir)
    from app.src.models import Entry, ModifyEntry
    from app.src.glossary import glossary

app = FastAPI(title="Glossary REST API", version="1.0.0")

# Получение списка всех терминов
@app.get("/", response_model=Dict[str, Entry])
async def all_entries():
    """
    Получить все записи из словаря
    """
    return glossary

# Получение информации о конкретном термине по ключевому слову
@app.get("/entry/{key}", response_model=Entry)
async def get_entry(key: str):
    """
    Получить одну запись по ключу
    """
    entry = glossary.get(key)
    if not entry:
        raise HTTPException(status_code=404, detail=f"'{key}' не обнаружен в базе")
    return entry

# Добавление нового термина с описанием
@app.post("/entry/{key}", response_model=Entry)
async def post_entry(key: str, entry: Entry):
    """
    Создать новую запись
    """
    if key in glossary:
        raise HTTPException(status_code=400, detail=f"'{key}' уже есть в словаре")
    glossary[key] = entry
    return glossary[key]

# Обновление существующего термина
@app.put("/entry/{key}", response_model=Entry)
async def modify_entry(key: str, entry: ModifyEntry):
    """
    Обновить существующую запись
    """
    if key not in glossary:
        raise HTTPException(status_code=404, detail=f"'{key}' не обнаружен в базе")
    
    if entry.description is not None:
        glossary[key].description = entry.description
    if entry.reference is not None:
        glossary[key].reference = entry.reference
    
    return glossary[key]

# Удаление термина из глоссария
@app.delete("/entry/{key}", response_model=Entry)
async def delete_entry(key: str):
    """
    Удалить запись из словаря
    """
    if key not in glossary:
        raise HTTPException(status_code=404, detail=f"'{key}' не обнаружен в базе")
    return glossary.pop(key)
