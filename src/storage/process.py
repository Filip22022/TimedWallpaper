import subprocess

import psutil


class Process:
    process_name = "wallpaper_switcher.exe"

    @staticmethod
    def is_active():
        for proc in psutil.process_iter():
            try:
                if Process.process_name.lower() in proc.name().lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return False

    @staticmethod
    def terminate():
        subprocess.run(["taskkill", "/IM", Process.process_name, "/F"], shell=True)

