Detailed Description
********************

Setting up Grok projects as ``paster`` served WSGI applications
===============================================================

The main target of this package is to provide support for enabling
`Grok`_ applications to be run as `paster`_ served `WSGI`_
applications. To make this working some configuration files have to be
set up.

Setting up a project with ``grokproject``
-----------------------------------------

The most convenient way to setup a `Grok`_ project is using
`grokproject`_. Once installed, you can a project like this::

  $ grokproject Sample

which will generate all configuration files for you.

.. note:: Older versions of `grokproject`_ need an update

  As older versions of `grokproject`_ do not support
  `grokcore.startup`, you might want to update your existing
  `grokproject`_ installation by running::

    $ easy_install -U grokproject


Setting up a project manually
-----------------------------

Before we can make use of ``grokcore.startup``, we have to setup
several configuration files in the project root:

* ``setup.py``

* ``buildout.cfg`` (optional)

* ``zope.conf`` (normally found in the ``parts/etc/`` subdirectory of your
  `Grok`_ project)

* ``site.zcml`` (normally found in the ``parts/etc/`` subdirectory of your
  `Grok`_ project)

* ``deploy.ini`` (or any other .ini-file; normally found in the
  ``parts/etc/`` subdirectory of your `Grok`_ project)


When we want to setup a Zope instance as `paster`_ served `WSGI`_
application, then we have to set a ``paste.app_factory`` entry point
in ``setup.py``. A minimal setup could look like this::

  # setup.py
  from setuptools import setup, find_packages

  setup(name='sampleproject',
        version='0.1dev',
        description="A sample project",
        long_description="""Without a long description.""",
        classifiers=[],
        keywords="",
        author="U.N.Owen",
        author_email="",
        url="",
        license="",
        package_dir={'': 'src'},
        packages=find_packages('src'),
        include_package_data=True,
        zip_safe=False,
        install_requires=['setuptools',],
        entry_points = """
        [paste.app_factory]
        main = grokcore.startup:application_factory
        """,
        )

Here the `paste.app_factory` entry point pointing to
`grokcore.startup:application_factory` is important.

Furthermore we need at least a minimal ``buildout.cfg`` which enables
`zc.buildout`_ to create the control scripts for our instance::

  [buildout]
  develop = .
  parts = app

  [app]
  recipe = zc.recipe.egg
  eggs = sampleproject
         grokcore.startup
         Paste
         PasteScript
         PasteDeploy

Here an egg-entry for ``grokcore.startup`` **might** be important, if
it is not required otherwise by your application. Projects generated
by `grokproject`_ will automatically include such a dependency and
upcoming versions of `Grok`_ will pull in ``grokcore.startup`` anyway,
so that ``grokcore.startup`` would not be required in this list of
eggs any more.

Next we need ``site.zcml`` and ``zope.conf`` files to define the
Zope instance. These configurations are completely independent from
being served by `Paste`_ or not. If you are upgrading an old `Grok`_
project, you can use ``site.zcml`` and ``zope.conf`` of those project
as-is. You only have to take care of the maybe changed
``site-definition`` entry in ``zope.conf`` (see below).

The file ``site.zcml`` can be quite
short, but for real projects you certainly want to have some useful
content in here::

  <configure />

A short ``zope.conf`` file for use in tests could look like this::

  site-definition site.zcml

  <zodb>
    <mappingstorage />
  </zodb>

  <eventlog>
    <logfile>
      path STDOUT
     </logfile>
  </eventlog>

where the ``site-definition`` entry should point to the location of
the file ``site.zcml``. In regular Grok projects those files are put
into the ``etc/`` subdirectory of your project root.

Finally we have to provide a ``deploy.ini`` (or another .ini-file),
which tells paster where to find the pieces. This is also put into the
``etc/`` subdirectory of your project root in regular Grok projects
created by `grokproject`_::

  [app:main]
  use = egg:sampleproject

  [server:main]
  use = egg:Paste#http
  host = 127.0.0.1
  port = 8080

  [DEFAULT]
  zope_conf = %(here)s/zope.conf



