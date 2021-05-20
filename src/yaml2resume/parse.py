#!/usr/bin/env python3
import yaml
import dateparser
import os
from glob import glob

def merge_work_history(work_history):
    required_fields = ['company', 'title', 'start']
    # Setup a dict that we can use with unique keys so we can deduplicate (company, title, start)
    if len(work_history) <= 1:
        return work_history
    combined_work_history = {}
    for job in work_history:
        # Check if the fields aren't in the required fields
        if False in [x in job for x in required_fields]:
            raise KeyError('Missing required key in %s' % job)
        key = "|".join([job[x] for x in required_fields])
        # If this is a new job, add it to the list and move on to the next one.
        if key not in combined_work_history:
            combined_work_history[key] = job
            continue
        # Grab the item for the combined job so we can work on the items (specificially the accomplishments)
        c_job = combined_work_history[key]
        if 'accomplishments' in job and isinstance(job['accomplishments'], list):
            accomplishments = job.pop('accomplishments')
            if 'accomplishments' in c_job:
                c_job['accomplishments'].extend(accomplishments)
            else:
                c_job['accomplishments'] = accomplishments
        # If there are items inside the dictionary, then add them, otherwise use the first instance seen.
        for k, v in job.items():
            if k not in c_job:
                c_job[k] = v

    # Lets parse the dates, so we are working with a normalized date.
    for k, job in combined_work_history.items():
        if 'start' in job:
            job['start_parsed'] = dateparser.parse(job['start'], settings={'PREFER_DAY_OF_MONTH': 'first'})
        end = None
        if 'end' in job:
            end = dateparser.parse(job['end'], settings={'PREFER_DAY_OF_MONTH': 'last'})
        if not end:
            end = dateparser.parse('now')
        job['end_parsed'] = end
        # For each one of the jobs in the combined work history, we need to create a parsed date, which we will use to sort.
        dateparser.parse('5/2020', settings={'PREFER_DAY_OF_MONTH': 'first'})
    return sorted(combined_work_history.values(), key=lambda k: k['end_parsed'], reverse=True)
    
def merge_resumes(*resumes):
    resumes = list(resumes)
    if len(resumes) <= 1:
        return resumes
    if False in [isinstance(x, dict) for x in resumes]:
        raise ValueError('Resume should be a dict')
    resume_merged = resumes.pop(0)
    for resume in resumes:
        for k, v in resume.items():
            if k not in resume_merged:
                resume_merged[k] = v
            elif isinstance(v, list) and isinstance(resume_merged[k], list):
                resume_merged[k].extend(v)
    if 'work_history' in resume_merged:
        resume_merged['work_history'] = merge_work_history(resume_merged['work_history'])
    return resume_merged

def read_resumes(*filenames):
    file_list = []
    # Expand the user and any vars from the filnames that are passed into the function
    for filename in [os.path.expanduser(os.path.expandvars(x)) for x in filenames]:
        file_list.extend(glob(filename))
    # Create a unique list of filenames
    file_list = list(set(file_list))
    # Make sure we don't accidentally send a config.yaml into the file list
    file_list = [x for x in file_list if not x.endswith('config.yaml')]
    # Placeholder for invalid files
    invalid_files = []
    for filename in file_list:
        if not os.path.isfile(filename):
            invalid_files.append(filename)
    if invalid_files:
        raise FileNotFoundError('Invalid files: %s' % ", ".join(invalid_files))
    yaml_resumes = []
    for filename in file_list:
        yaml_resumes.append(yaml.load(open(filename, 'r'), Loader=yaml.SafeLoader))
    parsed_resumes = merge_resumes(*yaml_resumes)