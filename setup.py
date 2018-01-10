import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


long_description = (
    read('README.txt')
    + '\n' +
    read(os.path.join('src', 'grokcore', 'startup', 'README.txt'))
    + '\n' +
    read('CHANGES.txt')
    )


tests_require = [
    'zope.app.appsetup',
    'zope.component',
    'zope.interface',
    'zope.security',
    'zope.securitypolicy',
    'zope.testing',
    ]


debug_requires = [
    'IPython',
    ]

setup(
    name='grokcore.startup',
    version='3.0.0',
    author='Grok Team',
    author_email='grok-dev@zope.org',
    url='http://grok.zope.org',
    download_url='http://pypi.python.org/pypi/grokcore.startup',
    description='Paster support for Grok projects.',
    long_description=long_description,
    license='ZPL',
    keywords='zope zope3 grok grokproject WSGI Paste paster',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Framework :: Zope3',
        ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['grokcore'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'zope.app.debug',
        'zope.app.wsgi',
        'zope.component',
        'zope.dottedname',
        'zope.publisher',
        ],
    tests_require=tests_require,
    extras_require=dict(test=tests_require, debug=debug_requires),
    entry_points={
        'paste.app_factory': [
            'main = grokcore.startup:application_factory',
            'debug = grokcore.startup:debug_application_factory',
            ]
    },
)
