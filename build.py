import os
import subprocess
import distro

# subprocess.run(["rm", "./code_meta.desktop"])

subprocess.run([f"{os.path.dirname(os.path.abspath(__file__))}/deps_install.sh"])

# subprocess.run(['python3', '-m', 'venv', 'myenv'])
# subprocess.run(['source', 'myenv/bin/activate'], shell=True)

# subprocess.run(['pip', 'install', '-r', 'requirements.txt'])

# subprocess.run(['python3', 'db_schema_bootstrap.py'])
# subprocess.run(['pyinstaller', 'main.py'])

# # Deactivate virtual environment
# os.environ.pop("VIRTUAL_ENV", None)
# # Clean up
# subprocess.run(["rm", "-r", "myenv"])

# # Edit code_meta.desktop
# subprocess.run(["cp", "code_meta_template.desktop", "code_meta.desktop"])
# subprocess.run(["cp", "-r", "resources", "./dist/main/resources"])


def replace_string_in_file(fpath, old_str, new_str):
    try:
        # Open the file in read mode
        with open(fpath, 'r') as file:
            # Read the contents of the file
            file_data = file.read()

        file_data = file_data.replace(old_str, new_str)

        # Open the file in write mode
        with open(fpath, 'w') as file:
            # Write the modified data back to the file
            file.write(file_data)


        print(f"Successfully replaced '{old_str}' with '{new_str}' in '{fpath}'")

    except Exception as e:
        print(f"Failed to replace '{old_str}' with '{new_str}' in '{fpath}': {e}")


def move_desktop_file(fpath):
    distro_id = distro.id()

    if distro_id == 'ubuntu':
        dest = '/usr/share/applications/'

    elif distro_id == 'fedora':
        dest = '/usr/share/applications/'

    elif distro_id == 'debian':
        dest = '/usr/share/applications/'

    else:
        # For other Linux distributions, use /usr/local/share/applications/
        dest = '/usr/local/share/applications/'


    subprocess.run(["sudo", "cp", fpath, dest + "code_meta.desktop"])


replace_string_in_file(
    './code_meta.desktop', 
    'path_to_application', 
    os.path.dirname(os.path.abspath(__file__)) + '/dist/main/main'
    )

move_desktop_file('./code_meta.desktop')

