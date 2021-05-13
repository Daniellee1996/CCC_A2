#!/bin/bash

. ./unimelb-comp90024-2021-grp-44-openrc.sh; ansible-playbook  mrc.yaml -i host_vars/application_hosts.ini