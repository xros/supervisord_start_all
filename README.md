Hello
=====
Structure
-----
* Structure as the followings. 
* Three main things: 1) start_daemon.sh 2) project "supervisord_init 3) project "supervisord_init2
* In every project, there will be two useful things, as for this instance: (1) demo.conf (2) demo.py
* Those *log, *.pid, *.sock files are invoked/generated after 'supervisord/supervisorctl' running
    
>.    
>├── start_daemon.sh    
>├── supervisord_init    
>│   ├── demo.conf    
>│   '── demo.py    
>└── supervisord_init2    
>       ├── demo.conf    
>       '── demo.py    
>    
****

# Tips: #
* There is a sentence could be added into file ```/etc/rc.local```:  ```/bin/bash /home/path/to/start_daemon.sh  >>/var/log/start_daemon.log```
* In this way every time when the serving boots, the services handled/managed by the supervisord daemon will be auto-started.

#### Have Fun ####

