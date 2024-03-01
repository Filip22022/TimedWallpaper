import os

real_path = os.path.realpath(__file__)

win_wallpaper_path = os.path.join(os.path.dirname(real_path), 'wallpaper.exe')


def set_wallpaper(file_path):
    if type(file_path) != str:
        raise TypeError("file path was expected a string")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f'wallpaper file was not found in {file_path}')
    f = os.popen(f'{win_wallpaper_path} set {file_path}')
    return f.readlines()
