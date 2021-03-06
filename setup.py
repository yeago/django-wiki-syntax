#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='django-wiki-syntax',
    version="0.1.2",
    author='Steve Yeago',
    author_email='subsume@gmail.com',
    description='Managing wiki-syntax situations in Django',
    url='http://github.com/subsume/django-wiki-syntax',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Topic :: Software Development"
    ],
)
