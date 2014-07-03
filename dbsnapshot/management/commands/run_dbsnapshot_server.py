# -*- encoding: utf-8 -*-

import SocketServer
import types
import json
import os

from django.core.management.base import NoArgsCommand
from django.db import connection

from dbsnapshot import defaults


class StatisticsHandler(SocketServer.BaseRequestHandler):
    @staticmethod
    def list():
        return os.listdir(defaults.BACKUP_DIR)

    @staticmethod
    def backup():
        return {'status': os.system(defaults.MLB_BIN) == 0}

    @staticmethod
    def delete(filename):
        filename = os.path.join(defaults.BACKUP_DIR, filename)
        return {'status': os.system('rm -f %s' % filename) == 0}

    @staticmethod
    def cleanup(days='1', status=-1):
        if str(days).isdigit():
            status = os.system(
                "find %s -type f -name '*.tar.*' "
                "-mtime +%s -exec rm -f {} \;" % (defaults.BACKUP_DIR, days))
        return {'status': status == 0}

    @staticmethod
    def status(status=True):
        cursor = connection.cursor()
        cursor.execute("SHOW SLAVE STATUS;")
        result = dict(
            zip([col[0] for col in cursor.description], cursor.fetchone()))
        if result.get('Seconds_Behind_Master') is None:
            status = False
        elif result.get('Last_Error'):
            status = False
        elif result.get('Last_IO_Error'):
            status = False
        return {'status': status}

    @staticmethod
    def hello():
        return {'status': 'OK'}

    def handle(self):
        method, args = self.request.recv(1024).rstrip(';').split(':')
        if hasattr(self, method):
            method = getattr(self, method)
            if isinstance(method, types.FunctionType):
                result = json.dumps(method(*(args and args.split(','))))
                return self.request.sendall('%s;' % result)
        self.request.close()


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        address = (defaults.SERVER_HOST, defaults.SERVER_PORT)
        server = SocketServer.ForkingTCPServer(address, StatisticsHandler)
        server.serve_forever()
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        server.server_close()
