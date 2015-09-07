###Runner
An extremely useful multi-threaded SSH command runner with sudo support written in Python. I use this for my daily DevOps adventures to manage hosts and even load balancers. Make sure to add runner to your path and turn on execute permissions. 

- Use scripts/runner.py for a non-proxy version. 
- Use scripts/prunner.py for a proxy version, that utilizes an existing tunnel (on port 8081) and sconnect. 

###### Example Non-Sudo Usage
➜  bin git:(master) ✗ runner -c 'id' -r tux -c 'id' -log
INFO - [PARAM SET] - FILTERING ONLY HOSTNAMES MATCHING "tux"
INFO - [PARAM SET] - 1 HOSTS HAVE BEEN SELECTED
INFO - [PARAM SET] - LOGFILE IS /Users/jriedel/.runner/logs/runner.log.2015-09-07.13:46:53
INFO - [PARAM SET] - USER IS tuxninja
INFO - [PARAM SET] - SSH CONNECT TIMEOUT IS 10 SECONDS
INFO - [PARAM SET] - THREADS IS 10
INFO - [PARAM SET] - THREADS TIMEOUT IS 10
INFO - [PARAM SET] - DIVIDER IS 10 CREATING 1 CHUNKS
Please Enter Site Pass: 

INFO - [RESULT] - tuxlabs.com: uid=1000(tuxninja) gid=1000(tuxninja) groups=1000(tuxninja),27(sudo)

INFO - [SUMMARY] - Successfully logged into 1/1 hosts and ran your command(s) in 0:00:05 second(s)

INFO - [LOG] - Your logfile can be viewed @ /Users/jriedel/.runner/logs/runner.log.2015-09-07.13:46:53
➜  bin git:(master) ✗ 

###### Example Sudo Usage + Output Filtering

➜  bin git:(master) ✗ runner -c 'id' -r tux -c 'id' -log -s -lf RESULT,SUMMARY
Please Enter Site Pass: 

INFO - [RESULT] - tuxlabs.com: uid=0(root) gid=0(root) groups=0(root)
INFO - [RESULT] - tuxlabs.com: root@tlprod1:~#

INFO - [SUMMARY] - Successfully logged into 1/1 hosts and ran your command(s) in 0:00:02 second(s)

➜  bin git:(master) ✗ 

###### Key File
A key file is required for storing your password encrypted to disk. Create a file under ~/.runner/.key with a 16,24, or 32 byte character string only.

###### Store Password 
➜  scripts git:(master) ✗ storePass.py
Please Enter Site Pass: 
INFO:root:Your password has been encrypted & stored for use with Runner.
➜  scripts git:(master) ✗ 


##### Now Run 'Command File' with stored password 
➜  bin git:(master) ✗ runner -r tux -cf commands -log 
INFO - [PARAM SET] - FILTERING ONLY HOSTNAMES MATCHING "tux"
INFO - [PARAM SET] - 1 HOSTS HAVE BEEN SELECTED
INFO - [PARAM SET] - LOGFILE IS /Users/jriedel/.runner/logs/runner.log.2015-09-07.13:52:25
INFO - [PARAM SET] - USER IS tuxninja
INFO - [PARAM SET] - SSH CONNECT TIMEOUT IS 10 SECONDS
INFO - [PARAM SET] - THREADS IS 10
INFO - [PARAM SET] - THREADS TIMEOUT IS 10
INFO - [PARAM SET] - DIVIDER IS 10 CREATING 1 CHUNKS
INFO - [PARAM SET] - RETRIEVED ENCRYPTED PASSWD
INFO - [RESULT] - tuxlabs.com: uid=1000(tuxninja) gid=1000(tuxninja) groups=1000(tuxninja),27(sudo)
INFO - [RESULT] - tuxlabs.com:  16:52:27 up 27 days, 16:20,  0 users,  load average: 0.00, 0.01, 0.05

INFO - [SUMMARY] - Successfully logged into 1/1 hosts and ran your command(s) in 0:00:02 second(s)

INFO - [LOG] - Your logfile can be viewed @ /Users/jriedel/.runner/logs/runner.log.2015-09-07.13:52:25
➜  bin git:(master) ✗ 

###### Hosts file
- The current version requires that you load your hosts into a file, one host per line under ~/.runner/hosts/hosts-all 
- You can also add custom host files here and used -f to use a custom hosts file with Runner. 

