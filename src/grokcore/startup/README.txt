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
    >>> app_factory = application_factory(dict(zope_conf = zope_conf))
    >>> app_factory
    <zope.app.wsgi.WSGIPublisherApplication object at 0x...>


``interactive_debug_prompt(zope_conf_path)``
--------------------------------------------

  Get an interactive console with a debugging shell started.

  Normally used as entry point in projects ``setup.py``.

  The debugger will be started with the configuration given in
  `zope.conf_path`.

  We cannot start an interactive console here, but we can at least
  import the debugger function::

    >>> from grokcore.startup import interactive_debug_prompt

``zdaemon_controller(zdaemon_conf_path)``
-----------------------------------------

  Wrapper function to start a zdaemon.

  Normally used as entry point in projects ``setup.py``.

  The zdaemon is started using the given configuration in
  `zdaemon_conf_path`.

  We do not start a complete environment here, but we can at least
  import the wrapper function::

    >>> from grokcore.startup import zdaemon_controller

  Clean up::

    >>> import shutil
    >>> shutil.rmtree(temp_dir)


Update Instructions
*******************

If you want to update an existing Grok project to make use of
``grokcore.startup``, then there are several possibilites depending on
what version of `grokproject_` you used to create the project.

First you have to make sure, that ``grokcore.startup`` is installed
locally and loaded on startup. This can be done by adding::

  grokcore.startup

to the list of requirements of your project in ``setup.py``.

Upcoming versions of Grok (> 1.0a1) will require ``grokcore.startup``
anyway, so that if you use `grok`_ > 1.0.a1 then you can skip this
step.

Projects with a ``startup.py`` file
===================================

If you can find a file ``startup.py`` in your Grok application
sources, then chances are good, that your project was already created
with paster support (and you should be able to find an ``etc/``
configuration directory in your project root) and you can do an update
in three steps:

1) In your project's ``setup.py`` add a dependency to
   ``grokcore.startup``.

2) In your project's ``setup.py`` modify the lines reading::

      [paste.app_factory]
      main = <myapplication>.startup:application_factory

  to::

      [paste.app_factory]
      main = grokcore.startup:application_factory

  and rerun buildout::

      $ bin/buildout

2) Remove ``startup.py`` from your application sources.


Projects without a ``startup.py`` file
======================================

Here the situation is more tricky, because you have to generate all
the configuration files needed py `Paste`_.

You can setup those files manually following the instructions above or
simply create a new grokproject with the same name and copy all source
files (i.e. the stuff below your ``src/`` directory) over to the new
project directory.

If you decide to switch manually, then chances are that you can reuse
**parts** of your old ``zope.conf`` or ``site.zcml`` files (located
somewhere in the ``parts/`` directory) but overall it might be faster
(and less error-prone) to simply create a new project with the same
name using a recent `grokproject`_ and copying the old sources (inside
the ``src/`` directory) over.

Afterwards you should also rerun buildout to make all changes active::

  $ bin/buildout


.. _grok: http://pypi.python.org/pypi/grok
.. _grokproject: http://pypi.python.org/pypi/grokproject
.. _Paste: http://pythonpaste.org/
.. _paster: Paste_
.. _setuptools: http://pypi.python.org/pypi/setuptools
.. _WSGI: http://www.wsgi.org/wsgi/
.. _WSGIPublisherApplication: http://apidoc.zope.org/++apidoc++/Code/zope/app/wsgi/WSGIPublisherApplication/index.html
.. _zc.buildout: http://pypi.python.org/pypi/zc.buildout
