# File: aws_config.py
# Path: utils\aws_config.py

import json
import os


def load_aws_config():
    config_file_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')

    with open(config_file_path, 'r') as config_file:
        config = json.load(config_file)
    return config
