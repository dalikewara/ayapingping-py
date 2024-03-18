import os
import subprocess
import sys
import urllib.request

name = "AyaPingPing (Py)"
version = "v4.5.5"
language = "Python"
generator_url = "https://raw.githubusercontent.com/dalikewara/ayapingping-sh/master/main_v4.sh"
generator_file = "main.sh"
generator_file_tmp = "main_tmp.sh"
base_structure_dir = "_base_structure"
path_separator = os.path.sep


def main():
    args_len = len(sys.argv)
    command, value, source_prefix, source = "", "", "", ""

    if args_len >= 2:
        command = sys.argv[1]
    if args_len >= 3:
        value = sys.argv[2]
    if args_len >= 4:
        source_prefix = sys.argv[3]
    if args_len >= 5:
        source = sys.argv[4]

    runtime_dir = get_runtime_dir()

    try:
        check_generator(runtime_dir)
    except Exception as e:
        print(e)
        sys.exit(1)

    cmd = [os.path.join(runtime_dir, generator_file), version, language, command, value, source_prefix, source]
    subprocess.run(cmd, stdout=sys.stdout, stderr=sys.stderr, stdin=sys.stdin)


def get_runtime_dir():
    runtime_filepath = os.path.abspath(__file__)
    return os.path.dirname(runtime_filepath)


def sync_generator(runtime_dir):
    try:
        with urllib.request.urlopen(generator_url) as response:
            file_data = response.read()

        with open(os.path.join(runtime_dir, generator_file_tmp), 'wb') as file:
            file.write(file_data)

        if not is_file_valid_sh(os.path.join(runtime_dir, generator_file_tmp)):
            return

        with open(os.path.join(runtime_dir, generator_file_tmp), 'rb') as file:
            file_data = file.read()

        with open(os.path.join(runtime_dir, generator_file), 'wb') as file:
            file.write(file_data)

    except Exception as e:
        pass


def check_generator(runtime_dir):
    chmod(runtime_dir)
    sync_generator(runtime_dir)

    if not is_file(os.path.join(runtime_dir, generator_file)):
        raise FileNotFoundError(
            "no generator found, please connect to the internet and run the command again to synchronize")

    if not is_file_valid_sh(os.path.join(runtime_dir, generator_file)):
        raise ValueError(
            "invalid generator file, please connect to the internet and run the command again to synchronize")


def chmod(runtime_dir):
    os.chmod(os.path.join(runtime_dir, generator_file), 0o775)
    os.chmod(os.path.join(runtime_dir, generator_file_tmp), 0o775)

    for root, dirs, files in os.walk(os.path.join(runtime_dir, base_structure_dir)):
        for dir_name in dirs:
            os.chmod(os.path.join(root, dir_name), 0o775)
        for file_name in files:
            os.chmod(os.path.join(root, file_name), 0o664)


def is_file(path):
    return os.path.isfile(path)


def is_file_valid_sh(path):
    try:
        with open(path, 'rb') as file:
            content = file.read()
            return content.startswith(b"#!/bin/sh")
    except Exception as e:
        return False


if __name__ == "__main__":
    main()
