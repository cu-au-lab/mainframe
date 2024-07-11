import json
from typing import List, Dict
from pathlib import Path

class ConfigManager:
    def __init__(self, config_path: str):
        self.config_path = Path(config_path)
        self.config: List[Dict] = []

    def load_config(self) -> None:
        """Load the configuration from the JSON file."""
        try:
            with self.config_path.open('r') as config_file:
                self.config = json.load(config_file)
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON in configuration file: {self.config_path}")
        except IOError:
            raise IOError(f"Unable to read configuration file: {self.config_path}")

    def get_tasks(self) -> List[Dict]:
        """Return the list of tasks from the configuration."""
        return self.config

    def validate_config(self) -> None:
        """Validate the configuration structure."""
        required_keys = {'name', 'utility', 'macro', 'inputs', 'outputs', 'instances', 'capacity'}
        for task in self.config:
            if not required_keys.issubset(task.keys()):
                missing_keys = required_keys - set(task.keys())
                raise ValueError(f"Missing required keys in task configuration: {missing_keys}")

    def get_utilities(self) -> List[str]:
        """Get a list of unique utilities used in the configuration."""
        return list(set(task['utility'] for task in self.config))
