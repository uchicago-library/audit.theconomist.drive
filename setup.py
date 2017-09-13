from setuptools import setup

def _readme():
    with open("README.md", "r") as read_file:
        return read_file.read()

setup(
    name="auditing_the_economist_files",
    author="Tyler Danstrom",
    author_email="tdanstrom@uchicago.edu",
    version="1.0.0",
    license="LGPL3.0",
    description="A command-line script to generate Simple Archive Format directory for " +\
                "ingesting Proquest disseratations to a DSpace repository",
    long_description=_readme(),
    keywords="python3.5 SimpleArchiveFormat generation csv proquest",
    scripts=['bin/saf-generation.py'],
    classifiers=[
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "Operating System :: POSIX :: Linux",
        "Topic :: Text Processing :: Markup :: XML",
    ]
)
