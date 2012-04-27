# -*- coding: utf-8 -*-

import os
import sys
import logging
import ZConfig

from zope import component
from zope.site.hooks import setSite
from zope.site.interfaces import IRootFolder

from grokcore.view.publication import GrokBrowserPublication

from zope.app.appsetup import appsetup, product
from zope.publisher.interfaces import ISkinnable
from zope.app.wsgi import WSGIPublisherApplication
from zope.publisher.skinnable import setDefaultSkin
from zope.app.publication.httpfactory import chooseClasses


# XXX We have to subclass from WSGIPublisherApplication because the
#     ZODB-Stuff is very hard linked into it.
class NOZODBWSGIPublisherApplication(WSGIPublisherApplication):
    """
    """

    def __init__(self, handle_errors):
        self.handleErrors = handle_errors
        self.requestFactory = SimplePublicationRequestFactory()


class SimplePublicationRequestFactory(object):
    """ This Publication Request Factory does not have a link to
        ZODB.
    """

    def __call__(self, input_stream, env):
        method = env.get('REQUEST_METHOD', 'GET').upper()
        request_class, publication_class = chooseClasses(method, env)

        publication = BrowserPublication()
        request = request_class(input_stream, env)
        request.setPublication(publication)
        if ISkinnable.providedBy(request):
            # only ISkinnable requests have skins
            setDefaultSkin(request)
        return request


class BrowserPublication(GrokBrowserPublication):
    """ Browser Publication with NoZODB
    """

    def __init__(self):
        app = component.queryUtility(IRootFolder)
        if not app:
            raise NotImplementedError("""
                You have to register your own IRootFolder utility
                to be able to register your stuff on it:
                class AppRoot(grok.GlobalUtility):
                    grok.implements(IRootFolder)""")
        else:
            setSite(app)
            self._app = app

    def getApplication(self, request):
        return self._app


# Maybe we can include a smarter version
# in zope.app.wsgi.__init__ config for this...
def config(configfile, schemafile=None, features=()):
    # Load the configuration schema
    if schemafile is None:
        schemafile = os.path.join(
            os.path.dirname(appsetup.__file__), 'schema', 'schema.xml')

    # Let's support both, an opened file and path
    if isinstance(schemafile, basestring):
        schema = ZConfig.loadSchema(schemafile)
    else:
        schema = ZConfig.loadSchemaFile(schemafile)

    # Load the configuration file
    # Let's support both, an opened file and path
    try:
        if isinstance(configfile, basestring):
            options, handlers = ZConfig.loadConfig(schema, configfile)
        else:
            options, handlers = ZConfig.loadConfigFile(schema, configfile)
    except ZConfig.ConfigurationError, msg:
        sys.stderr.write("Error: %s\n" % str(msg))
        sys.exit(2)

    # Insert all specified Python paths
    if options.path:
        sys.path[:0] = [os.path.abspath(p) for p in options.path]

    # Parse product configs
    product.setProductConfigurations(
        options.product_config)

    # Setup the event log
    options.eventlog()

    # Setup other defined loggers
    for logger in options.loggers:
        logger()

    # Insert the devmode feature, if turned on
    if options.devmode:
        features += ('devmode',)
        logging.warning("Developer mode is enabled: this is a security risk "
            "and should NOT be enabled on production servers. Developer mode "
            "can usually be turned off by setting the `devmode` option to "
            "`off` or by removing it from the instance configuration file "
            "completely.")

    # Execute the ZCML configuration.
    appsetup.config(options.site_definition, features=features)
    return None
