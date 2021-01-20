#### Running `cadvisor` for docker stats monitoring tool:

> got dockerfile from here: https://hub.docker.com/r/vimagick/cadvisor/dockerfile/

Ansible playbook additional config for this:
- Install pip and docker-py (this is necessary for to run docker from ansible playbook)
- Run cadvisor container  

GUI will be hosted on: 192.168.33.10:8080 (server_ip:8080)

> Command for running (this works)
sudo docker run --volume=/:/rootfs:ro --volume=/var/run:/var/run:ro --volume=/sys:/sys:ro --volume=/var/lib/docker/:/var/lib/docker:ro --volume=/dev/disk/:/dev/disk:ro --publish=8080:8080 --detach=true --name=cadvisor --privileged --device=/dev/kmsg gcr.io/cadvisor/cadvisor:v0.36.0

> Somehow this doesn't connect automatically to docker daemon but it shows the GUI of Usage of CPU
    - name: Create build directory
      file:
        path: /root/monitor
        state: directory
        owner: root
        group: root
        mode: '0755'
    
    - name: Copy cadvisor Dockerfile to docker-host
      copy:
        src: ./monitor/Dockerfile
        dest: /root/monitor/Dockerfile
        owner: root
        group: root
        mode: '0644'

    - name: Build container image from Dockerfile
      docker_image:
        name: moni
        tag: v1
        path: /root/monitor
        state: present

    - name: Run this image in a container for monitoring
      docker_container:
          name: mongui
          image: "moni:v1"
          state: started
          ports:
            - "8080:8080"

    - name: Check if container is running
      shell: docker ps
