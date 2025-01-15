import os

from setuptools import find_packages
from setuptools import setup


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


long_description = (
    read('README.rst') + '\n' +
    read(os.path.join('src', 'grokcore', 'startup', 'README.rst')) + '\n' +
    read('CHANGES.rst'))

tests_require = [
    'zope.app.appsetup',
    'zope.component',
    'zope.interface',
    'zope.security',
    'zope.securitypolicy',
    'zope.testing',
    'zope.testrunner',
]

debug_requires = [
    'IPython >= 8',
]

setup(
    name='grokcore.startup',
    version='4.2.dev0',
    author='Grok Team',
    author_email='zope-dev@zope.dev',
    url='https://github.com/zopefoundation/grokcore.startup',
    description='Paster support for Grok projects.',
    long_description=long_description,
    license='ZPL',
    keywords='zope zope3 grok grokproject WSGI Paste paster',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Zope :: 3',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['grokcore'],
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.9',
    install_requires=[
        'setuptools',
        'zope.app.debug',
        'zope.app.wsgi',
        'zope.component',
        'zope.dottedname',
        'zope.publisher',
    ],
    extras_require=dict(test=tests_require, debug=debug_requires),
    entry_points={
        'paste.app_factory': [
            'main = grokcore.startup:application_factory',
            'debug = grokcore.startup:debug_application_factory',
        ]
    },
)
