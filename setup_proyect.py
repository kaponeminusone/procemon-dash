import os

# Definimos la estructura del proyecto
project_structure = {
    "app": {
        "__init__.py": "",
        "main.py": "",
        "api": {
            "__init__.py": "",
            "routes.py": "",
        },
        "models": {
            "__init__.py": "",
            "user.py": "",
        },
        "schemas": {
            "__init__.py": "",
            "user.py": "",
        },
        "db": {
            "__init__.py": "",
            "database.py": "",
        },
        "services": {
            "__init__.py": "",
            "user_service.py": "",
        },
    },
    "alembic": {
        "env.py": "",
        "README": "",
        "versions": {},
    },
    "requirements.txt": "",
    "README.md": "",
    ".gitignore": ".venv/\n__pycache__/\n*.pyc\n*.pyo\n*.pyd\n.DS_Store\n*.db\n",
}

def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            with open(path, 'w') as f:
                f.write(content)

if __name__ == "__main__":
    create_structure(os.getcwd(), project_structure)
    print("Estructura del proyecto creada con éxito.")
