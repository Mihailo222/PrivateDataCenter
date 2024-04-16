<h1>Private Data Center</h1>


![Screenshot (1437)](https://github.com/Mihailo222/PrivateDataCenter/assets/92820769/b2275bb9-3750-4acd-874a-479711f236e7)
 Project simulates a data center containing five virtual machines running Ubuntu22.04 Linux distribution. The setup includes DNS server, two web servers and two servers that represent a database cluster. <br> 
 
 **DNS server** is configured with bind9 service, where I achieved translation of IP addresses to a domain names for two web sites that are hosted on a same web server. DNS server contains a zones configured for both web sites. <br>
 
 On **web servers** I  configured Apache2 Virtual Hosting service. Virtual hosting is a solution for hosting multiple web sites on a same server, what I achieved. At the application layer I installed **WordPress software** and configured WordPress admins for both web sites. WordPress web sites are connected with database cluster with **MySQL client**. <br>
 
 For a database I chose to configure **Percona Xtradb Cluster** - High Availability Solution for MySQL. What I achieved here is  master and slave server synchronized to work as one. The entire cluster has a virtual IP address that is configured with keepalived service. Communication between servers in a cluster is encrypted. <br>
 
 So, why we need two web servers? My plan is  to make a web application that moves whole configuration from one server to another if one server is attacked. This is left for future implementation. The entire configuration is automated with python scripts, so if there is a need for changing some basic parameters as domain name, IP address, database name etc. I don’t need to do it in every single file manually. 
