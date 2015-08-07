#!/usr/bin/env python
from __future__ import absolute_import

import logging
import ssl
import sys

import irc
import irc.bot
import irc.client
import irc.connection


class IRCAlert(object):

    def __init__(self, server, port, channel, password, realname, msg):
        super(IRCAlert, self).__init__()
        self.server = server
        self.port = port
        self.channel = channel
        self.password = password
        self.username = realname
        self.message = msg
        self.botnick = 'alertbot'
        self.ssl_factory = irc.connection.Factory(wrapper=ssl.wrap_socket)
    getattr(logging, 'DEBUG')
    logging.basicConfig(level=logging.DEBUG)

    def on_connect(self, connection, event):
        channel = self.channel
        if irc.client.is_channel(channel):
            connection.join(channel)

    def on_join(self, connection, event):
        channel = self.channel
        message = self.message
        connection.privmsg(channel, message)

    def main(self):
        reactor = irc.client.Reactor()
        try:
            c = reactor.server().connect(
                self.server,
                self.port,
                self.botnick,
                self.password,
                self.username,
                connect_factory=self.ssl_factory,
            )
        except irc.client.ServerConnectionError:
            print(sys.exc_info()[1])
            raise SystemExit(1)

        c.add_global_handler("welcome", self.on_connect())
        c.add_global_handler("join", self.on_join())
        status = c.is_connected()
        print "Connected to IRC: %s" % status
        reactor.process_forever()
