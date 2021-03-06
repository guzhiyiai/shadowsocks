#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2015 mengskysama
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import sys
import os
import logging
import time
import getopt
import imp

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))
from shadowsocks import manager

def handler_SIGQUIT():
    return

def main():
    shortopts = 'hc:'
    longopts = ['help', 'config']
    optlist, args = getopt.getopt(sys.argv[1:], shortopts, longopts)

    config_path = None
    for o, a in optlist:
        if o in ('-h', '--help'):
            print 'Usage: run_manager -c path_to_config.py'
            sys.exit(0)
        elif o in ('-c', '--config'):
            config_path = a

    if not config_path:
        print 'config not specified'
        sys.exit(2)

    config = imp.load_source('config', config_path)

    level = config.LOG_LEVEL
    logging.basicConfig(level=level,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    configer = {
        'server': '%s' % config.SS_BIND_IP,
        'local_port': 1081,
        'port_password': {},
        'method': '%s' % config.SS_METHOD,
        'manager_address': '%s:%s' % (config.MANAGE_BIND_IP, config.MANAGE_PORT),
        'timeout': 60,
        'fast_open': False,
        'verbose': 5
    }
    manager.run(configer)

    while True:
        time.sleep(100)


if __name__ == '__main__':
    main()
