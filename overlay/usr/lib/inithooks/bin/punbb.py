#!/usr/bin/python
"""Set PunBB admin password, email and domain to serve

Option:
    --pass=     unless provided, will ask interactively
    --email=    unless provided, will ask interactively
    --domain=   unless provided, will ask interactively
                DEFAULT=www.example.com

"""

import sys
import getopt
import inithooks_cache

import hashlib
import random
import string

from dialog_wrapper import Dialog
from mysqlconf import MySQL
from executil import system

def usage(s=None):
    if s:
        print >> sys.stderr, "Error:", s
    print >> sys.stderr, "Syntax: %s [options]" % sys.argv[0]
    print >> sys.stderr, __doc__
    sys.exit(1)

DEFAULT_DOMAIN="www.example.com"

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "h",
                                       ['help', 'pass=', 'email=', 'domain='])
    except getopt.GetoptError, e:
        usage(e)

    email = ""
    domain = ""
    password = ""
    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt == '--pass':
            password = val
        elif opt == '--email':
            email = val
        elif opt == '--domain':
            domain = val

    if not password:
        d = Dialog('TurnKey Linux - First boot configuration')
        password = d.get_password(
            "PunBB Password",
            "Enter new password for the PunBB 'admin' account.")

    if not email:
        if 'd' not in locals():
            d = Dialog('TurnKey Linux - First boot configuration')

        email = d.get_email(
            "PunBB Email",
            "Enter email address for the PunBB 'admin' account.",
            "admin@example.com")

    inithooks_cache.write('APP_EMAIL', email)

    if not domain:
        if 'd' not in locals():
            d = Dialog('TurnKey Linux - First boot configuration')

        domain = d.get_input(
            "PunBB Domain",
            "Enter the domain to serve PunBB.",
            DEFAULT_DOMAIN)

    if domain == "DEFAULT":
        domain = DEFAULT_DOMAIN

    inithooks_cache.write('APP_DOMAIN', domain)

    def sha1(s):
        return hashlib.sha1(s).hexdigest()
    
    salt = ''.join((random.choice(string.letters+string.digits) for x in range(12)))
    hash = sha1(salt + sha1(password))

    m = MySQL()
    m.execute('UPDATE punbb.users SET password=\"%s\", salt=\"%s\", email=\"%s\" WHERE username=\"admin\";' % (hash, salt, email))

    m.execute('UPDATE punbb.config SET conf_value=\"%s\" WHERE conf_name=\"o_mailing_list\";' % email)
    m.execute('UPDATE punbb.config SET conf_value=\"%s\" WHERE conf_name=\"o_admin_email\";' % email)
    m.execute('UPDATE punbb.config SET conf_value=\"%s\" WHERE conf_name=\"o_webmaster_email\";' % email)

    conf = "/var/www/punbb/config.php"
    system("sed -i \"s|base_url.*|base_url = 'https://%s';|\" %s" % (domain, conf))

    apache_conf = "/etc/apache2/sites-available/punbb.conf"
    system("sed -i \"\|RewriteRule|s|https://.*|https://%s/\$1 [R,L]|\" %s" % (domain, apache_conf))
    system("sed -i \"\|RewriteCond|s|!^.*|!^%s$|\" %s" % (domain, apache_conf))
    system("service apache2 restart")

if __name__ == "__main__":
    main()
