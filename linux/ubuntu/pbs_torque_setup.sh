#!/bin/bash

# script adapted from Johann A. Briffa's blog, setup torque pbs job scheduler on Ubuntu 14.04 LTS
# NB. execute as root

apt-get install torque-server torque-client torque-mom -y

/etc/init.d/torque-mom stop
/etc/init.d/torque-scheduler stop
/etc/init.d/torque-server stop

pbs_server -t create # answer y here

killall pbs_server

SERVER=localhost # SERVER.DOMAIN, only SERVER for localhost
SERVER_ONLY=localhost
NCPU=20 # number of cores

echo $SERVER > /etc/torque/server_name
echo $SERVER > /var/spool/torque/server_priv/acl_svr/acl_hosts
echo root@$SERVER > /var/spool/torque/server_priv/acl_svr/operators
echo root@$SERVER > /var/spool/torque/server_priv/acl_svr/managers

# add compute node
echo "$SERVER np=$NCPU" > /var/spool/torque/server_priv/nodes

# tell compute node handler which server to contact
echo $SERVER > /var/spool/torque/mom_priv/config

/etc/init.d/torque-server start
/etc/init.d/torque-scheduler start
/etc/init.d/torque-mom start

# set scheduling properties
qmgr -c 'set server scheduling = true'
qmgr -c 'set server keep_completed = 300'
qmgr -c 'set server mom_job_sync = true'

# create default queue
qmgr -c 'create queue batch'
qmgr -c 'set queue batch queue_type = execution'
qmgr -c 'set queue batch started = true'
qmgr -c 'set queue batch enabled = true'
qmgr -c 'set queue batch resources_default.walltime = 1:00:00'
qmgr -c 'set queue batch resources_default.nodes = 1'
qmgr -c 'set server default_queue = batch'

# configure submission pool
qmgr -c "set server submit_hosts = $SERVER_ONLY"
qmgr -c 'set server allow_node_submit = true'

# now try qsub -I and qstat


