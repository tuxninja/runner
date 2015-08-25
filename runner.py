#!/usr/bin/env python
#Author: Jason Riedel

import paramiko
import getpass
import Queue
import threading
import argparse
import os.path
import time
import logging
import re
import datetime

## SETUP AVAILABLE ARGUMENTS ##
parser = argparse.ArgumentParser()
parser.add_argument('-f', action="store", dest="file_path", required=False, help="Specify your own path to a hosts file")
parser.add_argument('-l', action="store_true", dest="list_only", required=False, help="List all known hosts")
parser.add_argument('-q', action="store_true", dest="quiet_mode", required=False, help="Quiet mode: turns off RUNNER INFO messages.")
parser.add_argument('-qq', action="store_true", dest="super_quiet_mode", required=False, help="Super Quiet mode: turns off ALL RUNNER messages except [INPUT].")
parser.add_argument('-r', action="store", dest="host_match", required=False, help="Select Hosts matching supplied pattern")
parser.add_argument('-c', action="store", dest="command_string", required=False, help="Command to run")
parser.add_argument('-s', action="store_true", dest="sudo", required=False, help="Run command inside root shell using sudo") 
parser.add_argument('-t', action="store", dest="connect_timeout", required=False, help="ssh timeout to hosts in seconds")
parser.add_argument('-T', action="store", dest="threads", required=False, help="# of threads to run (don't get crazy)")
parser.add_argument('-u', action="store", dest="site_user", required=False, help="Specify a username (by default I use who you are logged in as)")
parser.add_argument('-1', action="store_true", dest="host_per_pool", required=False, help="One host per pool")
args = parser.parse_args()

##GLOBAL##
logging.getLogger('paramiko.transport').addHandler(logging.NullHandler())

stime = time.time()

## SET TIMEOUT ##
connect_timeout = 5
if args.connect_timeout:
    connect_timeout = args.connect_timeout

## SET THREADS / WORKERS ##
workers = 20
if args.threads:
    workers = int(args.threads)

## SET USER / PASS ##
site_user = getpass.getuser()
site_passwd = ''
if args.site_user:
    site_user = args.site_user

failed_logins = []
successful_logins = []

tstamp = datetime.datetime.now().strftime("%Y-%m-%d.%H:%M:%S")
logfile_dir = 'logs'
if not os.path.exists(logfile_dir):
    os.makedirs(logfile_dir)
logfile_path = '%s/runner.log.%s' % (logfile_dir, tstamp)
logfile = open(logfile_path, 'w')

## END GLOBAL ##

def ssh_to_host(hosts, site_passwd):
    for i in range(workers):
        t = threading.Thread(target=worker, args=(site_user, site_passwd))
        t.daemon = True
        t.start()

    for hostname in hosts:
        hostname = hostname.rstrip()
        q.put(hostname)

    q.join()

def worker(site_user, site_passwd):
    while True:
        hostname = q.get()
        node_shell(hostname, site_user, site_passwd)
        q.task_done()


def node_shell(hostname, site_user, site_passwd):
    ssh = paramiko.SSHClient()
    #comment out proxy_command and proxy_sock and remove sock=proxy_sock parameter from the connect string below, to NOT use a bastion/jumphost through a tunnel. 
    proxy_command = "sconnect -4 -w 4 -S localhost:8081 %s %s" % (hostname,'22')
    proxy_sock = paramiko.ProxyCommand(proxy_command)
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname, username=site_user, password=site_passwd, timeout=connect_timeout, sock=proxy_sock)
        transport = ssh.get_transport()
        transport.set_keepalive(1)

        cmd = args.command_string
	if args.sudo: 
		try: 
			## have to use invoke shell for sudo due to ssh config on machines requirng a TTY
			channel = ssh.invoke_shell() 
			sudocmd = 'sudo ' + cmd

			channel.send(sudocmd + '\n') 

			buff = ''
			while not '[sudo] password' in buff: 
				resp = channel.recv(9999)
				buff += resp

			channel.send(site_passwd + '\n') 

			buff = ''
			while not buff.endswith('$ '):
				resp = channel.recv(9999)
				buff += resp

			for line in buff.split('\n'):
				log_and_print("%s: %s" % (hostname, line))

		except Exception as e:
			log_and_print("ERROR: Sudo failed: %s" % (e))  
  
	else: 
        	(stdin, stdout, stderr) = ssh.exec_command(cmd)

		## stdout 
        	for line in stdout.readlines():
            		line = line.rstrip()
            		log_and_print("%s: %s" % (hostname, line))
		## stderr
        	for line in stderr.readlines():
            		line = line.rstrip()
            		log_and_print("%s: %s" % (hostname, line))

        successful_logins.append(hostname)
        ssh.close()

    except Exception as e:
        log_and_print("%s: failed to login : %s" % (hostname, e))
        failed_logins.append(hostname)
        ssh.close()

