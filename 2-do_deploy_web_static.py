#!/usr/bin/python3
"""
A Fabric script (based on the file 1-pack_web_static.py)
that distributes an archive to your web servers, using the function do_deploy:
"""

from fabric import Connection
import os
from datetime import datetime

env.hosts = ["100.26.136.11", "54.236.190.242"]
env.user = "ubuntu"


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
        for host in env.hosts:
            with Connection(host, user=username) as c:
                # Upload the archive to the /tmp/ directory on the web server.
                c.put(archive_path, remote=remote_dir)
                # Extract the filename without extension from the archive_path.
                directory_name = archive_path[9:]
                # Define the target directory where archive will be extracted.
                target_directory = '/data/web_static/releases/{}'.format(directory_name[:-4])

                # Create the target directory if it doesn't exist.
                c.run(f'sudo mkdir -p {target_directory}')

                # Uncompress the archive to the target directory.
                c.run(f'sudo tar -xzf {directory_name} -C {target_directory}')

                # Delete the archive file on the remote server.
                c.run(f'sudo rm {os.path.join(remote_dir, archive_filename)}')

                symbolic_link_path = "/data/web_static/current"

                # Delete the symbolic link if it exists.
                if c.run(
                    f'sudo test -L {symbolic_link_path}',
                    warn=True,
                    hide=True
                ).ok:
                    c.run(f'sudo rm {symbolic_link_path}')

                # Create a new symbolic link linked to new version of the code.
                c.run(f'sudo ln -s {target_directory} {symbolic_link_path}')
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
