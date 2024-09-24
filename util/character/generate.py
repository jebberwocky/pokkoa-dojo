import time
import json
import os
from util.character import GPTToneConfig, Character, sweet, encouraging, casual, professional, sharp_tongued, cbt_therapist, mindfulness_healer, default, boyfriend, motivational_sister, best_friend, therapist, poison_tongue, straightforwardrobot, cbttherapist, mindfulnesshealer
from datetime import datetime

def store_string_with_expiry(string, filename, expiry_seconds):
    """
    Stores a string in a local file with an expiration time.

    Args:
        string (str): The string to be stored.
        filename (str): The name of the file to store the string.
        expiry_seconds (int): The number of seconds until the file expires.
    """
    expiry_time = time.time() + expiry_seconds

    with open(filename, 'w') as file:
        file.write(string + '\n')
        file.write(str(expiry_time))


def read_string_with_expiry(filename):
    """
    Reads a string from a local file, checking if it has expired.

    Args:
        filename (str): The name of the file containing the string.

    Returns:
        str: The stored string if it has not expired, otherwise None.
    """
    try:
        with open(filename, 'r') as file:
            string = file.readline().strip()
            expiry_time = float(file.readline())

        if time.time() < expiry_time:
            return string
        else:
            return None
    except (FileNotFoundError, ValueError):
        return None

def generate_character_json(file_path):
    tone_configs = {
        "sweet": sweet,
        "encouraging": encouraging,
        "casual": casual,
        "professional": professional,
        "sharp_tongued": sharp_tongued,
        "cbt_therapist": cbt_therapist,
        "mindfulness_healer": mindfulness_healer
    }

    characters = {
        "default": default,
        "boyfriend": boyfriend,
        "motivational_sister": motivational_sister,
        "best_friend": best_friend,
        "therapist": therapist,
        "poison_tongue": poison_tongue,
        "straightforward_robot": straightforwardrobot,
        "cbt_therapist": cbttherapist,
        "mindfulness_healer": mindfulnesshealer
    }

    tone_configs_dict = {name: config.__dict__ for name, config in tone_configs.items()}
    characters_dict = {name: {
        "name": char.name,
        "role": char.role,
        "personality": char.personality,
        "tone_config": next(key for key, value in tone_configs.items() if value == char.tone_config),
        "prompt": char.prompt
    } for name, char in characters.items()}

    data = {
        "tone_configs": tone_configs_dict,
        "characters": characters_dict
    }

    if os.path.exists(file_path):
        base, ext = os.path.splitext(file_path)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.rename(file_path, f"{base}_old_{timestamp}{ext}")

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    generate_character_json("character.json")