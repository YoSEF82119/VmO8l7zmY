# 代码生成时间: 2025-09-24 00:30:57
from quart import Quart, request, jsonify
import json
import os
from pathlib import Path
from typing import Any, Dict, Optional, List

# Initialize the Quart application
app = Quart(__name__)

# Define the path to the configuration directory
CONFIG_DIR = 'configs'

# Define the path to the example configuration file
DEFAULT_CONFIG_PATH = Path(CONFIG_DIR) / 'default_config.json'

# Ensure the configuration directory exists
os.makedirs(CONFIG_DIR, exist_ok=True)

class ConfigManager:
    """
    A class to manage configuration files.
    Provides methods to read, update, and delete configuration files.
    """

    def __init__(self, config_dir: str = CONFIG_DIR):
        self.config_dir = config_dir

    def read_config(self, config_name: str) -> Optional[Dict[str, Any]]:
        """
        Read a configuration file from the config directory.
        """
        try:
            config_path = Path(self.config_dir) / config_name
            with open(config_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return None
        except json.JSONDecodeError:
            return None

    def update_config(self, config_name: str, config_data: Dict[str, Any]) -> bool:
        """
        Update a configuration file with new data.
        """
        try:
            config_path = Path(self.config_dir) / config_name
            with open(config_path, 'w') as file:
                json.dump(config_data, file, indent=4)
            return True
        except Exception as e:
            print(f"Error updating config: {e}")
            return False

    def delete_config(self, config_name: str) -> bool:
        """
        Delete a configuration file from the config directory.
        """
        try:
            config_path = Path(self.config_dir) / config_name
            config_path.unlink()
            return True
        except FileNotFoundError:
            return False
        except Exception as e:
            print(f"Error deleting config: {e}")
            return False

# Create an instance of ConfigManager
config_manager = ConfigManager()

@app.route('/config/<config_name>', methods=['GET'])
async def get_config(config_name: str):
    """
    GET endpoint to retrieve a configuration file.
    """
    config_data = config_manager.read_config(config_name)
    if config_data is None:
        return jsonify({'error': f'Config {config_name} not found'}), 404
    return jsonify(config_data)

@app.route('/config/<config_name>', methods=['PUT'])
async def update_config_endpoint(config_name: str):
    """
    PUT endpoint to update a configuration file.
    """
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400

    config_data = await request.get_json()
    success = config_manager.update_config(config_name, config_data)
    if success:
        return jsonify({'message': 'Config updated successfully'}), 200
    else:
        return jsonify({'error': 'Failed to update config'}), 500

@app.route('/config/<config_name>', methods=['DELETE'])
async def delete_config_endpoint(config_name: str):
    """
    DELETE endpoint to delete a configuration file.
    """
    success = config_manager.delete_config(config_name)
    if success:
        return jsonify({'message': 'Config deleted successfully'}), 200
    else:
        return jsonify({'error': 'Failed to delete config'}), 500

if __name__ == '__main__':
    # Run the Quart application
    app.run(debug=True)
