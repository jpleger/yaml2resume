#!/usr/bin/env python3
import sys
import os
import shutil
from argparse import ArgumentError, ArgumentParser
from yaml2resume.parse import read_resumes

def init(args):
    # copy the skel folder over and place inside the directory we init to
    module_dir = os.path.abspath(os.path.dirname(__file__))
    skel_dir = os.path.join(module_dir, 'skel')
    dest_dir = os.path.abspath(os.path.expanduser(os.path.expandvars(args.directory)))
    shutil.copytree(skel_dir, dest_dir, dirs_exist_ok=True)
    print('Initialized yaml2resume in %s' % dest_dir)

def generate(args):
    # We need to get a list of file names, but exclude config.yaml, since we know that isn't what we want/need.
    # This is in the case of people going yaml2resume gen *.yaml
    yaml_files = [os.path.abspath(os.path.expanduser(os.path.expandvars(x))) for x  in args.yamlfiles if not x.endswith('config.yaml')]
    resume = read_resumes(*yaml_files)
    print(resume)
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
    generate_parser.add_argument('-o', '--out-dir', metavar='OUT_DIR', default=None, help='Directory to output resume to')
    generate_parser.add_argument('-n', '--name', metavar='RESUME_NAME', default=None, help='Resume name')
    generate_parser.add_argument('-c', '--config', metavar='CONFIG', default='./config.yaml', help='Configuration file')

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
    elif args.command.startswith('gen'):
        generate(args)
    elif args.command == 'summary' or args.command == 'info':
        summary(args)
    elif args.command == 'check':
        check(args)
    else:
        raise ArgumentError('Unkown argument: %s' % args.command)
