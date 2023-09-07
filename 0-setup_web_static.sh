#!/usr/bin/env bash
# a Bash script that sets up my web servers for the deployment of web_static.

# Install Nginx if not already installed
if ! dpkg -l | grep -q "nginx"; then
	sudo apt-get update
	sudo apt install -y nginx
	sudo systemctl start nginx
	sudo systemctl enable nginx
	echo "Nginx Installed"
fi

data_folder="/data/"
# Create /data/ if it !exists
if [ ! -d "$data_folder" ]; then
	sudo mkdir -p "$data_folder"
	echo "/data/ directory created"
fi

web_static_folder="/data/web_static/"
# Create the folder /data/web_static/ if it !exist
if [ ! -d "$web_static_folder" ]; then
	sudo mkdir -p "$web_static_folder"
	echo "/data/web_static/ directoy created"
fi

web_static_rel_dir="/data/web_static/releases/"
# Create the folder /data/web_static/releases/ if it !exist
if [ ! -d "$web_static_rel_dir" ]; then
	sudo mkdir -p "$web_static_rel_dir"
	echo "/data/web_static/releases/ directory created"
fi

web_static_shared="/data/web_static/shared/"
# Create the folder /data/web_static/shared/ if it !exist
if [ ! -d "$web_static_shared" ]; then
	sudo mkdir -p "$web_static_shared"
	echo "/data/web_static/shared/ directory created"
fi

# Create the folder /data/web_static/releases/test/ if it doesn’t already exist
if [ ! -d "/data/web_static/releases/test/" ]; then
	sudo mkdir -p "/data/web_static/releases/test/"
	echo "/data/web_static/releases/test/ directory created"
fi

# create a fake HTML file with simple content
html_file="/data/web_static/releases/test/index.html"
sudo mkdir -p '$(dirname "$html_file")'
echo "<html>
	<head>
		<title> **Test Page** </title>
	</head>
	<body>
		<h1> Hello, It mr Pontuagi!</h1>
	</body>
     </html>" | sudo tee "$html_file" > /dev/null

echo "test HTML file created"

# create a symbolic link /data/web_static/current
# linked to the /data/web_static/releases/test/ folder

symbolic_link="/data/web_static/current"
target_dir="/data/web_static/releases/test/"

# remove existing symbolic link if it exists
if [ -L "$symbolic_link" ]; then
	sudo rm "$symbolic_link"
fi


# Create a new symbolic_link
sudo ln -s "$target_dir" "$symbolic_link"

echo "symbolic link created"

# Give ownership of the /data/ folder to the ubuntu user AND group
user="ubuntu"
group="ubuntu"
sudo chown -R "$user:$group" "/data/"

nginx_config="/etc/nginx/sites-available/default"
alias_config="location /hbnb_static/ {
	alias /data/web_static/current/;
	index index.html;
	}"
sudo sed -i "s|location / {|location / { $alias_config|g" "$nginx_config"
if sudo nginx -t; then
    sudo systemctl restart nginx
    echo "Nginx configuration updated and Nginx restarted."
else
    echo "Nginx configuration test failed. Please check your configuration."
fi
