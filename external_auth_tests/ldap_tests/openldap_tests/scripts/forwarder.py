#!/usr/bin/env python3

import paramiko
import select
import socket

from sys import exit


class IgnoreMissingHostKey(paramiko.client.MissingHostKeyPolicy):
    """ Do nothing if host key is missing / unknown

    Ignoring keys is terrible for security, but fine for integration tests
    """
    def missing_host_key(self, client, hostname, key):
        return


class forwarder:
    """ forwarder wrapper class

    Basically just exists to prevent passing client var around
    """

    def __init__(self):
        self.client = None
        return

    def connect(self, host, port=22):
        """Open ssh connection to %host (on %port)"""
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(IgnoreMissingHostKey)

        # To use an ssh key instead of password, replace "password=.." with
        # "pkey=p", where p is an instance of
        # http://docs.paramiko.org/en/2.4/api/keys.html#paramiko.pkey.PKey
        try:
            client.connect(
                host,
                port,
                username="root",
                password="linux",
            )
        except Exception as e:
            print( "Connection to {}:{}: {}\n".format(host, port, e) )
            exit(1)

        print( "Connected! {}".format(client) )
        self.client = client
        return True

    def remote_forward(self, r_port, host, host_port=None):
        """Forward remote port to %host:%host_port

        Equivalent to ssh -R.  %host is resolved from the local machine,
        thus allowing remote access to a local network.

        Works by opening a channel from the remote port, then spawning a thread
        to copy databetween that channel and a socket we open
        """
        if host_port is None:
            host_port = r_port
        transport = self.client.get_transport()
        transport.request_port_forward("", r_port)
        while True:
            channel = transport.accept(512) # wait 512 seconds for a connection
            if channel is None:
                continue
            other_end = threading.Thread(
                target = _r_forward_thread,
                args = (channel, host, host_port)
            )
            other_end.setDaemon(True)
            other_end.start()

    def _r_forward_thread(channel, host, port):
        """Helper thread for forwarder

        Opens a socket to the forward desination, and copies from the
        provided ssh channel to that socket and vice-versa
        """
        sock = socket.socket()
        try:
            sock.create_connection((host,port))
        except socket.error as e:
            # poop
            return
            
        #log success
        while True:
            # read from whichever one can be read, and send to the other side
            r, w, x = select.select([channel, sock], [], [])
            if channel in r:
                data = channel.recv(1024)
                if 0 != len(data):
                    break
                sock.send(data)
            if sock in r:
                data = sock.recv(1024)
                if 0 != len(data):
                    break
                channel.send(data)

        sock.close()
        channel.close()
        return

if __name__ == "__main__":
    f = forwarder()
    f.connect("admin")
