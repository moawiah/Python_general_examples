import os, sys
import paramiko, logging
from optparse import OptionParser

#getting and parsing options and their arguments
usage = """Usage: you should provide 4 arguments:   --hostname / -host [hostname]  
                                                    --username / -u username [username]  
                                                    --password / -p  [password]
                                                    --command / -c [command]"""

parser = OptionParser()

parser.add_option("--host", "--hostname",action="store", type="string", dest="hostname", help="Hostname for the SSH command")
parser.add_option("-u", "--username",action="store", type="string", dest="username", help="Username for SSH command")
parser.add_option("-p", "--password",action="store", type="string", dest="password", help="Password for SSH")
parser.add_option("-c", "--command",action="store", type="string", dest="command", help="Command to run")

(options, args) = parser.parse_args()

if not (options.hostname and options.username and options.password and options.command):
    parser.error(usage)

#print("LOG: ", options.hostname, options.username, options.password, options.command)
print("debug info: hostname={0}, username={1}, password={2}, command={3}".format(options.hostname, options.username, options.password, options.command))

def ssh(hostname,username,password,command):
    client = paramiko.SSHClient()
    ##Adding the host key to local list
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.load_system_host_keys()

    print("Creating connection to hostname:{0}".format(hostname))
    client.connect(hostname=hostname,username=username,password=password)

    print("Connected to hostname:{0}".format(hostname))

    ##Try to execute the command and parse the output to check for errors based on exit status
    try:
        print("Executing command:{0}".format(command))
        stdin, stdout, stderr = client.exec_command(command)
        exit_status = stdout.channel.recv_exit_status()
        if exit_status != 0:
            raise paramiko.SSHException("'%s' failed with exit status %d", command, exit_status)

        print("--- OUTPUT STARTS ---")

        stdout_content = stdout.read().decode('ascii')
        print(stdout_content)

        stderr_content = stderr.read().decode('ascii')
        print("--- OUTPUT ENDS ---")

    except paramiko.SSHException as e:
        logging.error("Unable to excute command '%s' on host: %s", command, e)
        logging.debug("stdout: %s", stdout_content)
        logging.debug("stderr: %s", stderr_content)
        raise e

    print("exit status = {0}".format(exit_status))
    return stdout_content, stderr_content, exit_status

    print("Closing Connection")
    client.close()
    print("Closing Connection")

##calling ssg with arguments
stdout_content, stderr_content, exit_status = ssh(options.hostname,options.username,options.password,options.command)



