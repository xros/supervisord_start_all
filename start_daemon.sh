#!/bin/bash
# This script is used to start supervisor daemon after server's rebooting
# Diagram as the followings:
# 1) find the directory of of 'tornado' app
# 2) change directroy into the app's path
# 3) start the supervisord daemon with "$~ supervisord -c demo.conf"
# 4) start the app using supervisorctl "$~ supervisorctl -c demo.conf start all"
# {NOTICE} : This script should be in the same folder of those 'tornado' apps
#find ./ -type d -maxdepth 1 -name "*supervisor*" 2>/dev/null | xargs supervisord -c -/demo.conf && supervisorctl -c -/demo.conf start all

# The current absolute path
#path=`dirname $0`

# Kill all the daemons before restarting/starting
#pid=$(netstat -npl | grep supervisor.sock | awk '{print $9}'| cut -d "/" -f1 | xargs echo)
#for p in $pid;do
#    kill $p
#done
# ## the string/array to store the file
#folders=$(find $path -type d -maxdepth 1 -name "*supervisor*" 2>/dev/null | xargs echo);
##echo $folders
#for i in $folders;do
#    file=$(find $i -type f -maxdepth 1 -name "*.conf" 2>/dev/null | xargs echo);
#    # start the daemon
#    current_time=`date "+%Y-%m-%d %H:%M:%S"`
#    echo "[* Starting project $current_time ]: "$i
#    supervisord -c $file #2&>/dev/null
#    current_time=`date "+%Y-%m-%d %H:%M:%S"`
#    echo "[* Starting its app $current_time ]: "$file
#    #supervisorctl -c $file stop all
#    supervisorctl -c $file start all
#done
#

# [New version]
#supervisorctl -c daemon.conf reload 2&>/dev/null
current_time=`date "+%Y-%m-%d %H:%M:%S"`
echo "[ Stopping previous 'supervisord' daemon if any $current_time ]"
supervisorctl -c daemon.conf shutdown 2&>/dev/null
current_time=`date "+%Y-%m-%d %H:%M:%S"`
echo "[ Starting 'supervisord' daemon $current_time ]"
supervisord -c daemon.conf
current_time=`date "+%Y-%m-%d %H:%M:%S"`
echo "[ Starting all apps using 'supervisorctl' $current_time ]"
supervisorctl -c daemon.conf start all
