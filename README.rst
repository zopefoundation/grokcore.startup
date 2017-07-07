
grokcore.startup
****************

This package provides elements for starting a Grok project with
paster and WSGI.

That sounds simple but there is a huge amount going on under the hood.  

WSGI stands for Web Server Gateway Interface.  It provides for a standard 
way for any web server (including ones written in Python) 
to talk to any Python application.  

WSGI also allows one  to create 
middleware, these are python applications which speak 
WSGI on both the client and server sides.  
Existing WSGI Middleware include logging, exception handling, and html validators. 
It is also possible to chain together a web server, WSGI middleware, and a 
Python application server.  Or one can even use middleware to 
call  different Python application servers depending on the URL. 

Okay that explains WSGI.  So how do we manage WSGI servers?  WIth Python software called Paste, PasteScript, and PasteDeploy.  This is where grokcore.startup comes in.  It does all the work to invoke and configure  the Paste routines. 

To learn more about the WSGI 
standard, I encourage you to read 
`PEP 3333 <https://www.python.org/dev/peps/pep-3333/#abstract>`_
It is very nicely written. 


To learn more about Python Paste 
standard, you might find the
`Read the Docs  page <https://paste.readthedocs.io/en/latest/>`_
helpful.

And of course it is very helpful to read the 
`grokcore.startup <./src/grokcore/startup/README.rst>`_ documentation.

And if all of that still does not solve your problems, 
there is great detailed documentation over at the  
`Pyramid Pages on PasteDeploy <https://docs.pylonsproject.org/projects/pyramid/en/latest/narr/paste.html>`_.

Setting up ``grokcore.startup``
===============================

There is nothing special to setup this package.

All you have to do is, to make this package available during runtime.

With zc.buildout or other setuptools-related setups this can be
done by simply adding the package name grokcore.startup to the
required packages of your project in setup.py.



