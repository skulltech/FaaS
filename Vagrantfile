Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/focal64"
  config.vm.define "docker-host"
  # config.vm.network "forwarded_port", guest: 5000, host: 5000
  config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

  config.vm.provider "virtualbox" do |vb|
    vb.memory = 2048
    vb.cpus = 2
  end

  config.vm.provision "shell", inline: <<-SHELL
    wget -qO- https://get.docker.com/ | sh
    mkdir /etc/systemd/system/docker.service.d
    echo "[Service]" >> /etc/systemd/system/docker.service.d/override.conf
    echo "ExecStart=" >> /etc/systemd/system/docker.service.d/override.conf
    echo "ExecStart=/usr/bin/dockerd -H fd:// -H tcp://0.0.0.0:2375 --containerd=/run/containerd/containerd.sock" >> /etc/systemd/system/docker.service.d/override.conf
    systemctl daemon-reload
    systemctl restart docker.service
  SHELL
end
