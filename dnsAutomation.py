import os

#***********************Variables*************************************************
#*******************(EDIT THESE PARAMETERS)***************************************
domain = "your new domain"
key_domain = "domain.ca"
dns_ipv4 = "new dns IP address"
key_dns_ip="192.168.56.14"
trusted_clients = [ "list of DNS trusted clients"]
ws1_ipv4="IP address - Web Server One"
ws2_ipv4="IP address - Web Server Two"
subdomain_one = "subdomain_one.domain.ca"
subdomain_two = "subdomain_two.domain.ca"
#********************************************************************************

def edit_named_conf_local(key_domain,domain, key_dns_ip, dns_ipv4):

    with open("dns/config/named.conf.local","r") as file:
        lines = file.readlines()
        print(lines) 

    ip1 = key_dns_ip.split('.')
    ip1 = ip1[::-1]
    key ='.'.join(ip1[1:])
    
    ip2 = dns_ipv4.split('.')
    ip2 = ip2[::-1]
    val ='.'.join(ip2[1:])




    with open("dns/config/named.conf.local","w") as file: #ispisuje liniju po liniju kako ja hocu u prazan fajl
        for line in lines:
            if "%s.rev" %(key_domain) in line:
                file.write('file "/etc/bind/%s.rev";' % (domain)+'\n')

            elif "%s.fwd" %(key_domain) in line:
                file.write('file "/etc/bind/%s.fwd";' % (domain)+'\n')

            elif '"%s"' %(key_domain) in line:
                file.write('zone "%s" IN { ' % (domain)+'\n')
            
            elif key_domain in line:
                file.write('zone "%s.in-addr.arpa" IN {' % (val)+'\n')
            
            else:
                file.write(line)
def edit_named_conf_options(dns_ipv4, trusted_clients):

        acl_list = 'acl "trusted_clients" {\n'
        for ip in trusted_clients:
            acl_list+='%s;\n'% (ip)
        acl_list+='};\n'


        with open("dns/config/named.conf.options","r") as file:
            lines = file.readlines()
 

        #first_index_acl_list = lines.index('acl "trusted_clients" {\n')
        last_index_acl_list = lines.index('};\n')


        with open("dns/config/named.conf.options","w") as file:

            file.write(acl_list)

            for line in lines:


                if "listen-on port 53" in line:
                    file.write("\t\t listen-on port 53 {  localhost; %s; };" %(dns_ipv4)+"\n")

                elif  lines.index(line) in range(last_index_acl_list+1):
                    continue

                else:
                    file.write(line)
def edit_resolv_conf(dns_ipv4):
    with open("dns/nameserver_file/resolv.conf","w") as file:
        file.write("nameserver %s" %(dns_ipv4))
def edit_fwd_file(dns_ipv4, ws1_ipv4,domain,subdomain_one, subdomain_two):
    with open("dns/zone_files/%s.fwd" % (domain),"r") as file:
        lines = file.readlines()
    
    with open("dns/zone_files/%s.fwd" %(domain),"w") as file:
        for line in lines:
            if lines.index(line)==0:
                file.write('%s. 1w IN SOA ns1.%s. hostmaster.%s 1 1d 1h 1w 1h\n' %(domain,domain,domain))
            elif lines.index(line)==1:
                file.write('%s. 1w IN NS ns1.%s.\n'%(domain,domain))
            elif lines.index(line)==2:
                file.write('ns1.%s. 1w IN A %s\n' %(domain,dns_ipv4))
            elif lines.index(line)==3:
                file.write('%s.%s. 1w IN A %s\n' % (subdomain_one,domain,ws1_ipv4))
            elif lines.index(line)==4:
                file.write('%s.%s. 1w IN A %s\n' % (subdomain_two,domain,ws1_ipv4))
def edit_rev_file(dns_ipv4, ws1_ipv4,domain,subdomain_one, subdomain_two):

    ip1 = dns_ipv4.split('.')
    ip1 = ip1[::-1]
    ip1 ='.'.join(ip1[1:])
    
    conf="%s.in-addr.arpa. 1w IN SOA ns1.%s. hostmaster.%s 1 1d 1h 1w 1h\n" % (ip1,domain,domain)
    conf+="%s.in-addr.arpa. 1w IN NS ns1.%s.\n" %(ip1,domain)

    dns_ip = dns_ipv4.split('.')
    dns_iprev = '.'.join(dns_ip[::-1])
    
    conf+="%s.in-addr.arpa. 1w IN PTR ns1.%s.\n" %(dns_iprev,domain)
    
    ws1_ip = ws1_ipv4.split('.')
    ws1_iprev = '.'.join(ws1_ip[::-1])

    conf+="%s.in-addr.arpa. 1w IN PTR %s.%s.\n" %(ws1_iprev,subdomain_one,domain)
    conf+="%s.in-addr.arpa. 1w IN PTR %s.%s.\n" %(ws1_iprev,subdomain_two,domain)
   # print(conf)

    with open("dns/zone_files/%s.rev" % (domain),"w") as file:
        file.write(conf)
def edit_vars_file(key_domain,domain):
    with open("dns/vars.yml","r") as file:
        lines = file.readlines()

    with open("dns/vars.yml","w") as file:
        for line in lines:
            if key_domain in line:
                file.write(" second_level_domain: %s\n" %(domain))
            else:
                file.write(line)
def edit_inventory(dns_ip):
    with open("inventory","r") as file:
        lines = file.readlines()
    with open("inventory","w") as file:
        for line in lines:
            if dns_ip in line:
                file.write(dns_ip+'\n')
            else:
                file.write(line)

#**********************************************************************************
def edit_dns_config(key_domain, domain,key_dns_ip,dns_ipv4,ws1_ipv4,subdomain_one,subdomain_two):

    #firstly rename .fwd and .fwd files
    os.rename("dns/zone_files/%s.fwd" %(key_domain),"dns/zone_files/%s.fwd" %(domain))
    os.rename("dns/zone_files/%s.rev" %(key_domain),"dns/zone_files/%s.rev" %(domain))

    #edit DNS ip address in Vagrantfile
    with open("Vagrantfile","r") as file:
        lines = file.readlines()
    with open("Vagrantfile","w") as file:
        for line in lines:
            if key_dns_ip in line:
                file.write('dns_server.vm.network "private_network", ip: "%s", netmask: "255.255.255.0"\n' %(dns_ipv4))
            else:
                file.write(line)




    edit_named_conf_local(key_domain,domain,key_dns_ip,dns_ipv4)
    edit_named_conf_options(dns_ipv4,trusted_clients)
    edit_resolv_conf(dns_ipv4)
    edit_fwd_file(dns_ipv4,ws1_ipv4,domain,subdomain_one,subdomain_two)
    edit_rev_file(dns_ipv4,ws1_ipv4,domain,subdomain_one,subdomain_two)
    edit_vars_file(key_domain,domain)
    edit_inventory(key_dns_ip)







#**********************FUNCTION CALL*************************************************

edit_dns_config(key_domain,domain,key_dns_ip,dns_ipv4,ws1_ipv4,subdomain_one,subdomain_two)


