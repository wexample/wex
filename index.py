#!/usr/bin/python3

import argparse

parser = argparse.ArgumentParser(
    description='A bash scripts manager.'
)

parser.add_argument(
    'command_name',
    metavar='command_name',
    type=str,
    help='Command name'
)

parser.add_argument(
    '-a',
    '--first-arg',
    dest='first_arg',
    type=str,
    help='Your first arg'
)

args = parser.parse_args()

print('Addon/group/name: ' + args.addon_group_name)
print('First arg: ' + str(args.first_arg))
