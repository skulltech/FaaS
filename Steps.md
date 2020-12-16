# FaaS

1. Install VirtualBox.
2. Create a VM, name it "Server 1".
	- Ubuntu Server 20.04.1
	- 4096 MB RAM.
	- 10 GB VMDK image, [reference](https://superuser.com/a/440384).
	- While installation, import SSH key from public Github account for easy access.
	- Change the network setting so that it uses a network adapter in briged mode, [reference](https://www.nakivo.com/blog/virtualbox-network-setting-guide/).
2. Set up an apt cache on localhost following [this tutorial](https://askubuntu.com/a/3507).
3. Set up localhost and the creted VM "Server 1" to use this apt cache.
4. Run an apt update, apt upgrade so that everything is up-to-date.
5. Shutdown the VM and take a snapshot of it at this moment, so that similar VMs can be created easily. Name it "Snapshot 1".
6. Install Docker on "Server 1" following the [docs](https://docs.docker.com/engine/install/ubuntu).
7. Do some post-installation steps following [this](https://docs.docker.com/engine/install/linux-postinstall/). Especially the following
	- Manage docker as a non-root user
	- Configure docker to start on boot
	- Configure remote access through systemd unit file
8. Connect to the docker server remotely using the exposed port and API. Confirm it works with both the CLI client and then the Python SDK.
9. Start looking into how to deploy a Python function, run it in a container, and get the result. Relevant sources
	- https://hub.docker.com/_/python
	- https://runnable.com/docker/python/dockerize-your-python-application
	- https://vsupalov.com/docker-env-vars/
	- https://goinbigdata.com/docker-run-vs-cmd-vs-entrypoint
	- https://habiletechnologies.com/blog/better-saving-files-database-file-system/
	- https://codeburst.io/know-your-http-status-a-cheat-sheet-for-http-status-codes-5fb43863e589
	- https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/