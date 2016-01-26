 
import json

# Path to configuration file
path = 'config.json'

# Defaults
defaults = {}
defaults['bind_port_range'] = [50000, 50050]
defaults['known_hosts'] = ['localhost']

def get():
    global path
    global defaults
    try:
        with open(path, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        return defaults
    return config

def set(config):
    global path
    with open(path, 'w') as f:
        json.dump(config, f)
