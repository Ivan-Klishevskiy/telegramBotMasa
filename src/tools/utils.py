import subprocess
import os
import sys


def install_script_dependencies():
    # Get the directory of the current script
    script_directory = os.path.dirname(os.path.realpath(sys.argv[0]))

    # Generate requirements.txt file using pipreqs
    requirements_file = os.path.join(script_directory, '../requirements.txt')
    subprocess.run(["pipreqs", script_directory, "--no-overwrite"], stdout=open(os.devnull, 'wb'))

    # Install the dependencies using pip
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', requirements_file])

    print("Dependencies installed successfully.")