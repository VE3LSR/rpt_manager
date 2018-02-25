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

    node_parser = argparse.ArgumentParser(add_help=False)
    node_parser.add_argument('-n', '--node', type=int, help="The Allstar Node", action='append', required=True)

    debug_parser = argparse.ArgumentParser(add_help=False)
    debug_parser.add_argument('-D', dest='debug', help="DEBUG Logging", action='store_true')

    parser = argparse.ArgumentParser(description='RPT Manager CLI', parents=[debug_parser])
    subparsers = parser.add_subparsers(dest='command')

    parser_getnodestat = subparsers.add_parser('getnodestat', parents=[node_parser,debug_parser])
    parser_getnodestat.add_argument('statcmd', help="The Stats command", choices=['XStat', 'SawStat', 'NodeStat', 'RptStat'], default='XStat')

    parser_sendnodecmd = subparsers.add_parser('sendnodecmd', parents=[node_parser,debug_parser])
    parser_sendnodecmd.add_argument('cmd', help="The command to run")

    parser_nodestats = subparsers.add_parser('nodestats', parents=[node_parser,debug_parser])

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
    else:
        parser.print_help()

    local_controller.stop()
