# yaml2resume

yaml2resume is a simple python app that takes a resume in a YAML file and then renders it using jinja2 templates. This app supports inheriting a base resume and having a number of different customized resumes based off the role being applied to (think a manager vs. devops role). Since many job sites suck, it is nice to have a well formatted text and PDF version of resumes that can easily be submitted, without having to manually keep them in sync.

This is geared towards software developers or technical engineers that want to have a simple way to manage/customize their resume, but still have something that looks professional.

## How it works

### Installation

```
pip install yaml2resume
```

### Usage

```
cd ~/vcs/resume
# Create the resume
yaml2resume init
# start a simple http server to work on the resume
yaml2resume serve
```

### Customizing your resume

Configuration file details



