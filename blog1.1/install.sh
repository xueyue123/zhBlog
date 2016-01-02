#!/bin/bash

#to build some soft
sudo apt-get install gcc g++ make -y

#create virtual env
sudo apt-get install python-virtualenv -y
sudo easy_install virtualenvwrapper
mkdir $HOME/.virtualenvs
echo "export WORKON_HOME=$HOME/.virtualenvs" >> $HOME/.bashrc
echo "source /usr/local/bin/virtualenvwrapper.sh" >> $HOME/.bashrc
source $HOME/.bashrc
mkvirtualenv blog

#virtual develop enviroment 
sudo apt-get install mysql-server mysql-common python-dev libmysqlclient-dev -y
workon blog;
pip install --upgrade pip

pip install Django==1.7.8
pip install ipdb==0.8.1
pip install ipython==3.2.0
pip install MySQL-python==1.2.5
pip install Pillow==2.8.2
pip install wheel==0.24.0
pip install uWSGI==2.0.11.2


#install nginx
cd ./soft
tar xvf pcre-8.37.tar.gz
cd pcre-8.37/
./configure &&make&&sudo make install
cd ../
rm pcre-8.37 -rf

printf "pcre installed\n";

tar xvf openssl-1.0.0r.tar.gz
cd openssl-1.0.0r/
./config &&make &&sudo make install
cd ../
rm openssl-1.0.0r -rf

tar xvf nginx-1.6.2.tar.gz
cd nginx-1.6.2/
./configure &&make &&sudo make install
cd ../
rm nginx-1.6.2 -rf
cd ../

#link pcre to /lib/libpcre.so.1
sudo ln -s /usr/local/lib/libpcre.so.1 /lib/libpcre.so.1

#config nginx.conf
sudo cp ./config/nginx.conf /usr/local/nginx/conf/nginx.conf

#start nginx
sudo /usr/local/nginx/sbin/nginx

#static resource
sudo mkdir /var/static -p
sudo chmod 777 /var/static 
python manage.py collectstatic

#start uwsgi --zhblog
uwsgi --ini project.ini &

#over
printf "\nfinish install nginx! Good Luck!\n";
printf "\nPlease add \"/usr/local/nginx/sbin/nginx\" to /etc/rc.local \n";

