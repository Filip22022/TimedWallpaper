import os
import pickle
import random
import shutil

from PyQt5.QtGui import QColor


def clear_layout(layout):
    for i in reversed(range(layout.count())):
        layout.itemAt(i).widget().setParent(None)


def set_random_background_color(self):
    # Generate random RGB values
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)

    # Create a QColor with the random RGB values
    color = QColor(red, green, blue)

    # Set the background color of the widget
    self.setStyleSheet(f"background-color: {color.name()};")


def save_image(image_path: str):
    script_path = os.path.dirname(os.path.abspath(__file__))

    try:
        new_directory = os.path.join(script_path, "..\..\data\images")
        new_directory = os.path.abspath(new_directory)
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
        print(f"Error: Permission denied. Check if you have the necessary permissions.")


def get_process():
    with open("../data/pid.pk", 'rb') as file:
        pid = pickle.load(file)
    return pid


def save_process():
    pid = os.getpid()
    with open("../data/pid.pk", 'wb') as file:
        pickle.dump(pid, file)


def save_data(data):
    data_filename = "../data/wallpaper_data.pk"

    with open(data_filename, 'wb') as file:
        pickle.dump(data, file)


def load_data():
    data_filename = "../data/wallpaper_data.pk"

    with open(data_filename, 'rb') as file:
        wallpaper_data = pickle.load(file)
    return wallpaper_data
