from pathlib import Path

class ConfigParser:
    def __init__(self):
        self.config_path = Path.home() / ".config" / "hypr" / "hyprland.conf"

    def parse(self):
        config_data = {}
        
        # Parse main config file
        with open(self.config_path, 'r') as file:
            section = None
            for line in file:
                stripped_line = line.strip()
                if stripped_line.endswith('{'):
                    section = stripped_line[:-2].strip()  # Extract section name
                elif "=" in stripped_line:
                    key, value = map(str.strip, stripped_line.split("=", 1))
                    if key == 'source':
                        sourced_file = Path(value).expanduser()
                        if not sourced_file.exists():
                            raise Exception(f"Sourced file not found: {sourced_file}")
                        else:
                            with open(sourced_file, 'r') as source_file:
                                source_section = None
                                for source_line in source_file:
                                    source_stripped_line = source_line.strip()
                                    if source_stripped_line.endswith('{'):
                                        source_section = source_stripped_line[:-2].strip()  # Extract section name from sourced file
                                    elif "=" in source_stripped_line:
                                        source_key, source_value = map(str.strip, source_stripped_line.split("=", 1))
                                        config_data[source_key] = (source_value, sourced_file, source_section)
                    else:
                        config_data[key] = (value, self.config_path, section)
        return config_data

if __name__ == "__main__":
    parser = ConfigParser()
    config = parser.parse()
    print(config)
