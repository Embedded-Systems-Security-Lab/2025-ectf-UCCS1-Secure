import json
import socket
import binascii
from ectf25.utils.decoder import DecoderIntf
from loguru import logger

def read_json_file(file_path):
    """
    Reads a JSON file and returns the data as a Python dictionary.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: The data from the JSON file as a Python dictionary, or None if an error occurs.
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {file_path}")
        return None

# Example usage:
file_path = 'frame_playback.json'
data = read_json_file(file_path)

decoder = DecoderIntf("/dev/ttyACM0")

if data:
    #print(data)
    for frame in data:
        print(frame["encoded"])
        encoded = binascii.a2b_hex(frame["encoded"])
        decoded = decoder.decode(encoded)
        logger.info(
            (
                b"\n"
                + b"\n".join(
                    [decoded[i : i + 8] for i in range(0, 64, 8)]
                )
            ).decode("utf-8")
        )    
        input("...")
        