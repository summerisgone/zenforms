# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):

    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()

    except IOError:
        return ''

setup(
    name="django-zenforms",

    version=__import__('zenforms').__version__,
    description=read('DESCRIPTION'),

    license="GPL",
    keywords="django forms zen uniform",

    author="Ivan Gromov",

    author_email="ivan.gromov@redsolution.ru",

    maintainer='Ivan Gromov',
    maintainer_email='ivan.gromov@redsolution.ru',

    url="http://github.com/summerisgone/zenforms",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',

        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Framework :: Django',
        'Environment :: Web Environment',
        'Natural Language :: Russian',
        'Natural Language :: English',

        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    packages=find_packages(exclude=['example', 'example.*']),

    install_requires=['django-classy-tags',],
    include_package_data=True,
    zip_safe=False,
    long_description=read('README'),
)