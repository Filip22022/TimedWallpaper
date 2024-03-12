import ctypes
import os
import pickle
import sys
import time

import schedule


def app_root_path(relative_path):
    app_path = ""
    if getattr(sys, 'frozen', False):
        script_path = os.path.dirname(sys.executable)
        app_path = os.path.join(script_path, "./")
    elif __file__:
        script_path = os.path.dirname(os.path.abspath(__file__))
        app_path = os.path.join(script_path, "../../")

    new_path = os.path.join(app_path, relative_path)
    new_path = os.path.abspath(new_path)
    new_path = new_path.replace("\\", "/")
    return new_path


def set_wallpaper(file_path):
    if type(file_path) != str:
        raise TypeError("file path was expected a string")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f'wallpaper file was not found in {file_path}')
    ctypes.windll.user32.SystemParametersInfoW(20, 0, file_path, 3)


# Load user settings
data_path = app_root_path("./data/wallpaper_data.pk")
with open(data_path, 'rb') as file:
    wallpaper_data = pickle.load(file)

print("Setting up changepoints:")
for change_time, path in wallpaper_data:
    print(change_time + "    " + path)
    schedule.every().day.at(change_time).do(set_wallpaper, file_path=path)

while True:
    schedule.run_pending()
    time.sleep(1)
