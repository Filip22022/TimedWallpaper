import pickle

from src.storage.functions import app_root_path


class WallpaperData:
    path = app_root_path("./data/wallpaper_data.pk")

    @staticmethod
    def save(times, image_paths):
        data = list()
        for value, path in zip(times, image_paths):
            if value is None or path is None:
                raise Exception("Unspecified Image")
            data.append((value, path))

        print("Saving data: " + str(data))
        with open(WallpaperData.path, 'wb') as file:
            pickle.dump(data, file)

    @staticmethod
    def load():
        with open(WallpaperData.path, 'rb') as file:
            wallpaper_data = pickle.load(file)
        return wallpaper_data
