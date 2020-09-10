#!/bin/bash
CONTAINER="authark"
PLAYBOOK="setup/deploy.yml"
REPOSITORY="https://github.com/knowark/authark.git"
REPOSITORY_PATH=$PWD

echo "Deploying LXD container..."

lxc launch ubuntu:20.04 $CONTAINER
lxc config device add $CONTAINER home disk source=$HOME path=/mnt/$HOME

echo "Install Ansible..."

sleep 5  # Wait for container network connectivity.
lxc exec $CONTAINER -- apt update -y
lxc exec $CONTAINER -- apt install ansible -y
lxc exec $CONTAINER -- apt autoremove -y

echo "Deploy with Ansible..."

lxc exec $CONTAINER -- mkdir /var/git
lxc exec $CONTAINER -- ln -s /mnt/$REPOSITORY_PATH /var/git/$CONTAINER
lxc exec $CONTAINER -- bash -c "ansible-playbook -c local -i localhost, \
    /var/git/$CONTAINER/$PLAYBOOK 2>&1 | tee deploy.log"
