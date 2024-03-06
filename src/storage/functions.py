import os
import shutil
import sys


def save_image(image_path: str):
    try:
        new_directory = app_root_path(".\data\images")
        os.makedirs(new_directory, exist_ok=True)

        image_file_name = os.path.basename(image_path)

        new_image_path = os.path.join(new_directory, image_file_name)

        shutil.copy(image_path, new_image_path)
        new_image_path = new_image_path.replace("\\", "/")
        print(f"Image copied from '{image_path}' to '{new_image_path}' successfully.")

        return new_image_path

    except FileNotFoundError:
        print(f"Error: Image file '{image_path}' not found.")
    except PermissionError:
        print("Error: Permission denied. Check if you have the necessary permissions.")


def app_root_path(relative_path):
    app_path = ""
    if getattr(sys, 'frozen', False):
        script_path = os.path.dirname(sys.executable)
        app_path = os.path.join(script_path, "../")
    elif __file__:
        script_path = os.path.dirname(os.path.abspath(__file__))
        app_path = os.path.join(script_path, "../../")
    app_path = resolve_path(app_path)
    new_path = resolve_path(os.path.join(app_path, relative_path))

    return new_path


def resolve_path(path):
    new_path = os.path.abspath(path)
    new_path = new_path.replace("\\", "/")
    return new_path
