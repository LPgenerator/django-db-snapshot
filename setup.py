from setuptools import setup, find_packages
from dbsnapshot import get_version


setup(
    name='django-db-snapshot',
    version=get_version(),
    description='Reusable Django app for fully automatic database snapshots',
    keywords="",
    long_description=open('README.rst').read(),
    author="GoTLiuM InSPiRiT",
    author_email='gotlium@gmail.com',
    url='https://github.com/LPgenerator/django-db-snapshot',
    packages=find_packages(exclude=['demo']),
    package_data={'dbsnapshot': [
        'locale/*/LC_MESSAGES/django.*',
    ]},
    include_package_data=True,
    install_requires=[
        'setuptools',
    ],
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],
)
