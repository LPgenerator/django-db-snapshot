# -*- encoding: utf-8 -*-

from django.conf import settings


def get_settings(key, default):
    return getattr(settings, key, default)


SERVER_HOST = get_settings('DBS_SERVER_HOST', '127.0.0.1')
SERVER_PORT = get_settings('DBS_SERVER_PORT', 61216)
BACKUP_DIR = get_settings('DBS_BACKUP_DIR', '/var/cache/mylvmbackup/backup')
MLB_BIN = get_settings('DBS_MLB_BIN', '/usr/bin/mylvmbackup')
