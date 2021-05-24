#!/usr/bin/env python3
import sys
import os
import shutil
import re
from glob import glob
from argparse import ArgumentError, ArgumentParser
from spellchecker import SpellChecker
from yaml2resume.helpers import get_yaml_abspath
from yaml2resume.parse import read_resumes, read_config
from yaml2resume.output import write_resume, print_summary
from yaml2resume import __version__ as VERSION

spellcheck_re  = re.compile('([a-zA-Z]+)')

def init(args):
    # copy the skel folder over and place inside the directory we init to
    module_dir = os.path.abspath(os.path.dirname(__file__))
    skel_dir = os.path.join(module_dir, 'skel')
    dest_dir = os.path.abspath(os.path.expanduser(os.path.expandvars(args.directory)))
    shutil.copytree(skel_dir, dest_dir, dirs_exist_ok=True)
    print('[+] Initialized yaml2resume in %s' % dest_dir)

def generate(args):
    config_file = os.path.abspath(os.path.expanduser(os.path.expandvars(args.config)))
    print('[+] Reading config (%s)' % config_file)
    config = read_config(config_file)
    # Read the resume yaml files, combining per the logic in the parser
    yaml_files = get_yaml_abspath(args.yamlfiles, config=config)
    print('[+] Using the following yaml files as inputs:')
    for filename in yaml_files:
        print('  [-] %s' % filename)
    resume = read_resumes(yaml_files)
    print('[+] Parsed resume yaml files')

    # Use jinja to output the resume
    write_resume(resume, config, out_dir=args.out_dir, resume_name=args.resume_name)

def check(args):
    config_file = os.path.abspath(os.path.expanduser(os.path.expandvars(args.config)))
    try:
        config = read_config(config_file)
        print('[-] Successfully read config file (%s)' % config_file)
    except Exception as e:
        print('[!] Failed to parse config file!!!')
        print('Exception details:\n %s' % e)
        sys.exit(-1)
    target_yamls = glob(os.path.join(os.getcwd(), '*.yaml'))
    yaml_files = get_yaml_abspath(target_yamls, config=config)
    print('[+] Checking each resume yaml file for validity and spelling')
    ignore_fields = config.get('spellcheck_ignore_fields', [])
    spell_check = SpellChecker()
    spell_check.word_frequency.load_words(config.get('spellcheck_dictionary', []))
    for yaml_file in yaml_files:
        spelling_error_count = 0
        print('  [+] Checking %s' % yaml_file)
        try:
            resume = read_resumes([yaml_file, ])
            print('    [-] Successfully parsed yaml file')
        except Exception as e:
            resume = {}
            print('    [!] Failed to parse file!!!')
            continue
        if not resume:
            print('    [!] Resume is blank!')
            continue
        for k, v in resume.items():
            field_text = ""
            if k in ignore_fields:
                continue
            elif k == 'work_history':
                for job in v:
                    field_text = job.get('company', '')
                    field_text += ' ' + job.get('title', '')
                    field_text += ' ' + job.get('summary', '')
                    field_text += ' ' + ' '.join(job.get('accomplishments', []))
            elif isinstance(v, list) and len(v) > 0:
                if isinstance(v[0], str):
                    field_text = " ".join(v)
            # print(field_text)
            spellcheck_words = spellcheck_re.findall(field_text)
            spellcheck_words = [x for x in spellcheck_words if len(x) > 1]
            spelling_errors = spell_check.unknown(spellcheck_words)
            if spelling_errors:
                print('    [!] Potentially misspelt words in %s: %s' % (k, ', '.join(spelling_errors)))
                spelling_error_count += 1
        if not spelling_error_count:
            print('    [-] No spelling issues found')

def summary(args):
    config_file = os.path.abspath(os.path.expanduser(os.path.expandvars(args.config)))
    print('[+] Reading config (%s)' % config_file)
    config = read_config(config_file)
    # Read the resume yaml files, combining per the logic in the parser
    yaml_files = get_yaml_abspath(args.yamlfiles, config=config)
    print('[+] Using the following yaml files as inputs:')
    for filename in yaml_files:
        print('  [-] %s' % filename)
    resume = read_resumes(yaml_files)
    print('[+] Parsed resume yaml files')
    print('-'*40)
    print_summary(resume, config)
    

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
    generate_parser.add_argument('-n', '--name', metavar='RESUME_NAME', default=None, dest='resume_name', help='Resume name')
    generate_parser.add_argument('-c', '--config', metavar='CONFIG', default='./config.yaml', help='Configuration file')

    # Check Subparser Arguments
    check_parser.add_argument('-c', '--config', metavar='CONFIG', default='./config.yaml', help='Configuration file')

    # Summary Subparser Arguments
    summary_parser.add_argument('yamlfiles', metavar='YAML_FILE', nargs='+', help='YAML files to generate resume from')
    summary_parser.add_argument('-c', '--config', metavar='CONFIG', default='./config.yaml', help='Configuration file')

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(-1)
    print('yaml2resume version %s\n' % VERSION)
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