API Documentation
=================

``application_factory(global_conf, **local_conf)``
--------------------------------------------------

  ``grokcore.startup`` provides a function ``application_factory``
  which delivers a `WSGIPublisherApplication`_ instance when called
  with an appropriate configuration. See the `zope.app.wsgi
  documentation
  <http://apidoc.zope.org/++apidoc++/Code/zope/app/wsgi/README.txt/index.html>`_
  to learn more about Zope objects supporting `WSGI`_.

  A call to this function is normally required as entry point in
  `setuptools`_-driven `paster`_ environments  (see
  http://pythonpaste.org/deploy/#paste-app-factory).

  We have to create our own site definition file -- which will simply
  be empty -- to provide a minimal test::

    >>> import os, tempfile
    >>> temp_dir = tempfile.mkdtemp()
    >>> sitezcml = os.path.join(temp_dir, 'site.zcml')
    >>> open(sitezcml, 'w').write('<configure />')

  Furthermore we create a Zope configuration file, which is also quite
  plain::

    >>> zope_conf = os.path.join(temp_dir, 'zope.conf')
    >>> open(zope_conf, 'wb').write('''
    ... site-definition %s
    ...
    ... <zodb>
    ...   <mappingstorage />
    ... </zodb>
    ...
    ... <eventlog>
    ...   <logfile>
    ...     path STDOUT
    ...   </logfile>
    ... </eventlog>
    ... ''' %sitezcml)

  Now we can call ``application_factory`` to get a WSGI application::

    >>> from grokcore.startup import application_factory
    >>> app_factory = application_factory({'zope_conf': zope_conf})
    >>> app_factory
    <zope.app.wsgi.WSGIPublisherApplication object at 0x...>

``debug_application_factory(global_conf, **local_conf)``
--------------------------------------------------------

  There's a second application factory that can be used when debugging
  the application, especially when using the ``z3c.evalexception`` middleware.

  When debugging zope is instructed not to handle any raised exceptions
  itself. The ``z3c.evalexception`` middleware then catches the exceptions
  and provides an user interfaces for debugging in the webbrowser.

  As a result also the IUnauthorized execption would not be handled by zope
  and the authentication mechanisms of zope are not triggered. As a result,
  when debugging one cannot login.

  The ``debug_application_factory`` function accepts the "exempt-exceptions"
  configuration option. The value for this option should be a comma seperated
  list of dotted names for each of the execptions that should *still* be
  handled by zope and not re-raised to be catched by the middleware.

    >>> from grokcore.startup import debug_application_factory
    >>> app_factory = debug_application_factory({'zope_conf': zope_conf})
    >>> app_factory
    <zope.app.wsgi.WSGIPublisherApplication object at 0x...>

    >>> from zope.interface import implements
    >>> from zope.security.interfaces import IUnauthorized
    >>> class UnauthorizedException(object):
    ...     implements(IUnauthorized)
    >>>
    >>> from zope.component import queryAdapter
    >>> from zope.publisher.interfaces import IReRaiseException

  Since the ``exempt-execptions`` configuration option was not passed,
  there's no IReRaiseException adapter registered for any type of exceptions
  including IUnauthorized:

    >>> error = UnauthorizedException()
    >>> reraise = queryAdapter(error, IReRaiseException, default=None)
    >>> reraise is None
    True

  When the option is passed, the adapter will be registered. Calling this
  adapter yields ``False``, telling zope not to reraise this particular
  exception.

    >>> app_factory = debug_application_factory(
    ...     {'zope_conf': zope_conf},
    ...     **{'exempt-exceptions': 'zope.security.interfaces.IUnauthorized'})
    >>>
    >>> reraise = queryAdapter(error, IReRaiseException, default=None)
    >>> reraise is None
    False
    >>> reraise()
    False

  Clean up the temp_dir

    >>> import shutil
    >>> shutil.rmtree(temp_dir)

``get_debugger(zope_conf_path)``
--------------------------------------------

  Get an interactive console with a debugging shell started.

  `grokcore.startup` provides two different debuggers currently: a
  plain one based on `zope.app.debug` and a more powerful `IPython`_
  debugger. The IPython debugger is automatically enabled if you have
  IPython available in the environment.

  You can explicitly enable the IPython_ debugger by stating::

    grokcore.startup [debug]

  in the install requirements of your `setup.py`, probably adding only
  ``[debug]`` to an already existing entry for
  `grokcore.startup`. Don't forget to rerun `buildout` afterwards.

  You can explicitly require one or the other debugger by calling::

    grokcore.startup.startup.interactive_debug_prompt(zope_conf)

  or::

    grokcore.startup.debug.ipython_debug_prompt(zope_conf)

  in the ``[interactive_debugger]`` section of your ``buildout.cfg``.

    >>> import zope.app.appsetup.appsetup
    >>> # Ugh - allow a reconfiguration of an app.
    >>> zope.app.appsetup.appsetup._configured = False

    >>> temp_dir = tempfile.mkdtemp()
    >>> sitezcml = os.path.join(temp_dir, 'site.zcml')
    >>> open(sitezcml, 'w').write(
    ...    """<configure xmlns="http://namespaces.zope.org/zope">
    ...   <include package="zope.component" file="meta.zcml"/>
    ...   <include package="zope.component"/>
    ...   <include package="zope.traversing"/>
    ...   <include package="zope.security" file="meta.zcml"/>
    ...   <include package="zope.security"/>
    ...   <include package="zope.container"/>
    ...   <include package="zope.site"/>
    ...   <include package="zope.app.appsetup"/>
    ... </configure>""")
    >>>
    >>> zopeconf = os.path.join(temp_dir, 'zope.conf')
    >>> open(zopeconf, 'w').write("""
    ...     site-definition %s
    ...     <zodb>
    ...       <filestorage>
    ...         path %s
    ...       </filestorage>
    ...     </zodb>
    ...     <eventlog>
    ...       <logfile>
    ...         path STDOUT
    ...         formatter zope.exceptions.log.Formatter
    ...       </logfile>
    ...     </eventlog>
    ...     """ % (sitezcml, os.path.join(temp_dir, 'Data.fs')))
    >>>
    >>> import sys
    >>> old_argv = sys.argv[:]
    >>>
    >>> script = os.path.join(temp_dir, 'script.py')
    >>> open(script, 'w').write(
    ...    """import sys
    ... from pprint import pprint
    ... pprint(debugger)
    ... pprint(app)
    ... pprint(root)
    ... pprint(sys.argv)
    ... pprint(__file__)
    ... pprint(__name__)""")
    >>>
    >>> sys.argv = ['get_debugger', script]
    >>> from grokcore.startup import interactive_debug_prompt
    >>> try:
    ...     interactive_debug_prompt(zope_conf=zopeconf)
    ... except SystemExit:
    ...     # Catch the exit from the interactive prompt as it would
    ...     # exit this test as well.
    ...     pass
    ------
    ...WARNING zope.app.appsetup Security policy is not configured.
    Please make sure that securitypolicy.zcml is included in site.zcml
    immediately before principals.zcml
    ...
    <zope.app.debug.debug.Debugger object at ...>
    <zope.app.debug.debug.Debugger object at ...>
    <zope.site.folder.Folder object at ...>
    ['...script.py']
    '...script.py'
    '__main__'

  Clean up the temp_dir

    >>> sys.argv = old_argv
    >>> import shutil
    >>> shutil.rmtree(temp_dir)

.. _grok: http://pypi.python.org/pypi/grok
.. _grokproject: http://pypi.python.org/pypi/grokproject
.. _Paste: http://pythonpaste.org/
.. _paster: Paste_
.. _setuptools: http://pypi.python.org/pypi/setuptools
.. _WSGI: http://www.wsgi.org/wsgi/
.. _WSGIPublisherApplication: http://apidoc.zope.org/++apidoc++/Code/zope/app/wsgi/WSGIPublisherApplication/index.html
.. _zc.buildout: http://pypi.python.org/pypi/zc.buildout
.. _ipython: http://ipython.org/
