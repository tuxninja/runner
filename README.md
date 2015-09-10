###Runner

Runner is a simple, multi-threaded command line SSH utility for quick ad-hoc administration tasks and automation.  

Runner has been tested to SSH into Ubuntu, Redhat, Solaris, F5 Bigip's and Cisco IOS devices. 

#### Features & Capabilities

* Provides tunable multi-threaded SSH capabilities (-t) 
* Allows for custom hosts files (-hf)
* Accepts regular expressions for filtering host selections. (-r '^example') 
* Provides regex for 1 host per pool (-1) 
    * Note: Regular Expression may need modification for your hostname convention
* Can break apart hosts into chunks(groups) to be threaded (-d)
    * (-d 0 for Turbo Mode)  
* Works with sudo (-s) 
* Gives you full control over logging & output filtering. (-log, -ll, -pl) 
* Can run multiple commands using custom command files. (-cf)  
    * (roadmap: templating for advanced automation) 
* Seemless setup for proxying through a jump host (starttunnel, and then runner -p <port>)
* Encryption for safely remembering your password. (storePass.py, Runner finds it automatically) 

#### Usage

    ➜  ~  runner
    usage: runner [-h] [-c COMMANDSTRING] [-cf COMMANDFILE] [-ct CONNECTTIMEOUT]
                  [-cmdt CMDTIMEOUT] [-d DIVIDER] [-e] [--filter LOGFILTER]
                  [-hf HOSTFILEPATH] [-l] [-lf [LOGFILE]] [-ll LOGLEVEL]
                  [-p PROXYPORT] [-pl PARAMIKOLOGLEVEL] [-r HOSTMATCH] [-s]
                  [-t THREADS] [-u SITEUSER] [-1]
    
    optional arguments:
      -h, --help            show this help message and exit
      -c COMMANDSTRING      Command to run
      -cf COMMANDFILE       Specify a 'command file' full of commands to run on
                            selected machine(s)
      -ct CONNECTTIMEOUT    SSH connect timeout to hosts in seconds: default (10)
      -cmdt CMDTIMEOUT      Timeout for how long to let commands run: default (60)
      -d DIVIDER            Divide hosts by this number to create chunks of hosts
                            to run at a time.
      -e                    Echo's the command ran before the result output
      --filter LOGFILTER    Filter all logs for (i.e. '[RESULT],[SUMMARY]'
      -hf HOSTFILEPATH      Specify your own path to a hosts file
      -l                    List all known hosts
      -lf [LOGFILE]         Turns logging on, can also take logfile location as a
                            parameter.
      -ll LOGLEVEL          Set Log Level: DEBUG, INFO (DEFAULT), WARNING, ERROR,
                            CRITICAL
      -p PROXYPORT          If using SSH Tunnel, define port to use
      -pl PARAMIKOLOGLEVEL  Set Paramiko Log Level: DEBUG, INFO, WARNING, ERROR,
                            CRITICAL (DEFAULT)
      -r HOSTMATCH          Select Hosts matching supplied pattern
      -s                    Run command with sudo (performance is much slower)
      -t THREADS            Number of threads to run, don't get crazy ! Increasing
                            threads too much can negatively impact performance.
      -u SITEUSER           Specify a username (by default I use who you are
                            logged in as)
      -1                    One host per pool
    
    ERROR - Either -l (list hosts only) or -c (Run command) or -cf (Run command file) is required.
    ➜  ~  
    
#### Installation

Real instructions coming soon, for now... 

* git clone https://github.com/tuxninja/runner.git
* pip install dependencies
* Copy bin/* to /usr/local/bin or add it to your PATH.

#### Example Non-Sudo Usage

    ➜  bin git:(master) ✗ runner -r tux -c 'id' -lf
    INFO - [PARAM SET] - FILTERING ONLY HOSTNAMES MATCHING "tux"
    INFO - [PARAM SET] - 1 HOSTS HAVE BEEN SELECTED
    INFO - [PARAM SET] - LOGFILE IS /Users/tuxninja/.runner/logs/runner.log.2015-09-07.13:46:53
    INFO - [PARAM SET] - USER IS tuxninja
    INFO - [PARAM SET] - SSH CONNECT TIMEOUT IS 10 SECONDS
    INFO - [PARAM SET] - THREADS IS 10
    INFO - [PARAM SET] - DIVIDER IS 10 CREATING 1 CHUNKS
    Please Enter Site Pass: 
    
    INFO - [RESULT] - tuxlabs.com: uid=1000(tuxninja) gid=1000(tuxninja) groups=1000(tuxninja),27(sudo)
    
    INFO - [SUMMARY] - Successfully logged into 1/1 hosts and ran your command(s) in 0:00:05 second(s)
    
    INFO - [LOG] - Your logfile can be viewed @ /Users/tuxninja/.runner/logs/runner.log.2015-09-07.13:46:53
    ➜  bin git:(master) ✗ 
    
#### Example Sudo Usage + Output Filtering
    
    ➜  bin git:(master) ✗ runner -r tux -c 'id' -lf -s --filter RESULT,SUMMARY
    Please Enter Site Pass: 
    
    INFO - [RESULT] - tuxlabs.com: uid=0(root) gid=0(root) groups=0(root)
    INFO - [RESULT] - tuxlabs.com: root@tlprod1:~#
    
    INFO - [SUMMARY] - Successfully logged into 1/1 hosts and ran your command(s) in 0:00:02 second(s)
    
    ➜  bin git:(master) ✗ 

#### Example SSH Tunneling aka Proxying
    ➜  bin git:(master) ✗ ./starttunnel 8081 jump.tuxlabs.com
    #################################################################
    #                                                               #
    #       This system is for the use of authorized users only.    #
    ...
    tuxninja@jump.tuxlabs,com's password: 
    ➜  bin git:(master) ✗ 
    
    ➜  bin git:(master) ✗ runner -r tux -c 'id' -p 8081
    INFO - [PARAM SET] - FILTERING ONLY HOSTNAMES MATCHING "tux"
    INFO - [PARAM SET] - 1 HOSTS HAVE BEEN SELECTED
    INFO - [PARAM SET] - USER IS tuxninja
    INFO - [PARAM SET] - SSH CONNECT TIMEOUT IS 10 SECONDS
    INFO - [PARAM SET] - THREADS IS 10
    INFO - [PARAM SET] - DIVIDER IS 10 CREATING 1 CHUNKS
    INFO - [PARAM SET] - RETRIEVED ENCRYPTED PASSWD
    INFO - [RESULT] - tuxlabs.com: uid=1000(tuxninja) gid=1000(tuxninja) groups=1000(tuxninja),27(sudo)
    
    INFO - [SUMMARY] - Successfully logged into 1/1 hosts and ran your command(s) in 0:00:01 second(s)
    
    ➜  bin git:(master) ✗ 

#### Store Password 

    ➜  ~  storePass.py                                                                   
    A key file was not found, you must create one.
    Enter Key(16,24, or 32 characters): 
    Please Enter Site Pass: 
    INFO:root:Your password has been encrypted & stored for use with Runner.
    ➜  ~  

#### Now We Can Run A 'Command File' with stored password 

    ➜  bin git:(master) ✗ runner -r tux -cf commands -lf
    INFO - [PARAM SET] - FILTERING ONLY HOSTNAMES MATCHING "tux"
    INFO - [PARAM SET] - 1 HOSTS HAVE BEEN SELECTED
    INFO - [PARAM SET] - LOGFILE IS /Users/tuxninja/.runner/logs/runner.log.2015-09-07.13:52:25
    INFO - [PARAM SET] - USER IS tuxninja
    INFO - [PARAM SET] - SSH CONNECT TIMEOUT IS 10 SECONDS
    INFO - [PARAM SET] - THREADS IS 10
    INFO - [PARAM SET] - DIVIDER IS 10 CREATING 1 CHUNKS
    INFO - [PARAM SET] - RETRIEVED ENCRYPTED PASSWD
    INFO - [RESULT] - tuxlabs.com: uid=1000(tuxninja) gid=1000(tuxninja) groups=1000(tuxninja),27(sudo)
    INFO - [RESULT] - tuxlabs.com:  16:52:27 up 27 days, 16:20,  0 users,  load average: 0.00, 0.01, 0.05
    
    INFO - [SUMMARY] - Successfully logged into 1/1 hosts and ran your command(s) in 0:00:02 second(s)
    
    INFO - [LOG] - Your logfile can be viewed @ /Users/tuxninja/.runner/logs/runner.log.2015-09-07.13:52:25
    ➜  bin git:(master) ✗ 



#### Required Hosts File & Custom Host Files

- Runner currently requires that you load your hosts into a file, one host per line under ~/.runner/hosts/hosts-all 
- You may create as many host files as you like and use -hf to supply a custom hosts file
