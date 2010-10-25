import os.path
import sys
import code
import zope.app.wsgi
import zope.app.debug

from zope.component import provideAdapter
from zope.publisher.interfaces import IReRaiseException
from zope.dottedname.resolve import resolve

def application_factory(global_conf, **local_conf):
    zope_conf = local_conf.get('zope_conf', global_conf.get(
            'zope_conf', os.path.join('parts', 'etc', 'zope.conf')))
    return zope.app.wsgi.getWSGIApplication(zope_conf)


def debug_application_factory(global_conf, **local_conf):
    # First create the application itself
    app = application_factory(global_conf, **local_conf)
    # Then register the IReRaiseException adaptation for
    # various types of exceptions that are exempt from being
    # raised by the publisher.
    def do_not_reraise_exception(context):
        return lambda : False
    iface_names = local_conf.get('exempt-exceptions', '').split(',')
    for name in iface_names:
        name = name.strip()
        if not name:
            continue
        iface = resolve(name)
        provideAdapter(do_not_reraise_exception, (iface, ), IReRaiseException)
    # Return the created application
    return app

def interactive_debug_prompt(
    zope_conf=os.path.join('parts', 'etc', 'zope.conf')):

    db = zope.app.wsgi.config(zope_conf)
    debugger = zope.app.debug.Debugger.fromDatabase(db)
    globals_ = {
        'debugger': debugger,
        'app': debugger,
        'root': debugger.root()}

    if len(sys.argv) > 1:
        # There're arguments passed to the command. We replicate the
        # "old" zopectl run command behaviour that would execfile()
        # the second argument.

        # The current first argument is the interactive_debugger command
        # itself. Pop it from the args list and as a result, the script
        # to run is the first argument.
        del sys.argv[0]

        globals_['__name__'] = '__main__'
        globals_['__file__'] = sys.argv[0]
        execfile(sys.argv[0], globals_)

        # Housekeeping.
        db.close()
        sys.exit()

    # Invoke an interactive interpreter prompt
    banner = (
        "Welcome to the interactive debug prompt.\n"
        "The 'root' variable contains the ZODB root folder.\n"
        "The 'app' variable contains the Debugger, 'app.publish(path)' "
        "simulates a request.")
    code.interact(banner=banner, local=globals_)
