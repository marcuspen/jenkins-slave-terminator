import argparse
import ConfigParser
from os.path import expanduser
from os import system

import jenkins


def check_slaves(server, slaves):
    for slave in slaves:
        info = server.get_node_info(slave)
        if info['offline']:
            system('gcloud compute instances stop {}'.format(slave))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'ids',
        nargs='+',
        help='Jenkins slave IDs',
    )
    args = parser.parse_args()
    slave_ids = args.ids

    config = ConfigParser.ConfigParser()
    config.read(expanduser('~/config/config.ini'))
    if not config.sections():
        raise Exception('No config file found')

    server = jenkins.Jenkins(
        config.get('Jenkins Server', 'url'),
        username=config.get('Credentials', 'username'),
        password=config.get('Credentials', 'password')
    )

    check_slaves(server, slave_ids)

if __name__ == '__main__':
    main()
