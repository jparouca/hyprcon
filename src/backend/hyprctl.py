import json
import subprocess


class HyprctlWrapper:
    def get_option(self, option):
        result = subprocess.run(['hyprctl', '-j', 'getoption', option], capture_output=True, text=True)
        if result.returncode == 0:
            try:
                data = json.loads(result.stdout)
                return int(data.get('int'))
            except json.JSONDecodeError:
                return 0
        else:
            return 0

    def set_option(self, section, option, value):
        command = ["hyprctl", "--batch", f"keyword {section}:{option} {value}"]
        print(f"Running command: {' '.join(command)}")
        
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        print(f"stdout: {result.stdout}")
        print(f"stderr: {result.stderr}")

