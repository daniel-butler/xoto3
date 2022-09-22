#!/usr/bin/env python
import argparse
import os
import subprocess
import glob


def find_pipenv_dir(fileorpath: str) -> str:
    fileorpath = os.path.abspath(fileorpath)
    pipenv_dir = (
        fileorpath
        if os.path.isdir(fileorpath)
        else os.path.dirname(fileorpath)
    )

    while len(pipenv_dir) > 1:
        if os.path.exists(os.path.join(pipenv_dir, "Pipfile")):
            return pipenv_dir
        pipenv_dir = os.path.dirname(pipenv_dir)
    return ""


def get_pipenv_venv_site_packages(pipenv_dir: str) -> str:
    venv_output = subprocess.check_output(["pipenv", "--venv"], text=True, cwd=pipenv_dir).rstrip(
        "\n"
    )
    glob_out = glob.glob(f"{venv_output}/lib/python*")
    return f"{glob_out[0]}/site-packages/"


def get_pythonpath_for_pipfile_dir_and_venv(filepath: str) -> str:
    if pipenv_dir := find_pipenv_dir(filepath):
        return ":".join([pipenv_dir, get_pipenv_venv_site_packages(pipenv_dir)])
    return ""


def main():
    """Prints a PYTHONPATH including the Pipfile's own directory, if one is found"""
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()

    if pythonpath := get_pythonpath_for_pipfile_dir_and_venv(args.path):
        print(pythonpath)


if __name__ == "__main__":
    main()
