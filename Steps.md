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
