import os
import re

class ConfigParser:
    def __init__(self):
        self.home = os.path.expanduser("~")
        self.main_config_file = os.path.join(self.home, ".config", "hypr", "hyprland.conf")
        self.temp_config_file = os.path.join(self.home, "Projects", "py-qt", "temp.conf")

    def parse(self):
        if not os.path.isfile(self.main_config_file):
            raise Exception(f"hyprland.conf file not found: {self.main_config_file}")

        with open(self.temp_config_file, "w") as temp_file:
            self.parse_file(self.main_config_file, temp_file)

            with open(self.main_config_file) as file:
                for line in file:
                    if line.startswith("source"):
                        sourced_file = line.split("=", 1)[1].strip()
                        sourced_file = os.path.expanduser(sourced_file)
                        self.parse_file(sourced_file, temp_file)

    def parse_file(self, file_path, temp_file):
        if not os.path.isfile(file_path):
            raise Exception(f"Sourced file not found: {file_path}")

        with open(file_path) as file:
            for line in file:
                temp_file.write(line)

if __name__ == "__main__":
    parser = ConfigParser()
    parser.parse()

