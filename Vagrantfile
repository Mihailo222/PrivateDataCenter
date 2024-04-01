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

end
