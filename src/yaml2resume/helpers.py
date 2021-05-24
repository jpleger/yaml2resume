#!/usr/bin/env python3
import os

def get_yaml_abspath(yaml_files, config = {}):
    # We need to get a list of file names, but exclude config.yaml, since we know that isn't what we want/need.
    # This is in the case of people going yaml2resume gen *.yaml
    yaml_files = [os.path.abspath(os.path.expanduser(os.path.expandvars(x))) for x  in yaml_files if not x.endswith('config.yaml')]
    base_resumes = config.get('include_always', [])
    # If there are include_always resume configs, make sure that they are part of the yaml_files list
    for r in base_resumes:
        r = os.path.abspath(os.path.expanduser(os.path.expandvars(r)))
        if r not in yaml_files:
            yaml_files.append(r)
    return yaml_files
