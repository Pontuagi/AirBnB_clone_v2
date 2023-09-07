#!/usr/bin/python3
"""
A Fabric script that distributes an archive to web servers using do_deploy.
"""

from fabric.api import env, put, run
import os

env.hosts = ['100.26.136.11', '54.236.190.242']


def do_deploy(archive_path):
    """
    Distributes an archive to web servers.
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ directory of the web server
        put(archive_path, "/tmp/")

        # Extract the archive to without extension>
        archive_name = os.path.basename(archive_path)
        release_dir = "/data/web_static/releases/{}".format(
            archive_name.split(".")[0]
        )
        run("mkdir -p {}".format(release_dir))
        run("tar -xzf /tmp/{} -C {}".format(archive_name, release_dir))

        # Delete the archive from the web server
        run("rm /tmp/{}".format(archive_name))

        # Remove the old symbolic link
        current_link = "/data/web_static/current"
        run("rm -f {}".format(current_link))

        # Create a new symbolic link to the new version of your code
        run("ln -s {} {}".format(release_dir, current_link))

        return True
    except Exception:
        return False
