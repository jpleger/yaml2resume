import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yaml2resume", # Replace with your own username
    version="0.0.8",
    author="James Pleger",
    author_email="jpleger@gmail.com",
    description="Take yaml files and convert them into a resume",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jpleger/yaml2resume",
    project_urls={
        "Bug Tracker": "https://github.com/jpleger/yaml2resume/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # Since we have directories in the skel folder, I don't want to deal with 
    # having to use the setuptools package resource to copy every single one of the files
    zip_safe=False,
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    # Include extra package data
    include_package_data=True,
    package_data={
        # Include skeleton files
        "": ["skel/*", "skel/static/*", "skel/static/.placeholder", "skel/templates/*"],
    },
    entry_points = {
        'console_scripts': ['yaml2resume=yaml2resume.cli:main'],
    },
    python_requires=">=3.6",
    install_requires=[
        "Jinja2>=2.11.3",
        "PyYAML>=5.4.1",
        "pyspellchecker>=0.6.2",
    ],
)