def log_and_print(message):
    if args.super_quiet_mode or args.list_only:
        if "RUNNER [INPUT]" in message or "RUNNER [ERROR]" in message or "RUNNER" not in message:
            print message
            logfile.write(message + '\n')
    elif args.quiet_mode or args.list_only:
        if "RUNNER [INFO]" not in message:
            print message
            logfile.write(message + '\n')
    else:
        print message
        if not args.list_only:
            logfile.write(message + '\n')

def get_hosts(file_path):
    if os.path.exists(file_path):
        hosts = open(file_path)
        selected_hosts = []
        if not args.host_match:
            selected_hosts = list(hosts)
            log_and_print("RUNNER [INFO]: SELECTING ALL HOSTS")
        else:
            host_match = args.host_match
            for host in hosts:
                if re.search(host_match, host):
                    selected_hosts.append(host)
            log_and_print("RUNNER [INFO]: MATCHING HOSTNAMES WITH '%s'" % (host_match))
    else:
        log_and_print("RUNNER [ERROR]: %s does not exist ! Try running ./update-runner-hosts" % (file_path))
        exit()

    ## Select one host per pool
    if args.host_per_pool:
        seen = {}
        host_per_pool = []
        for host in selected_hosts:
	    # Here strip values that make hostnames unique like #'s
	    # That way the dict matches after 1 host per pool has been seen 
            nhost = re.sub("\d+?\.", ".", host) #Removing #'s in a hostname like host1234.tuxlabs.com
            if not nhost in seen:
                seen[nhost] = 1
                host_per_pool.append(host)
        selected_hosts = host_per_pool

    log_and_print("RUNNER: %s HOSTS HAVE BEEN SELECTED" % (len(selected_hosts)))
    return selected_hosts

if __name__ == "__main__":
    file_path = 'hosts/hosts-all' ## update-hosts-all creates the DIR 

    if args.file_path:
        file_path = args.file_path
        if '~' in file_path:
            print "RUNNER [ERROR]: -f does not support '~'"
            exit()

    if args.list_only or args.command_string:
        selected_hosts = get_hosts(file_path)
        if args.list_only:
            for host in selected_hosts:
                host = host.rstrip()
                log_and_print(host)
            log_and_print("\nThere were %s hosts listed." % (len(selected_hosts)))
            exit()

        else:
            log_and_print("RUNNER [INFO]: LOGFILE SET - %s" % (logfile_path))
            log_and_print("RUNNER [INFO]: USER SET - %s" % (site_user))
            log_and_print("RUNNER [INFO]: SSH CONNECT TIMEOUT is: %s seconds" % (connect_timeout))
            log_and_print("RUNNER [INFO]: THREADS SET - %s" % (workers))
	    if args.sudo:
		log_and_print("RUNNER [INFO]: SUDO IS ON") 

            site_passwd = getpass.getpass("RUNNER [INPUT]: Please Enter Site Pass: ")

            q = Queue.Queue()

            ssh_to_host(selected_hosts,site_passwd)

            etime=time.time()
            run_time = int(etime-stime)

            timestamp = str(datetime.timedelta(seconds=run_time))
            log_and_print("\nRUNNER [RESULT]: Successfully logged into %s/%s hosts and ran your commands in %s second(s)" % (len(successful_logins), len(selected_hosts), timestamp))
            log_and_print("RUNNER [RESULT]: There were %s login failures.\n" % (len(failed_logins)))
            if len(failed_logins) > 0:
                for failed_host in failed_logins:
                    log_and_print("RUNNER [RESULT]: Failed to login to: %s" % (failed_host))
    else:
        parser.print_help()
        output = "\nRUNNER [INFO]: Either -l (list hosts only) or -s (Run cmd string) is required.\n"
        log_and_print(output)
