import docker
import importlib
import argparse
import os
import subprocess


def deploy(server, payload):
    client = docker.DockerClient(base_url=f"tcp://{server}:2375")
    image_tag = os.path.splitext(os.path.basename(payload))[0]
    subprocess.run(["scp", "-q", "run.py", f"sumit@{server}:~"])
    subprocess.run(["scp", "-q", payload, f"sumit@{server}:~"])
    image = client.images.build(path=".", buildargs={"payload": payload}, tag=image_tag)
    return image


def run(server, payload, function, update=False):
    client = docker.DockerClient(base_url=f"tcp://{server}:2375")
    image_tag = os.path.splitext(os.path.basename(payload))[0]
    if update:
        deploy(server, payload)
    else:
        try:
            client.images.get(image_tag)
        except docker.errors.ImageNotFound:
            deploy(server, payload)
    r = client.containers.run(image_tag, command=["python3", "run.py", function])
    return r.decode("UTF-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("server", help="docker server")
    parser.add_argument("payload", help="python3 application payload")
    parser.add_argument("function", help="function name")
    parser.add_argument("-u", "--update", help="force update payload", action="store_true")
    args = parser.parse_args()
    result = run(args.server, args.payload, args.function)
    print(result)


if __name__ == "__main__":
    main()
