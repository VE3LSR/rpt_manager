#!/usr/bin/env python3

import argparse

from app.allstar import allstar
from app.asterisk import asterisk
from app.config import config

controller = 'controller-1'

if __name__ == "__main__":
    config = config()

    parser = argparse.ArgumentParser(description='RPT Manager CLI')
    parser.add_argument('command', help="The command to run", choices=['getnodestat', 'sendnodecmd', 'nodestats'])
    parser.add_argument('-n', '--node', dest='node', type=int, help="The Allstar Node", action='append')
    parser.add_argument('--statcmd', dest='statcmd', help="The Stats command", choices=['XStat', 'SawStat', 'NodeStat', 'RptStat'], default='XStat')
    parser.add_argument('--cmd', dest='cmd', help="The command to run")

    args = parser.parse_args()

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
