"""This module provides Client service to SSH."""

import capture_logger as logger
from os import system
from paramiko import SSHClient, AutoAddPolicy, RSAKey
from paramiko.auth_handler import AuthenticationException, SSHException
from scp import SCPClient, SCPException

file_name = logger.logfilegen()
logger.logformat(file_name)


class RemoteClient:
    """Client to interact with a remote host."""

    def __init__(self, host, user, password, remote_path=''):
        self.host = host
        self.user = user
        self.password = password
        self.remote_path = remote_path
        self.client = None
        self.scp = None
        self.conn = None

    def __connect(self):
        """
        Open connection to remote host.
        """
        try:
            self.client = SSHClient()
            self.client.load_system_host_keys()
            self.client.set_missing_host_key_policy(AutoAddPolicy())
            self.client.connect(self.host,
                                username=self.user,
                                password=self.password,
                                timeout=5000)
            self.scp = SCPClient(self.client.get_transport())
        except AuthenticationException as error:
            logger.info('Authentication failed: did you remember to create an SSH key?')
            logger.error(error)
            raise error
        finally:
            return self.client

    def disconnect(self):
        """
        Close ssh connection.
        """
        self.client.close()
        self.scp.close()

    def bulk_upload(self, files):
        """
        Upload multiple files to a remote directory.

        :param files: List of strings representing file paths to local files.
        """
        if self.client is None:
            self.client = self.__connect()
        uploads = [self.__upload_single_file(file) for file in files]
        logger.info('Finished uploading {} files to {} on {}'.format(len(uploads),self.remote_path,self.host))

    def __upload_single_file(self, file):
        """Upload a single file to a remote directory."""
        try:
            self.scp.put(file,
                         recursive=True,
                         remote_path=self.remote_path)
        except SCPException as error:
            logger.error(error)
            raise error
        finally:
            logger.info('Uploaded {} to {}'.format(file,self.remote_path))

    def download_file(self, file):
        """Download file from remote host."""
        if self.conn is None:
            self.conn = self.connect()
        self.scp.get(file)

    def execute_command(self, command):
        """
            Execute command on Remote Host
        :param command this is input
        """
        if self.client is None:
            self.client = self.__connect()
        stdin, stdout, stderr = self.client.exec_command(command)
        stdout.channel.recv_exit_status()
        response = stdout.readlines()
        print(response)
        for line in response:
            logger.info('INPUT: {} | OUTPUT: {}'.format(command,line))

    def execute_multiple_commands(self, filename):
        """
            Execute commands on Remote Host
        :param filename: Pass file path/filename
        """
        if self.client is None:
            self.client = self.__connect()
        commands = open(filename,'r')
        for command in commands:
            stdin, stdout, stderr = self.client.exec_command(command)
            stdout.channel.recv_exit_status()
            response = stdout.readlines()
            print(response)
            for line in response:
                logger.info('INPUT: {} | OUTPUT: {}'.format(command,line))


if __name__ == '__main__':
    rc_obj = RemoteClient('192.168.1.1','root','password')
    rc_obj.execute_command('ls -l')

    rc_obj.disconnect()