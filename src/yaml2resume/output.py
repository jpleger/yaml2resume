#!/usr/bin/env python3
import os
import shutil
from glob import glob
from jinja2 import Environment, PackageLoader, select_autoescape

jinja_env = Environment(
    autoescape=select_autoescape()
)


def write_resume(resume, config, out_dir=None, resume_name=None):
    if not out_dir:
        out_dir = config.get('output_dir', 'output')
    if not resume_name:
        resume_name = config.get('resume_name', 'resume')
    out_dir = os.path.join(out_dir, resume_name)
    out_dir = os.path.abspath(os.path.expanduser(os.path.expandvars(out_dir)))
    templates_dir = os.path.join(os.getcwd(), config.get('templates_dir', 'templates'))
    static_dir = os.path.join(os.getcwd(), config.get('static_dir', 'static'))
    static_dir_out = os.path.join(out_dir, config.get('static_dir', 'static'))
    templates = glob('%s/*.j2' % templates_dir)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    print('[+] Copying static files')
    shutil.copytree(static_dir, static_dir_out, dirs_exist_ok=True)
    print('[+] Writing templates')
    for template_file in templates:
        file_extension = os.path.split(template_file)[1].strip('.j2')
        file_formatter = jinja_env.from_string(config.get('file_format', '{{ full_name }}.{{ extension }}'))
        file_name = file_formatter.render(**resume, extension=file_extension, config=config)
        template = jinja_env.from_string(open(template_file, 'r').read())
        file_path = os.path.join(out_dir, file_name)
        with open(file_path, 'w') as fd:
            fd.write(template.render(**resume))
        print('  [-] Saved %s' % file_path)
    print('[+] Successfully wrote resume to %s' % out_dir)

def print_summary(resume, config):
    module_dir = os.path.abspath(os.path.dirname(__file__))
    template = jinja_env.from_string(open(os.path.join(module_dir, "summary.j2"), 'r').read())
    print(template.render(**resume, config=config))
    print('\n')
