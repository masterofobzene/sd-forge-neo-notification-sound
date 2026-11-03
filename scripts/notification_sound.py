# Notification Sound for Forge Neo
# Plays notification.mp3 from the Python side when a generation finishes, so it keeps
# working when the browser is minimized. Windows only (uses the built-in MCI audio API).
#
# Sound file lookup order:
#   1. <extension folder>/notification.mp3
#   2. <webui root>/notification.mp3
# Honors the existing "notification_audio" and "notification_volume" settings.

import sys
import threading
from pathlib import Path

from modules import scripts, shared

EXT_DIR = Path(__file__).resolve().parents[1]
ROOT_DIR = Path(__file__).resolve().parents[3]  # <root>/extensions/<name>/scripts/this_file
_lock = threading.Lock()


def _find_sound():
    for folder in (EXT_DIR, ROOT_DIR, Path.cwd()):
        candidate = folder / "notification.mp3"
        if candidate.exists():
            return candidate
    return None


def _mci(command: str) -> int:
    import ctypes

    return ctypes.windll.winmm.mciSendStringW(command, None, 0, None)


def _play_blocking(sound: Path, volume: int):
    if not _lock.acquire(blocking=False):
        return  # already playing
    try:
        alias = "sdnotif"
        _mci(f"close {alias}")
        if _mci(f'open "{sound}" type mpegvideo alias {alias}') != 0:
            print(f"[notification_sound] could not open {sound}")
            return
        _mci(f"setaudio {alias} volume to {max(0, min(1000, volume * 10))}")
        _mci(f"play {alias} wait")
        _mci(f"close {alias}")
    finally:
        _lock.release()


def play_notification():
    if sys.platform != "win32":
        return
    if not getattr(shared.opts, "notification_audio", True):
        return
    sound = _find_sound()
    if sound is None:
        return
    volume = int(getattr(shared.opts, "notification_volume", 100) or 100)
    threading.Thread(target=_play_blocking, args=(sound, volume), daemon=True).start()


class NotificationSound(scripts.Script):
    def title(self):
        return "Notification Sound"

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def postprocess(self, p, processed, *args):
        play_notification()
