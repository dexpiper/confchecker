import json
from optparse import OptionParser


DEFAULT_PATH = './config.json'


def do_if_ok() -> str:
    print("Ok. Test passed")


def do_if_failed() -> str:
    print("ERROR: test failed")


def get_config(path: str) -> dict:
    """Open config file with provided path"""
    with open(path, 'r') as file:
        dct = json.loads(file.read())
    return dct


def register(initial_task: int, cfg: dict) -> bool:
    """
    Recursion call. Would return RecursionError if config failes
    """
    lst_tasks = cfg.get(str(initial_task), [])
    if not len(lst_tasks):
        return True
    for task in lst_tasks:
        register(task, cfg)


def main(path) -> bool:
    cfg: dict = get_config(path)
    for key in cfg:
        try:
            register(key, cfg)
        except RecursionError:
            return False
    return True


if __name__ == "__main__":
    op = OptionParser()
    op.add_option("-p", "--path", action="store", default=DEFAULT_PATH)
    opts, _ = op.parse_args()
    result = main(opts.path)
    do_if_ok() if result else do_if_failed()
