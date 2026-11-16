import json
from pathlib import Path


DATA_FOLDER = Path("data")
SOUNDS_FILE = DATA_FOLDER / "sounds.json"


def load_sounds():
    DATA_FOLDER.mkdir(exist_ok=True)

    if not SOUNDS_FILE.exists():
        save_sounds([])
        return []

    try:
        with open(SOUNDS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        sounds = data.get("sounds", [])
        if not isinstance(sounds, list):
            return []

        return [
            sound for sound in sounds
            if isinstance(sound, dict)
            and "id" in sound
            and "name" in sound
            and "file" in sound
        ]

    except (json.JSONDecodeError, OSError):
        return []


def save_sounds(sounds):
    DATA_FOLDER.mkdir(exist_ok=True)

    data = {"sounds": sounds}
    temporary_file = DATA_FOLDER / "sounds_temp.json"

    with open(temporary_file, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    temporary_file.replace(SOUNDS_FILE)
