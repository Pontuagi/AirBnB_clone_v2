#!/usr/bin/python3
"""
A Fabric script (based on the file 1-pack_web_static.py)
that distributes an archive to your web servers, using the function do_deploy:
"""

from fabric import Connection
import os
from datetime import datetime

env.hosts = ["100.26.136.11", "54.236.190.242"]


def do_pack():
    """ 
    Generates a .tgz archive from the contents of the web_static folder
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = "web_static_" + timestamp + ".tgz"
    archive_path = "versions/" + archive_name

    try:
        local("mkdir -p versions")
        local("tar -cvzf {} web_static".format(archive_path))
        return archive_path
    except Exception:
        return None


def do_deploy(archive_path):
    """
    A function to distribute an archive to web servers
    """
    username = "ubuntu"
    remote_dir = "/tmp/"

    if not os.path.exists(archive_path):
        return False

    try:
        with Connection(env.hosts[0], user=username) as c:
            # Upload the archive to the /tmp/ directory on the web server.
            c.put(archive_path, remote=remote_dir)
            # Extract the filename without extension from the archive_path.
            archive_filename = os.path.basename(archive_path)
            directory_name = os.path.splitext(archive_filename)[0]
            # Define the target directory where the archive will be extracted.
            target_directory = f'/data/web_static/releases/{directory_name}'

            # Create the target directory if it doesn't exist.
            c.run(f'mkdir -p {target_directory}')

            # Uncompress the archive to the target directory.
            c.run(f'tar - xzvf {os.path.join(remote_dir, archive_filename)} \
                  -C {target_directory}')

            # Delete the archive file on the remote server.
            c.run(f'rm {os.path.join(remote_dir, archive_filename)}')

            # Delete the symbolic link /data/web_static/current if it exists.
            c.run(f'rm -f /data/web_static/current')

            # Create a new symbolic link linked to the new version of the code.
            c.sudo(f'ln -s {target_directory} /data/web_static/current')
    except Exception as e:
        print(f"Error: {e}")
        return False

    return True


if __name__ == "__main__":
    archive_path = do_pack()
    if archive_path:
        result = do_deploy(archive_path)
        if result:
            print("Deployment successful.")
        else:
            print("Deployment failed.")
