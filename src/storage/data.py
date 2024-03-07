import pickle

from src.storage.functions import app_root_path


class WallpaperData:
    path = app_root_path("./data/wallpaper_data.pk")

    @staticmethod
    def save(data):
        print("Saving data: " + str(data))
        with open(WallpaperData.path, 'wb') as file:
            pickle.dump(data, file)

    @staticmethod
    def load():
        with open(WallpaperData.path, 'rb') as file:
            wallpaper_data = pickle.load(file)
        return wallpaper_data
