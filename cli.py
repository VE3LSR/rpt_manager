#!/usr/bin/env python3

from app.allstar import allstar
from app.asterisk import asterisk
from app.config import config

controller = 'controller-1'

if __name__ == "__main__":
    config = config()

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

#    result = local_controller.getNodeRptStat(29133)
#    print (result)

#    result = local_controller.sendNodeCmd("rpt fun 29154 #81")
#    print (result)

    time.sleep(2)

    local_controller.stop()
