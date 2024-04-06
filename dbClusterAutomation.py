#***********************Variables*************************************************
#*******************(EDIT THESE PARAMETERS)***************************************

dns_ipv4 = ""

percona_master_ipv4_key = "192.168.56.17"
percona_slave_ipv4_key = "192.168.56.18"
percona_master_ipv4_val = ""
percona_slave_ipv4_val = ""
virtual_ip_key = "192.168.56.25/24"
virtual_ip_val = ""

folderMaster = "master" 
folderSlave = "slave"

auth_pass = ""

cluster_name = ""

percona_master_name = ""
percona_slave_name = ""

wp_db_username1 = ""
wp_db_username2 = ""
wp_pass1 = ""
wp_pass2 = ""
db1_name = ""
db2_name = ""

#********************************************************************************

def edit_nameserver(dns_ip, folder):
    with open("%s/nameserver/resolv.conf"%(folder),"w") as file:
        file.write("nameserver %s"%(dns_ip))
def edit_mysqld_file(this_ip, other_ip, this_node_name, cluster_name, folder):
    with open("%s/mysqld.cnf" % (folder),"r") as file:
        lines = file.readlines()
        print(lines)
    with open("%s/mysqld.cnf" % (folder),"w") as file:
        for line in lines:
            if "wsrep_cluster_address" in line:
                file.write("wsrep_cluster_address=gcomm://%s,%s\n"%(this_ip, other_ip))
            elif "wsrep_node_address" in line:
                file.write("wsrep_node_address=%s\n"%(this_ip))
            elif "wsrep_cluster_name" in line:
                file.write("wsrep_cluster_name=%s\n" %(cluster_name))
            elif "wsrep_node_name=" in line:
                file.write("wsrep_node_name=%s\n"%(this_node_name))
            else:
                file.write(line)
def edit_keepalive_file(host_ip, another_ip_val, another_ip_key, virtual_ip_key, virtual_ip_val, passwd, folder):
    with open("%s/keepalive/keepalived.conf" %(folder),"r") as file:
        lines = file.readlines()
    with open("%s/keepalive/keepalived.conf" %(folder),"w") as file:
        for line in lines:
            if "unicast_src_ip" in line:
                file.write("unicast_src_ip %s\n" %(host_ip))
            elif "auth_pass" in line:
                file.write("auth_pass %s\n" %(passwd))
            elif another_ip_key in line:
                file.write(another_ip_val+"\n")
            elif virtual_ip_key in line:
                file.write(virtual_ip_val+"\n") 
            else:
                file.write(line)
def edit_vars_file(wp_db_usr1, wp_db_usr2,wp_usr1_pass,wp_usr2_pass, master_ip, db1_name, db2_name):
    with open("slave/vars.yml","r") as file:
        lines = file.readlines()
    with open("slave/vars.yml","w") as file:
        for line in lines:
            if "remote_user_uname_one" in line:
                file.write(" remote_user_uname_one: %s\n"%(wp_db_usr1))
            elif "remote_user_uname_two" in line:
                file.write(" remote_user_uname_two: %s\n"%(wp_db_usr2))
            elif "remote_user_one_password:" in line:
                file.write(" remote_user_one_password: %s\n"%(wp_usr1_pass))
            elif "remote_user_two_password:" in line:
                file.write(" remote_user_two_password: %s\n"%(wp_usr2_pass))
            elif "master_ip:" in line:
                file.write(" master_ip: %s"%(master_ip))
            elif "db1_name:" in line:
                file.write(" db1_name: %s\n"%(db1_name))
            elif "db2_name:" in line:
                file.write(" db2_name: %s\n"%(db2_name))
            else:
                file.write(line)
def edit_vagrantfile(master_ip, slave_ip):
    with open("Vagrantfile","r") as file:
        lines = file.readlines()
    with open("Vagrantfile","w") as file:
        for line in lines:
            if 'pxc_master_node.vm.network' in line:
                file.write('    pxc_master_node.vm.network "private_network", ip: "%s", netmask: "255.255.255.0"'%(master_ip)) 
            elif 'pxc_slave_node.vm.network' in line:
                file.write('    pxc_slave_node.vm.network "private_network", ip: "%s", netmask: "255.255.255.0"'%(slave_ip))
            else:
                file.write(line) 
#**********************************************************************************



def edit_db_files():
    #editing percona master files
    edit_nameserver(dns_ipv4, folderMaster)
    edit_mysqld_file(percona_master_ipv4_val,percona_slave_ipv4_val,percona_master_name,cluster_name,folderMaster)
    edit_keepalive_file(percona_master_ipv4_val,percona_slave_ipv4_val,percona_slave_ipv4_key,virtual_ip_key,virtual_ip_val,auth_pass,folderMaster)
    #editing percona slave files
    edit_nameserver(dns_ipv4,folderSlave)
    edit_mysqld_file(percona_slave_ipv4_val,percona_master_ipv4_val,percona_slave_name,cluster_name,folderSlave)
    edit_keepalive_file(percona_slave_ipv4_val,percona_master_ipv4_val,percona_master_ipv4_key,virtual_ip_key,virtual_ip_val,auth_pass,folderSlave)
    #edit vars file
    edit_vars_file(wp_db_username1,wp_db_username2,wp_pass1,wp_pass2,percona_master_ipv4_val,db1_name, db2_name)
    #edit Vagrantfile
    edit_vagrantfile(percona_master_ipv4_val,percona_slave_ipv4_val)


edit_db_files()