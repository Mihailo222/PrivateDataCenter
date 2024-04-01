VAGRANTFILE_API_VERSION = "2"
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
   
   #db slave node 
   config.vm.define "pxc_slave_node" do |pxc_slave_node| #config.vm.define <-> inventory file (Vagrant-Ansible communication)
    pxc_slave_node.vm.box = "geerlingguy/ubuntu2004"
    pxc_slave_node.ssh.insert_key = false
    pxc_slave_node.vm.hostname = "slave"
    pxc_slave_node.vm.network "private_network", ip: "192.168.56.18", netmask: "255.255.255.0"

    pxc_slave_node.vm.provision "ansible" do |ansible|
      ansible.playbook="slave.yml"
    end
   end
  
   #db master node
   config.vm.define "pxc_master_node" do |pxc_master_node|
    pxc_master_node.vm.box = "geerlingguy/ubuntu2004"
    pxc_master_node.ssh.insert_key = false
    pxc_master_node.vm.hostname = "master"
    pxc_master_node.vm.network "private_network", ip: "192.168.56.17", netmask: "255.255.255.0"
   
    pxc_master_node.vm.provision "ansible" do |ansible|
     ansible.playbook="master.yml"
    end
   end

   #dns
   config.vm.define "dns_server" do |dns_server|
    dns_server.vm.box = "geerlingguy/ubuntu2004"
    dns_server.ssh.insert_key = false
    dns_server.vm.hostname = "dns"
    dns_server.vm.network "private_network", ip: "192.168.56.14", netmask: "255.255.255.0"

    dns_server.vm.provision "ansible" do |ansible|
     ansible.playbook="dns.yml"
    end
   end

   #wordpress1
   config.vm.define "wp_server_one" do |wp_server_one|
    wp_server_one.vm.box = "geerlingguy/ubuntu2004"
    wp_server_one.ssh.insert_key = false
    wp_server_one.vm.hostname = "wpOne"
    wp_server_one.vm.network "private_network", ip: "192.168.56.15", netmask: "255.255.255.0"
     
    wp_server_one.vm.provision "ansible" do |ansible|
     ansible.playbook="wpOne.yml"
    end
   end

     #wordpress2
   config.vm.define "wp_server_two" do |wp_server_two|
    wp_server_two.vm.box = "geerlingguy/ubuntu2004"
    wp_server_two.ssh.insert_key = false
    wp_server_two.vm.hostname = "wpTwo"
    wp_server_two.vm.network "private_network", ip: "192.168.56.16", netmask: "255.255.255.0"

    wp_server_two.vm.provision "ansible" do |ansible|
     ansible.playbook="wpTwo.yml"
    end
   end

end
