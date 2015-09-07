 
import json

def get():
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config

def set(config):
    with open('config.json', 'w') as f:
        json.dump(config, f)

if __name__ == "__main__":
    
    d = get()
    print(d)