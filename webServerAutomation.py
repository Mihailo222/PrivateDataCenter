import os

#***********************Variables*************************************************
#*******************(EDIT THESE PARAMETERS)***************************************
wsOne_ipv4 = "WORDPRESS SERVER1 IP ADDRESS"
wsTwo_ipv4 = "WORDPRESS SERVER2 IP ADDRESS"
wsOne_ipv4_key = "192.168.56.15"
wsTwo_ipv4_key = "192.168.56.16"
dns_ipv4 = "192.168.56.14"
domain = "NEW DOMAIN"
key_domain = "domain.ca"
siteOne_wp_conf_folder_key="WordpressOne"
siteTwo_wp_conf_folder_key="wordpressTwo"
siteOne_wp_conf_folder="NEW FOLDER NAME FOR WORDPRESS ONE"
siteTwo_wp_conf_folder= "NEW FOLDER NAME FOR WORDPRESS TWO"
subdomain_one_key = "webSiteOne"
subdomain_one_val = "NEW SUBDOMAIN ONE"
subdomain_two_key = "webSiteTwo"
subdomain_two_val = "NEW SUBDOMAIN TWO"
#***********************DB Variables***************************************************
#host one in percona cluster
db_name1=''
db_user1=''
db_password1=''

#host two in percona cluster
db_name2=''
db_user2=''
db_password2=''

#cluster ip address
cluster_ipv4='192.168.56.25'

#**************************************************************************************

def edit_nameserver_file(dns_ipv4):
    with open("wp_server/nameserver/resolv.conf","w") as file:
        file.write("nameserver %s" %(dns_ipv4))

def edit_wsconfig(ws_ipv4,wsOne_ipv4_key,domain, key_domain,subdomain_one_key,subdomain_one_val,siteOne_wp_conf_folder_key,siteOne_wp_conf_folder):
    with open("wp_server/%s/%s.conf" %(siteOne_wp_conf_folder_key,siteOne_wp_conf_folder_key),"r") as file:
        lines = file.readlines()
    with open("wp_server/%s/%s.conf" %(siteOne_wp_conf_folder_key,siteOne_wp_conf_folder_key),"w") as file:
        for line in lines:
            if wsOne_ipv4_key in line:
                file.write('<VirtualHost %s:80> \n' % (ws_ipv4))
            elif "%s.%s" % (subdomain_one_key,key_domain) in line:
                file.write('ServerName %s.%s\n' %(subdomain_one_val,domain))
            elif "DocumentRoot" in line:
                file.write(" DocumentRoot /srv/www/%s\n"%(siteOne_wp_conf_folder))
            elif "<Directory /srv/www/%s>"%(siteOne_wp_conf_folder_key) in line:
                file.write(" <Directory /srv/www/%s>\n"%(siteOne_wp_conf_folder))
            elif "<Directory /srv/www/%s/wp-content>"%(siteOne_wp_conf_folder_key) in line:
                file.write('<Directory /srv/www/%s/wp-content>\n'%(siteOne_wp_conf_folder))
            else:
                file.write(line)


def edit_wp_file(dbname, dbuser, dbpass,cluster_ip,site_wp_conf_folder):
    with open("wp_server/%s/wp-config.php" % (site_wp_conf_folder),"r") as file:
        lines = file.readlines()
    with open("wp_server/%s/wp-config.php" % (site_wp_conf_folder),"w") as file:
        for line in lines:
            if 'DB_NAME' in line:
                file.write("define( 'DB_NAME', '%s' );\n" %(dbname))
            elif 'DB_USER' in line:
                file.write("define( 'DB_USER', '%s' );\n" %(dbuser))
            elif 'DB_PASSWORD' in line:
                file.write("define( 'DB_PASSWORD', '%s' );\n" %(dbpass))
            elif 'DB_HOST' in line:
                file.write("define( 'DB_HOST', '%s' );\n" %(cluster_ip))
            else:
                file.write(line)


