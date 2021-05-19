# yaml2resume

yaml2resume is a simple python app that takes a resume in a YAML file and then renders it using jinja2 templates. The app supports appending resume content, using different yaml files, so that resumes can be customized based off the role being applied to (think a manager vs. devops role). This tool supports outputting different file formats (by default an HTML and TXT template are provided), which can be used to make outputs flexible.

This is geared towards software developers or technical engineers that want to have a simple way to manage/customize their resume, but still have something that looks professional.

## How it works

### Installation

```
pip3 install yaml2resume
```

### Usage

```
cd ~/vcs/resume
# Create the resume
yaml2resume init
# start a simple http server to work on the resume
yaml2resume dev
```

### Customizing your resume

Configuration file details



