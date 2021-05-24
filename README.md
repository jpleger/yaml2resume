# yaml2resume

yaml2resume is a simple python app that takes a resume in a YAML formatted file and then renders it using jinja2 templates. The primary use-case is for engineers, managers or other technical users who have diverse skillsets, but might be want to provide a targeted resume for a specific job post, highlighting specific skills or relevant work experience.

By default, an HTML (suitable for exporting to PDF) and TXT template (for copying and pasting text) are provided. yaml2resume is also designed to be used in conjunction with a version control system such as git, to provide version tracking.

A sample use case might be a software engineer looking to move to a devops engineer role. Using yaml2resume the user can define skills and bucket them by category (such as `python.yaml`, `kubernetes.yaml`, `scrum_master.yaml`, `aws.yaml`, `security.yaml`, `blogging.yaml`), then generate a resume that is tailored to each role.

## Things to note

Keep in mind when using the generate function that the first yaml file will appear first in your output. For example if you invoke yaml2resume by using `yaml2resume base.yaml technical.yaml`, the contents of `base.yaml` will appear first, which might not be what you want. Be aware that using shell globbing, sometimes the order will not be what you are looking for.

### Installation

```shell
pip3 install yaml2resume
```

### Usage

```shell
cd ~/vcs/resume
# Initialize the resume
yaml2resume init
# Generate the resume, outputting to the output directory (defined in config.yaml)
yaml2resume generate *.yaml
# Spell check/verify yaml files are all in good working order
yaml2resume check

```

### Customizing your resume

Once you have initialized your resume, note the config.yaml. This file is commented fairly well, but there are a couple key configuration options to keep in mind:

| Field Name | Description |
|------------|-------------|
| output_dir | This is the directory that the resume templates are outputted to (defaults to `output`) |
| resume_name | This is the default resume name that is used (defaults to `resume`) |
| file_format | This is a jinja formatted output for the resume, including the extension of the template |
| static_dir | The static directory gets copied over to each resume generated |
| template_dir | Where yaml2resume will look for templates (in current working directory) |
| include_always | These resume yaml files will always be included, useful for things like certs or generic info like phone/name |
| spellcheck_dictionary | A list of words to be added to the spellchecking dictionary |
| spellcheck_ignore_fields | Any fields to ignore spellchecking on |

### Organizing your resume

Since the yaml files can be pulled in by globs, you can organize using buckets and globs.

For example, if you have a list of files like:

- `01_devops_kube.yaml`
- `02_devops_monitoring.yaml`
- `03_devops_security.yaml`

You could then use something like `yaml2resume *devops*.yaml` and pull in all the relevant resume items.
