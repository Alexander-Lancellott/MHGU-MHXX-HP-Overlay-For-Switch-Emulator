import subprocess
from modules.utils import absolute_path


def main():
    path = absolute_path("setup_cx.py")
    py_path = absolute_path(".venv\\Scripts\\python")

    command_options = [py_path, path, "build"]

    subprocess.run(command_options)


if __name__ == "__main__":
    main()
