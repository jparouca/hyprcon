import json
import subprocess


class HyprctlWrapper:
    def get_option(self, section, option, dataType):
        result = subprocess.run(['hyprctl', '-j', f'getoption {section}:{option}'], capture_output=True, text=True)
        if result.returncode == 0:
            try:
                data = json.loads(result.stdout)
                return (data.get(dataType))
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

