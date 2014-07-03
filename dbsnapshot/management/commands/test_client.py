# -*- encoding: utf-8 -*-

from optparse import make_option
from pprint import pprint

from django.core.management.base import BaseCommand
from dbsnapshot import defaults, client


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-p', '--port', dest='port', default=defaults.SERVER_PORT),
        make_option('-r', '--host', dest='host', default=defaults.SERVER_HOST),
        make_option('-m', '--method', dest='method', default='hello'),
        make_option('-a', '--args', dest='args', default=''),
    )

    def handle(self, **options):
        cli = client.Client(options['host'], int(options['port']))
        cli.send(options.get('method'), options.get('args'))
        pprint(cli.recv())
        cli.close()
