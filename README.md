###Runner
An extremely useful multi-threaded SSH command runner with sudo support written in Python. I use this for my daily DevOps adventures to manage hosts and even load balancers. Make sure to add runner to your path and turn on execute permissions. 

- Use runner.py for a non-proxy version. 
- Use prunner.py for a proxy version, that utilizes an existing tunnel (on port 8081) and sconnect. 

###### Usage
	➜  runner git:(master) ✗ runner -r web -c 'id' -T 40 -p 10 -s
	RUNNER [INFO]: MATCHING HOSTNAMES WITH 'web'
	RUNNER [INFO]: 19565 HOSTS HAVE BEEN SELECTED
	RUNNER [INFO]: LOGFILE SET - /Users/jriedel/.runner/logs/runner.log.2015-08-25.00:43:21
	RUNNER [INFO]: USER SET - jriedel
	RUNNER [INFO]: SSH CONNECT TIMEOUT is: 10 seconds
	RUNNER [INFO]: THREADS SET - 40
	RUNNER [INFO]: PERCENTAGE SET - 10
	RUNNER [INFO]: HOSTS ARE BEING DIVIDED INTO 1957 CHUNKS
	RUNNER [INFO]: SUDO IS ON
	RUNNER [INPUT]: Please Enter Site Pass: 


###### sconnect
Is a binary that gets used by runner if you need to tunnel through a bastion or jump box. 
See https://bitbucket.org/gotoh/connect/wiki/Home for more info on sconnect
