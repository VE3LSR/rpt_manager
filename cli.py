#!/usr/bin/env python3

import argparse
import logging

from app.allstar import allstar
from app.asterisk import asterisk
from app.config import config
import app.log

controller = 'controller-1'
logger = app.log.setup_custom_logger('RPT_Manager_CLI')

if __name__ == "__main__":
    config = config()

    parser = argparse.ArgumentParser(description='RPT Manager CLI')
    parser.add_argument('command', help="The command to run", choices=['getnodestat', 'sendnodecmd', 'nodestats'])
    parser.add_argument('-n', '--node', dest='node', type=int, help="The Allstar Node", action='append')
    parser.add_argument('--statcmd', dest='statcmd', help="The Stats command", choices=['XStat', 'SawStat', 'NodeStat', 'RptStat'], default='XStat')
    parser.add_argument('--cmd', dest='cmd', help="The command to run")
    parser.add_argument('-D', dest='debug', help="DEBUG Logging", action='store_true')

    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)

    values = config['asterisk'][controller]
    local_controller = asterisk(values['address'], values['port'], values['user'], values['password'])
    # XStat

    if args.command == "getnodestat":
        for node in args.node:
            result = local_controller.getNodeStat(node, args.statcmd)
            print (result)
    elif args.command == "sendnodecmd":
        for node in args.node:
            result = local_controller.sendNodeCmd(node, args.cmd)
            print (result)
    elif args.command == "nodestats":
        for node in args.node:
            result = local_controller.getNodeRptStat(node)
            print (result['data'])

    local_controller.stop()
