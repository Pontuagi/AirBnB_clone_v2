#!/usr/bin/env bash
#Bash script that sets up your web servers for the deployment of web_static

#Nginx Installation
sudo apt-get update
sudo apt-get -y install nginx
sudo ufw allow 'Nginx HTTP'

#Creates folders and files if it doesn't exist
sudo mkdir -p /data/
sudo mkdir -p /data/web_static/
sudo mkdir -p /data/web_static/releases/
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/
sudo touch /data/web_static/releases/test/index.html
sudo echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo /data/web_static/releases/test/index.html

#Creates symbolic link
sudo ln -s -f /data/web_static/releases/test/ /data/web_static/current

#Gives ownership of the /data/ folder to the ubuntu user AND group
sudo chown -R ubuntu:ubuntu /data/

#Updates Nginx configuration
sudo sed -i '/listen 80 default_server/a location /hbnb_static { alias /data/web_static/current/;}' /etc/nginx/sites-enabled/default

#Restarts Nginx after configuration
sudo service nginx restart
