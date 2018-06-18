# -*- coding: utf-8 -*-

# Third
from setuptools import find_packages, setup

__version__ = '0.1.0'
__description__ = 'Api Python Flask'
__long_description__ = 'This is an API to Flask Api Users'

__author__ = 'Lucas Simon'
__author_email__ = 'lucassrod@gmail.com'

testing_extras = [
    'pytest',
    'pytest-cov',
]

setup(
    name='api',
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    packages=find_packages(),
    license='MIT',
    description=__description__,
    long_description=__long_description__,
    url='https://github.com/lucassimon/flask-api-users.git',
    keywords='API, MongoDB',
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
        'Environment :: Web Environment',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    extras_require={
        'testing': testing_extras,
    },
)
