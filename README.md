# FaaS
Handcrafted FaaS platform.

## Instructions

1. Install the following on your development machine
    - VirtualBox
    - Vagrant
    - Ansible
    - Docker

2. Check the IP address of your computer using the command `$ ip a`, then change `192.168.0.105` with your IP in each of the following files
    - `docker-host/docker-daemon.json`
    - `docker-compose.yml`

3. Run `vagrant up` from inside the `docker-host` directory.

2. From inside the root `FaaS` directory, run
    ```terminal
    $ docker-compose build
    $ docker-compose up
    ```

3. There will be 3 APIs up and running
    - _Allocator_ at [`http://localhost:6060/docs`](http://localhost:6060/docs)
    - _Controller_ at [`http://localhost:7070/docs`](http://localhost:7070/docs)
    - _Filer_ at [`http://localhost:8080/docs`](http://localhost:8080/docs)

4. Using the application
    - Use _Filer_ to upload the function payloads, such as `hello-world.zip` and `get-ip.zip`.
    - Use _Controller_ to upload the function, note the `id`. You'll have to mention the function entry point, e.g. for `get-ip.zip` it's `app.ip`.
    - Use _Allocator_ to run the function using its `id`.
