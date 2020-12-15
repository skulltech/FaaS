import docker
import importlib
import argparse
import os
import subprocess

def deploy(server, payload, function):
    subprocess.run(["scp", "-q", "run.py", f"sumit@{server}:~"])
    subprocess.run(["scp", "-q", payload, f"sumit@{server}:~"])
    client = docker.DockerClient(base_url=f"tcp://{server}:2375")
    image_tag = os.path.splitext(os.path.basename(payload))[0]

    try:
        client.images.get(image_tag)
    except docker.errors.ImageNotFound:
        client.images.build(path=".", buildargs={"payload": payload}, tag=image_tag)

    r = client.containers.run(image_tag, command=function)
    return r.decode("UTF-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("server", help="Docker server")
    parser.add_argument("payload", help="Python3 application payload")
    parser.add_argument("function", help="Function name")
    args = parser.parse_args()
    result = deploy(args.server, args.payload, args.function)
    print(result)


if __name__ == "__main__":
    main()
