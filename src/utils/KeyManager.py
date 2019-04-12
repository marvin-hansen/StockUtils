import os
import pickle
from enum import Enum, unique, auto
from pathlib import Path


@unique
class KEYS(Enum):
    """ ENUM to encode valid keys """
    ALPHA = auto()
    QUANDL = auto()


DBG = False
alpha_key_file = "alpha.key"
quandl_key_file = "quandl.key"


def set_key(key: KEYS, key_folder: str = "keys") -> str:
    """
    :param key:
    :param key_folder:
    :return:
    """
    if key is KEYS.ALPHA:
        return load_key(k_file=alpha_key_file, k_folder=key_folder)

    if key is KEYS.QUANDL:
        return load_key(k_file=quandl_key_file, k_folder=key_folder)


def get_key(file: str = None, folder: str = "keys") -> str:
    return load_key(k_file=file, k_folder=folder)


def load_key(k_file: str = None, k_folder: str = "keys") -> str:
    """
    Set access key to either the provided string or loads from a local file containing the string.
    Note, the file must be created with "store_key" to ensure proper reading.

    :param k_folder: key folder
    :param k_file: key_file containing the key
    :return: str key loaded from file
    """
    if k_file is None:
        print("Please pass a path to a key file to load a key")

    if k_folder is None:
        print("Please pass a folder to a key file to load a key")

    else:
        if not os.path.exists(k_folder):
            print("Key folder does not exists")

        path = Path(k_folder + "/" + k_file)
        exists: bool = os.path.isfile(path)

        if not exists:
            print("Key file does not exists: " + k_file)

        else:
            if DBG:
                print("Loading key from from file: " + str(path))
            return pickle.load(open(path, "rb"))


def store_key(key: str = None, key_file: object = None, key_folder: object = "keys"):
    """
    Stores a key in a file.

    Ensure the key files and folder are all in the .gitignore file to prevent accidental leakage.

    :param key_folder: folder in which to store the key. Default: "keys"
    :param key: str - access key / token.
    :param key_file: file name. Default: "key.p"
    :return: void
    """
    if key is None and key_folder is None and key_file is None:
        print("Please pass a key, a folder, and a path to a key file to store the key")
    elif key_file is None:
        print("Please set a key file to store the key in it")
    elif key_folder is None:
        print("Please set a folder name")
    elif key is None:
        print("Please pass a key as string to store in a file: " + key_file)
    else:  # Create key folder if it does not exists yet.
        if not os.path.exists(key_folder):
            os.makedirs(key_folder)

        path = Path(key_folder + "/" + key_file)
        if DBG:
            print("Store key in file: " + str(path))
        pickle.dump(key, open(path, "wb"))
