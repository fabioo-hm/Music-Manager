import os
import json
from typing import Dict, List, Optional

def read_json(file_path: str) -> Dict:
    """Lee y retorna el contenido del archivo JSON"""
    try:
        with open(file_path, "r", encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def write_json(file_path: str, data: Dict) -> None:
    """Escribe datos en el archivo JSON"""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding='utf-8') as file:
        json.dump(data, file,ensure_ascii=False, indent=4)

def update_json(file_path: str, data: Dict, path: Optional[List[str]] = None) -> None:
    """
    Actualiza datos en el JSON, opcionalmente en una ruta específica
    Ejemplo: update_json('db.json', {'nuevo': 'dato'}, ['ruta', 'subruta'])
    """
    current_data = read_json(file_path)
    
    if not path:
        current_data.update(data)
    else:
        current = current_data
        for key in path[:-1]:
            current = current.setdefault(key, {})
        if path:
            current.setdefault(path[-1], {}).update(data)

    write_json(file_path, current_data)

def delete_json(file_path: str, path: List[str]) -> bool:
    """
    Elimina datos en la ruta especificada
    Retorna True si se eliminó exitosamente
    """
    data = read_json(file_path)
    current = data

    for key in path[:-1]:
        if key not in current:
            return False
        current = current[key]

    if path and path[-1] in current:
        del current[path[-1]]
        write_json(file_path, data)
        return True
    return False

def initialize_json(file_path: str, initial_structure: Dict) -> None:
    """
    Inicializa el archivo con una estructura base si no existe
    """
    if not os.path.isfile(file_path):
        write_json(file_path, initial_structure)
    else:
        current_data = read_json(file_path)
        for key, value in initial_structure.items():
            if key not in current_data:
                current_data[key] = value
        write_json(file_path, current_data)