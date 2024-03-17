import os
import subprocess
import sys

name = "AyaPingPing (Py)"
version = "v4.4.1"
language = "Python"
path_separator = os.path.sep


def main():
    args_len = len(sys.argv)
    command = value = source_prefix = source = ""

    if args_len >= 2:
        command = sys.argv[1]
    if args_len >= 3:
        value = sys.argv[2]
    if args_len >= 4:
        source_prefix = sys.argv[3]
    if args_len >= 5:
        source = sys.argv[4]

    runtime_dir, err = get_runtime_dir()
    if err is not None:
        raise err

    cmd = [os.path.join(runtime_dir, 'main_v4.sh'), version, language, command, value, source_prefix, source]
    subprocess.run(cmd, stdout=sys.stdout, stderr=sys.stderr, stdin=sys.stdin)


def get_runtime_dir():
    try:
        frame = sys._getframe(0)
        runtime_file_path = frame.f_code.co_filename
        return os.path.dirname(os.path.abspath(runtime_file_path)), None
    except Exception as e:
        return None, e


if __name__ == "__main__":
    main()
