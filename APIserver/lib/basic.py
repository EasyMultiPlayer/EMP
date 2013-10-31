import os
import subprocess


def _exe(command):
    os.system("bash -c '" + command + "&'>/dev/null")


def pipe(command, kind='str'):
    if kind == 'str':
        return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.readlines()[
                   0][1:-2]
    else:
        return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.readlines()


