VAGRANTFILE_API_VERSION = "2"
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|


   config.vm.define "pxc_slave_node" do |pxc_slave_node|
        pxc_slave_node.vm.box = "geerlingguy/ubuntu2004"
        pxc_slave_node.ssh.insert_key = false
        pxc_slave_node.vm.hostname = "slave"
        pxc_slave_node.vm.network "private_network", ip: "192.168.56.18", netmask: "255.255.255.0"


        pxc_slave_node.vm.provision "ansible" do |ansible|
       ansible.playbook="slave.yml"
       end


   end


    config.vm.define "pxc_master_node" do |pxc_master_node|
        pxc_master_node.vm.box = "geerlingguy/ubuntu2004"
        pxc_master_node.ssh.insert_key = false
        pxc_master_node.vm.hostname = "master"
        pxc_master_node.vm.network "private_network", ip: "192.168.56.17", netmask: "255.255.255.0"


       
       pxc_master_node.vm.provision "ansible" do |ansible|
       ansible.playbook="master.yml"
       end

   end       
end
