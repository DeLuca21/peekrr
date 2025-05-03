import os
import yaml
import questionary

CONFIG_PATH = os.path.expanduser("~/.peekrr.yaml")

DEFAULT_CONFIG = {
    "jellyseerr_url": "http://localhost:5055",
    "api_key": "",
    "result_limit": 10,
    "sort": "releaseDate:desc",
    "fuzzy_threshold": 80
}

def prompt_for_config():
    print("🔧 No configuration found. Let’s set it up.")
    jellyseerr_url = questionary.text("Enter your Jellyseerr URL:", default=DEFAULT_CONFIG["jellyseerr_url"]).ask()
    api_key = questionary.text("Enter your Jellyseerr API key:").ask()

    config = {
        "jellyseerr_url": jellyseerr_url.strip(),
        "api_key": api_key.strip(),
        "sort": DEFAULT_CONFIG["sort"],
        "fuzzy_threshold": DEFAULT_CONFIG["fuzzy_threshold"]
    }

    with open(CONFIG_PATH, "w") as f:
        yaml.dump(config, f, default_flow_style=False)

    return config

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            config = yaml.safe_load(f) or {}
    else:
        config = prompt_for_config()

    # Only override with known env keys
    env_override = {
        k: os.environ[k]
        for k in DEFAULT_CONFIG
        if k in os.environ
    }

    return {**DEFAULT_CONFIG, **config, **env_override}


def save_config(config):
    with open(CONFIG_PATH, "w") as f:
        yaml.dump(config, f, default_flow_style=False)

def get_config_path():
    return CONFIG_PATH
