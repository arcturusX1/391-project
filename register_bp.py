import os
import importlib
from flask import Flask, Blueprint

def register_blueprints(app: Flask, blueprints_folder: str = "blueprints"):
    """
    Dynamically registers all blueprints in the specified folder.

    Args:
        app (Flask): The Flask app instance.
        blueprints_folder (str): The folder containing blueprint files.

    Returns:
        None
    """
    # Get the absolute path to the blueprints folder
    folder_path = os.path.join(os.path.dirname(__file__), blueprints_folder)

    # Iterate over all Python files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".py") and file_name != "__init__.py":
            # Remove the file extension to get the module name
            module_name = f"{blueprints_folder}.{file_name[:-3]}"

            # Dynamically import the module
            module = importlib.import_module(module_name)

            # Search for all Blueprint instances in the module
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, Blueprint):
                    app.register_blueprint(attr)
                    print(f"Registered blueprint: {attr_name} from {module_name}")
