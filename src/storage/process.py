import os
import pickle
import subprocess

import psutil

from src.storage.functions import app_root_path


class Process:
    path = app_root_path("./data/pid.pk")

    @staticmethod
    def load():
        with open(Process.path, 'rb') as file:
            pid = pickle.load(file)
        return pid

    @staticmethod
    def save(pid):
        with open(Process.path, 'wb') as file:
            pickle.dump(pid, file)

    @staticmethod
    def file_exists():
        if os.path.exists(Process.path):
            return True
        return False

    @staticmethod
    def is_active():
        pid = Process.load()
        try:
            process = psutil.Process(pid)
            return process.is_running()
        except psutil.NoSuchProcess:
            return False

    @staticmethod
    def remove_file():
        os.remove(Process.path)
        print("Process file removed")

    @staticmethod
    def terminate():
        pid = Process.load()
        # os.kill(pid, signal.SIGTERM)

        subprocess.run(["taskkill", "/IM", "timed_wallpaper.exe", "/F"], shell=True)

        print("Process " + str(pid) + " terminated")

