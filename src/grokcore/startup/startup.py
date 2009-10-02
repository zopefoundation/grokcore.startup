import os.path
import sys
import code
import zdaemon.zdctl
import zope.app.wsgi
import zope.app.debug

from zope.component import provideAdapter
from zope.security.interfaces import IUnauthorized
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
    

def interactive_debug_prompt(zope_conf=os.path.join('parts', 'etc',
                                                    'zope.conf')):
    db = zope.app.wsgi.config(zope_conf)
    debugger = zope.app.debug.Debugger.fromDatabase(db)
    # Invoke an interactive interpreter shell
    banner = ("Welcome to the interactive debug prompt.\n"
              "The 'root' variable contains the ZODB root folder.\n"
              "The 'app' variable contains the Debugger, 'app.publish(path)' "
              "simulates a request.")
    code.interact(banner=banner, local={'debugger': debugger,
                                        'app':      debugger,
                                        'root':     debugger.root()})

class ControllerCommands(zdaemon.zdctl.ZDCmd):

    def do_debug(self, rest):
        interactive_debug_prompt()

    def help_debug(self):
        print "debug -- Initialize the application, providing a debugger"
        print "         object at an interactive Python prompt."

def zdaemon_controller(zdaemon_conf=os.path.join('parts', 'etc',
                                                 'zdaemon.conf')):
    args = ['-C', zdaemon_conf] + sys.argv[1:]
    zdaemon.zdctl.main(args, options=None, cmdclass=ControllerCommands)
