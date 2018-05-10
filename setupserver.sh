#!/bin/sh

#Setup Drives


sudo yum install -y xfsprogs
sudo umount /dev/xvdb
sudo mkfs.xfs /dev/xvdb
sudo mkdir /data
sudo mount /dev/xvdb /data


#Setup Server with MySQL
sudo blockdev --setra 0 /dev/xvdb
echo never | sudo tee  /sys/kernel/mm/transparent_hugepage/enabled
echo never | sudo tee  /sys/kernel/mm/transparent_hugepage/defrag

echo '* soft nofile 20000' | sudo tee /etc/security/limits.conf
echo '* hard nofile 20000'| sudo tee --append /etc/security/limits.conf

sudo yum install -y sysstat

sudo yum install -y mysql
sudo yum install -y mysql-server

sudo mkdir /data/mysql 
sudo chown mysql:mysql /data/mysql 

sudo sed -i 's#datadir=/var/lib/mysql#datadir=/data/mysql\nbind-address=127.0.0.1#' /etc/my.cnf

sudo service mysqld start
#No security but bound to localhost only.

#Install MongoDB 3.6 from Repository
REPOFILE="/etc/yum.repos.d/mongodb-enterprise.repo"
echo "[mongodb-enterprise]" | sudo tee $REPOFILE
echo "name=MongoDB Enterprise Repository"  | sudo tee --append $REPOFILE
echo "baseurl=https://repo.mongodb.com/yum/amazon/2013.03/mongodb-enterprise/3.6/x86_64/" | sudo tee --append  $REPOFILE
echo "gpgcheck=1" | sudo tee --append  $REPOFILE
echo "enabled=1" | sudo tee --append $REPOFILE
echo "gpgkey=https://www.mongodb.org/static/pgp/server-3.6.asc" | sudo tee --append $REPOFILE

sudo yum install -y mongodb-enterprise

sudo mkdir /data/mongodb 
sudo chown mongod:mongod /data/mongodb
sudo sed -i 's#dbPath:/var/lib/mongo#dbPath: /data/mongodb#' /etc/mongod.conf

sudo service mongod start

MDB


