"""

Development
===========
Source code is hosted in `GitHub <https://github.com/dcrosta/flask-pymongo>`_
(contributions are welcome!)
"""

from setuptools import find_packages, setup

setup(
    name='SpaceShare',
    version='0.4',
    url='spaceshare.me',
    download_url='https://github.com/davidawad/spaceshare/',
    license='BSD',
    author='David Awad',
    author_email='davidawad64@gmail.com',
    description='Flask Applications using MongoDB',
    long_description=__doc__,
    zip_safe=False,
    platforms='any',
    packages=find_packages(),
    install_requires=[
        'Flask >= 0.8',
        'pymongo >= 2.4',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    setup_requires=['nose'],
    tests_require=['nose', 'coverage'],
    test_suite='nose.collector',
)
