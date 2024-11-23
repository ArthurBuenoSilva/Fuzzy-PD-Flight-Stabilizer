import os
import socket
from contextlib import closing


def get_available_port():
    """Returns a port that's not being used"""
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


HOST = "127.0.0.1"
PORT = get_available_port()

DATASETS_FOLDER = os.path.join("app", "static", "datasets")

if not os.path.exists(DATASETS_FOLDER):
    os.mkdir(DATASETS_FOLDER)


class Configuration:
    SECRET_KEY = "e61886f07ce136bf67b0dff26f73de44f0b11ca95337dc05bbcb010bb1b61645"
