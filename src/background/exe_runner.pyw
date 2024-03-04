import os
import pickle

import schedule
import time

from src.utilities.functions import save_process

real_path = os.path.realpath(__file__)
win_wallpaper_path = os.path.join(os.path.dirname(real_path), 'wallpaper.exe')

save_process()


def set_wallpaper(file_path):
    if type(file_path) != str:
        raise TypeError("file path was expected a string")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f'wallpaper file was not found in {file_path}')
    f = os.popen(f'{win_wallpaper_path} set {file_path}')
    return f.readlines()


wallpaper_data = load_data()

for change_time, path in wallpaper_data:
    schedule.every().day.at(change_time).do(set_wallpaper, file_path=path)

while True:
    schedule.run_pending()
    time.sleep(1)
