from pathlib import Path

class ConfigParser:
    def __init__(self):
        self.config_path = Path.home() / ".config" / "hypr" / "hyprland.conf"

    def parse_config(self):
        config = {}

        if self.config_path.exists():
            with self.config_path.open() as f:
                for line in f:
                    if not line.startswith("#") and "=" in line:  # Ignore comments and lines without '='
                        key, value = line.strip().split("=", 1)
                        config[key.strip()] = value.strip()

        return config

    def parse_sourced_files(self):
        source_keyword = "source"
        sourced_files = {}

        for line in self.config_path.read_text().split("\n"):
            if line.startswith(source_keyword):
                sourced_file = line.split("=")[1].strip()
                sourced_file_path = Path(sourced_file).expanduser()

                if not sourced_file_path.exists():
                    raise Exception(f"Sourced file not found: {sourced_file_path}")

                with sourced_file_path.open() as f:
                    for line in f:
                        if not line.startswith("#") and "=" in line:  # Ignore comments and lines without '='
                            key, value = line.strip().split("=", 1)
                            sourced_files[key.strip()] = value.strip()

        return sourced_files

    def parse(self):
        config = self.parse_config()
        sourced_files = self.parse_sourced_files()

        config.update(sourced_files)

        return config


    @staticmethod
    def handle_update(section, property_name, value):
        config_file = Path.home() / ".config" / 'hypr'/ "hyprland.conf"
        
        # Read the config file and store the lines
        with config_file.open() as f:
            lines = f.readlines()

        # Find the property and update its value
        in_section = False
        found_property = False
        for i, line in enumerate(lines):
            # Check if we've entered the right section
            if line.strip() == f"{section} {{":
                in_section = True
            elif line.strip() == "}":
                in_section = False

            # Check if the current line is the property
            if in_section and line.strip().startswith(property_name):
                lines[i] = f"{property_name} = {str(value).lower()}\n"
                found_property = True
                break

        if not found_property:
            # If property wasn't found, add it to the section
            for i, line in enumerate(lines):
                if line.strip() == f"{section} {{":
                    # If the next line is a closing brace, insert the property before the closing brace
                    if lines[i+1].strip() == "}":
                        lines.insert(i+1, f"    {property_name} = {str(value).lower()}\n")
                    else:  # If the section is not empty, insert the property after the opening brace
                        lines.insert(i+2, f"    {property_name} = {str(value).lower()}\n")
                    break

        # Write the lines back to the file
        with config_file.open("w") as f:
            print(lines)
            f.writelines(lines)
parser = ConfigParser()
config = parser.parse()

print(config)

