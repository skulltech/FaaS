import importlib
import uuid
import argparse


def run(function_name):
    names = function_name.split(".")
    module = importlib.import_module(".".join(names[:-1]),)
    function = getattr(module, names[-1])
    result = function()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("function", help="Function name")
    args = parser.parse_args()
    result = run(args.function)
    print(result)


if __name__ == "__main__":
    main()
