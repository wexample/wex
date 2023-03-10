#!/usr/bin/python3

import argparse

parser = argparse.ArgumentParser(description='Description de votre programme.')
parser.add_argument('addon_group_name', metavar='addon_group_name', type=str,
                    help='Nom de l\'addon, groupe et nom du service.')
parser.add_argument('-a', '--first-arg', dest='first_arg', type=str,
                    help='Premier argument avec le nom court.')

args = parser.parse_args()

print('Hi! Welcome in wex world.')
print('Addon/group/name: ' + args.addon_group_name)
print('First arg: ' + str(args.first_arg))