def edit_vars_file(siteOne_wp_conf_folder, siteTwo_wp_conf_folder):
    with open("wp_server/vars.yml","r") as file:
        lines = file.readlines()
    with open("wp_server/vars.yml","w") as file:
        for line in lines:
            if "site_one_subdomain" in line:
                file.write(" site_one_subdomain: %s\n"%(siteOne_wp_conf_folder))
            elif "site_two_subdomain" in line:
                file.write(" site_two_subdomain: %s\n"%(siteTwo_wp_conf_folder))
            else:
                file.write(line)

def edit_db_vars_file(ws_ip_one, ws_ip_two):
    with open("slave/vars.yml","r") as file:
        lines = file.readlines()

    with open("slave/vars.yml","w") as file:
        for line in lines:
            if "remote_ip_one:" in line:
                file.write(" remote_ip_one: %s #ip web servera1\n", ws_ip_one)
            elif "remote_ip_two:" in line:
                file.write(" remote_ip_two: %s #ip web servera1\n", ws_ip_two)
            else:
                file.write(line)            

def edit_inventory(ws1_ip, ws2_ip):
    with open("inventory","r") as file:
        lines = file.readlines()
    with open("inventory","w") as file:
        for line in lines:
            if ws1_ip in line:
                file.write(ws1_ip+'\n')
            elif ws2_ip in line:
                file.write(ws2_ip+'\n')
            else:
                file.write(line)




def edit_web_server_configuration():
    edit_nameserver_file(dns_ipv4)
    edit_wsconfig(wsOne_ipv4,wsOne_ipv4_key,domain, key_domain,subdomain_one_key,subdomain_one_val,siteOne_wp_conf_folder_key,siteOne_wp_conf_folder)
    edit_wsconfig(wsOne_ipv4,wsOne_ipv4_key,domain, key_domain,subdomain_two_key,subdomain_two_val,siteTwo_wp_conf_folder_key,siteTwo_wp_conf_folder)

    os.rename(siteOne_wp_conf_folder_key,siteOne_wp_conf_folder) #rename folder 1
    os.rename(siteTwo_wp_conf_folder_key,siteTwo_wp_conf_folder) #rename folder 2
    os.rename("wp_server/%s/%s.conf" %(siteOne_wp_conf_folder,siteOne_wp_conf_folder_key), "wp_server/%s/%s.conf"%(siteOne_wp_conf_folder,siteOne_wp_conf_folder) ) #rename file 1
    os.rename("wp_server/%s/%s.conf" %(siteTwo_wp_conf_folder,siteTwo_wp_conf_folder_key), "wp_server/%s/%s.conf"%(siteTwo_wp_conf_folder,siteTwo_wp_conf_folder) ) #rename file 2

    edit_wp_file(db_name1, db_user1, db_password1,cluster_ipv4,siteOne_wp_conf_folder)
    edit_wp_file(db_name2, db_user2, db_password2,cluster_ipv4,siteTwo_wp_conf_folder)

    edit_vars_file(siteOne_wp_conf_folder,siteTwo_wp_conf_folder)

    #edit WS1 ip address in Vagrantfile
    with open("Vagrantfile","r") as file:
        lines = file.readlines()
    with open("Vagrantfile","w") as file:
        for line in lines:
            if wsOne_ipv4_key in line:
                file.write('    wp_server_one.vm.network "private_network", ip: "%s", netmask: "255.255.255.0"\n' %(wsOne_ipv4))
            elif wsTwo_ipv4_key in line:
                file.write('    wp_server_two.vm.network "private_network", ip: "%s", netmask: "255.255.255.0"\n' %(wsTwo_ipv4))            
            else:
                file.write(line)

    edit_db_vars_file(wsOne_ipv4,wsTwo_ipv4)
    edit_inventory(wsOne_ipv4_key,wsTwo_ipv4_key)
    



edit_web_server_configuration()