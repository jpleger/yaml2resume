#!/usr/bin/env python3
from argparse import ArgumentError, ArgumentParser, FileType
import sys


def init(args):
    # copy the skel folder over and place inside the directory we init to
    
    pass

def generate(args):
    pass

def check(args):
    pass

def summary(args):
    pass

def main():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')
    
    init_parser = subparsers.add_parser('init')
    generate_parser = subparsers.add_parser('generate', aliases=['gen'])
    check_parser = subparsers.add_parser('check')
    summary_parser = subparsers.add_parser('summary', aliases=['info'])

    # Init Subparser Arguments
    init_parser.add_argument('directory', metavar='DIRECTORY', nargs='?', default='.', help='Directory to create initial yaml2resume files')


    # Generate Subparser Arguments
    generate_parser.add_argument('yamlfiles', metavar='YAML_FILE', nargs='+', help='YAML files to generate resume from')
    generate_parser.add_argument('-o', '--out-dir', metavar='OUT_DIR', default='none', help='Directory to output resume to')

    # Check Subparser Arguments
    check_parser.add_argument('yamlfiles', metavar='YAML_FILE', nargs='+', help='YAML files to generate resume from')

    # Summary Subparser Arguments
    summary_parser.add_argument('yamlfiles', metavar='YAML_FILE', nargs='+', help='YAML files to generate resume from')

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(-1)

    if args.command == 'init':
        init(args)
    elif str(args.command).startswith('gen'):
        generate(args)
    elif args.command == 'summary' or args.command == 'info':
        summary(args)
    elif args.command == 'check':
        check(args)
    else:
        raise ArgumentError('Unkown argument: %s' % args.command)

    print(dir(args))
    print(args)

