#!/usr/bin/env python3

import yaml, sys, time

from app.allstar import allstar
from app.asterisk import asterisk

controller = 'controller-1'

if __name__ == "__main__":
    with open("config.yml", 'r') as stream:
        try:
            config = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(0)

    print (config)

    values = config['asterisk'][controller]
    local_controller = asterisk(values['address'], values['port'], values['user'], values['password'])
    # XStat
    result = local_controller.getNodeStat(29133)
    print (result)

    # SawStat
    result = local_controller.getNodeStat(29133, "SawStat")
    print (result)

    # NodeStat
    result = local_controller.getNodeStat(29133, "NodeStat")
    print (result)

    # RptStat
    result = local_controller.getNodeStat(29133, "RptStat")
    print (result)

    result = local_controller.getNodeRptStat(29133)
    print (result)

#    result = local_controller.sendNodeCmd("rpt fun 29154 #81")
#    print (result)

    time.sleep(2)

    local_controller.stop()
