import code
import os.path
import sys

import zope.app.debug
import zope.app.wsgi
from zope.component import provideAdapter
from zope.dottedname.resolve import resolve
from zope.publisher.interfaces import IReRaiseException


def application_factory(global_conf, **local_conf):
    zope_conf = local_conf.get(
        'zope_conf',
        global_conf.get('zope_conf',
                        os.path.join('parts', 'etc', 'zope.conf')))
    return zope.app.wsgi.getWSGIApplication(zope_conf)


def debug_application_factory(global_conf, **local_conf):
    # First create the application itself
    app = application_factory(global_conf, **local_conf)
    # Then register the IReRaiseException adaptation for
    # various types of exceptions that are exempt from being
    # raised by the publisher.

    def do_not_reraise_exception(context):
        return lambda: False
    iface_names = local_conf.get('exempt-exceptions', '').split(',')
    for name in iface_names:
        name = name.strip()
        if not name:
            continue
        iface = resolve(name)
        provideAdapter(do_not_reraise_exception, (iface, ), IReRaiseException)
    # Return the created application
    return app


def _classic_debug_prompt(debugger):
    globals_ = {
        'debugger': debugger,
        'app': debugger,
        'root': debugger.root()}
    # Invoke an interactive interpreter prompt
    banner = (
        "Welcome to the interactive debug prompt.\n"
        "The 'root' variable contains the ZODB root folder.\n"
        "The 'app' variable contains the Debugger, 'app.publish(path)' "
        "simulates a request.")
    code.interact(banner=banner, local=globals_)


def _ipython_debug_prompt(debugger):
    from grokcore.startup.debug import ipython_debug_prompt
    return ipython_debug_prompt(debugger)


def interactive_debug_prompt(zope_conf):
    db = zope.app.wsgi.config(zope_conf)
    debugger = zope.app.debug.Debugger.fromDatabase(db)
    if len(sys.argv) > 1:
        # There're arguments passed to the command. We replicate the
        # "old" zopectl run command behaviour that would execfile()
        # the second argument.
        globals_ = {
            'debugger': debugger,
            'app': debugger,
            'root': debugger.root()}
        # The current first argument is the interactive_debugger command
        # itself. Pop it from the args list and as a result, the script
        # to run is the first argument.
        del sys.argv[0]
        globals_['__name__'] = '__main__'
        globals_['__file__'] = sys.argv[0]
        with open(sys.argv[0]) as f:
            exec(f.read(), globals_)
        # Housekeeping.
        db.close()
        sys.exit()
    # Start the interpreter.
    try:
        import IPython  # noqa: F401 imported but unused
    except ImportError:
        return _classic_debug_prompt(debugger)
    return _ipython_debug_prompt(debugger)
