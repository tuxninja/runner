###Runner
An extremely useful multi-threaded SSH command runner with sudo support written in Python. I use this for my daily DevOps adventures to manage hosts and even load balancers. Make sure to add runner to your path and turn on execute permissions. 

#### Usage
    ➜  ~  runner
    
    usage: runner [-h] [-c COMMANDSTRING] [-cf COMMANDFILE] [-ct CONNECTTIMEOUT]
                  [-d DIVIDER] [-e] [-hf HOSTFILEPATH] [-l] [-lf LOGFILTER]
                  [-ll LOGLEVEL] [-log] [-p PROXYPORT] [-pl PARAMIKOLOGLEVEL]
                  [-r HOSTMATCH] [-s] [-t THREADS] [-T THREADSTIMEOUT]
                  [-u SITEUSER] [-1]
    
    optional arguments:
      -h, --help            show this help message and exit
      -c COMMANDSTRING      Command to run
      -cf COMMANDFILE       Specify a 'command file' full of commands to run on
                            selected machine(s)
      -ct CONNECTTIMEOUT    SSH connect timeout to hosts in seconds
      -d DIVIDER            Divide hosts by this number to create chunks of hosts
                            to run at a time.
      -e                    Echo's the command ran before the result output
      -hf HOSTFILEPATH      Specify your own path to a hosts file
      -l                    List all known hosts
      -lf LOGFILTER         Filter all logs for (i.e. '[RESULT],[SUMMARY]'
      -ll LOGLEVEL          Set Log Level: DEBUG, INFO (DEFAULT), WARNING, ERROR,
                            CRITICAL
      -log                  Create a logfile. Logging to a file is off by default.
      -p PROXYPORT          If using SSH Tunnel, define port to use
      -pl PARAMIKOLOGLEVEL  Set Paramiko Log Level: DEBUG, INFO, WARNING
                            (DEFAULT), ERROR, CRITICAL
      -r HOSTMATCH          Select Hosts matching supplied pattern
      -s                    Run command with sudo (performance is much slower)
      -t THREADS            Number of threads to run, don't get crazy ! Increasing
                            threads too much can negatively impact performance.
      -T THREADSTIMEOUT     Default: 10 (Effects sudo only)
      -u SITEUSER           Specify a username (by default I use who you are
                            logged in as)
      -1                    One host per pool
    
    ERROR - Either -l (list hosts only) or -c (Run command) or -cf (Run command file) is required.
    ➜  ~  

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

