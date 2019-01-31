#!/usr/bin/env python

from __future__ import print_function
import psycopg2
import configparser
import StringIO
import os
import md5

CONFIG_PATH='/opt/products/dstar/dstar_gw/dsipsvd/dsipsvd.conf'
QUERY_UNREG = """SELECT user_cs, reg_date, e_mail, user_name FROM unsync_user_mng WHERE admin_flg = 'f' AND regist_flg = 'false' ORDER by user_cs"""
UPDATE_PASS = """UPDATE unsync_user_mng set password = %s WHERE user_cs = %s"""
UPDATE_ENABLE = """UPDATE unsync_user_mng set regist_flg = %s WHERE user_cs = %s"""

class G3:

    def __init__(self):
        self.ReadConfig()
        try:
            self.conn = psycopg2.connect("dbname='{}' user='{}' host='localhost' password='{}'".format(self.config['default']['DB_NAME'],self.config['default']['DB_USER'],self.config['default']['DB_PASSWORD']))
        except:
            print ("I am unable to connect to the database")
        self.cur = self.conn.cursor()

    def ReadConfig(self):
        self.config = configparser.ConfigParser()
        # Python 2
        config_string = StringIO.StringIO()
        config_string.write('[default]\n')
        config_string.write(open(CONFIG_PATH).read())
        config_string.seek(0, os.SEEK_SET)
        self.config.readfp(config_string)

        # Python 3
        #with open(CONFIG_PATH, 'r') as f:
        #    config_string = '[default]\n' + f.read()
        # config.read_string(config_string)

    def setPassword(self, user, passw):
        user = user.upper()
        passw = self.getDigest(passw)
        self.ExeQuery (UPDATE_PASS, (passw, user))

    def setRegister(self, user, flag):
        user = user.upper()
        self.ExeQuery (UPDATE_ENABLE, (flag, user))

    def getSeq(self):
        self.ExeQuery("""select nextval('command_seq')""", ())
        rows = self.cur.fetchone()
        return rows[0]

    # How G2/G3 stores passwords
    def getDigest(self, passw):
        m = md5.new()
        m.update(passw[0:16])
        return m.hexdigest()

    def GetUnregistered(self):
        self.cur.execute(QUERY_UNREG)
        rows = self.cur.fetchall()
        return rows

    def ExeQuery(self, query, params):
        self.cur.execute(query, params)
        self.conn.commit()

    def RunQuery(self, query):
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return rows

    def showRows(self, rows):
        for row in rows:
            for col in row:
                print ("[{}]  ".format(col), end="")
            print("")

if __name__ == "__main__":
    import argparse
    import getpass
    callsign_parser = argparse.ArgumentParser(add_help=False)
    callsign_parser.add_argument('CallSign', help="The users callsign")

    parser = argparse.ArgumentParser(description='Do things with DStar Gateway')
    subparsers = parser.add_subparsers(dest='command')

    password_parser = subparsers.add_parser('setpass', description='Set a users password', parents=[callsign_parser])
    unreg_parser = subparsers.add_parser('regreq', description='List unregistered users')

    enable_parser = subparsers.add_parser('enuser', description='Enable A User', parents=[callsign_parser])
    disable_parser = subparsers.add_parser('disuser', description='Disable A User', parents=[callsign_parser])

    g = G3()

    args = parser.parse_args()

    if args.command == "regreq":
        g.showRows(g.GetUnregistered())
    if args.command == "setpass":
        passw = getpass.getpass("Password: ")
        g.setPassword(args.CallSign,passw)
    if args.command == "enuser":
        g.setRegister(args.CallSign, True)
    if args.command == "disuser":
        g.setRegister(args.CallSign, False)

#    g.showRows(g.RunQuery("""SELECT user_cs, reg_date, e_mail, user_name, regist_flg FROM unsync_user_mng WHERE admin_flg = 'f' ORDER by user_cs"""))
#    g.showRows(g.RunQuery("""SELECT target_cs, arearp_cs, user_cs, pc_ipaddr FROM sync_mng WHERE del_flg = 'f' ORDER by user_cs, target_cs"""))
#    g.showRows(g.RunQuery("""SELECT user_cs, regist_rp_cs, start_ipaddr FROM sync_rip WHERE del_flg = 'f' and start_ipaddr != '0.0.0.0' ORDER by user_cs"""))
