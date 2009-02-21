from setuptools import setup, find_packages
import os

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
    'zope.app.testing',
    'zope.component',
    ]

setup(
    name='grokcore.startup',
    version='0.2',
    author='Grok Team',
    author_email='grok-dev@zope.org',
    url='http://grok.zope.org',
    download_url='http://pypi.python.org/pypi/grokcore.startup',
    description='Paster support for Grok projects.',
    long_description=long_description,
    license='ZPL',
    keywords='zope zope3 grok grokproject WSGI Paste paster',
    classifiers=['Intended Audience :: Developers',
                 'License :: OSI Approved :: Zope Public License',
                 'Programming Language :: Python',
                 'Framework :: Zope3',
                 ],

    packages=find_packages('src'),
    package_dir = {'': 'src'},
    namespace_packages=['grokcore'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['setuptools',
                      'zdaemon',
                      'zope.app.wsgi',
                      'zope.app.debug',
                      ],
    tests_require = tests_require,
    extras_require = dict(test=tests_require),
)
