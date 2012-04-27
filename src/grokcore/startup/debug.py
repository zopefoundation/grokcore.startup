#######################################################################
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#######################################################################
import sys
import os.path
import textwrap

import transaction
import zope.app.wsgi
import zope.app.debug
from pprint import pprint
from zope.securitypolicy.zopepolicy import settingsForObject

from IPython.frontend.terminal.embed import InteractiveShellEmbed
shell = InteractiveShellEmbed()


PATH_SEP = '/'

class GrokDebug(object):

    def __init__(self, zope_conf='parts/etc/zope.debug.conf'):
        db = zope.app.wsgi.config(zope_conf)
        debugger = zope.app.debug.Debugger.fromDatabase(db)
        self.app = debugger
        self.root = debugger.root()
        self.context = self.root

    def get_start_context(self, path):
        if path.startswith(PATH_SEP):
            context = self.root
        else:
            # relative path
            context = self.context
        return context

    def _get_object_names(self, context):
        return [obj.__name__ for obj in context.values()]

    def ns(self):
        """Return namespace dictionary.

        To be used for updating namespace of commands available
        for user in shell.
        """
        return dict(lsg=self.ls,
                    cdg=self.cd,
                    pwdg=self.pwd,
                    app=self.app,
                    root=self.root,
                    ctx=self.ctx,
                    security=self.get_security_settings,
                    sync=self.sync,
                    providedBy=self.providedBy,
                    commit=self.commit)

    def update_ns(self):
        shell.user_ns.update(self.ns())

    def get_security_settings(self):
        pprint(settingsForObject(self.ctx))

    def sync(self):
        self.root._p_jar.sync()

    def commit(self):
        transaction.commit()

    def ls(self, path=None):
        """List objects.

        This command is bound to `lsg` in IPython shell.

        Without `path` parameter list objects in current container,
        which is available as `ctx` from IPython shell.

        `path` can be relative or absolute.

        To use autocompletion of path command should be invoked
        with prepended semicolon in ipython shell as
        ;lsg /path
        """
        if path is None:
            return self._get_object_names(self.context)

        context = get_context_by_path(self.get_start_context(path), path)
        return self._get_object_names(context)


    def cd(self, path):
        """cd to specified path.

        Bound to `cdg` in IPython shell.
        `path` can be relative or absolute.

        To use autocompletion of path command should be invoked
        with prepended semicolon in ipython shell as
        ;cdg /path
        """
        if path.strip() == '..':
            self.context = self.context.__parent__
            self.update_ns()
            return self.pwd

        # cd
        self.context = get_context_by_path(self.get_start_context(path), path)
        self.update_ns()
        return self.pwd

    @property
    def pwd(self):
        """Print absolute path to current context object.

        Bound to `pwdg` in IPython shell
        """
        res = []
        obj = self.context
        while obj is not None:
            name = obj.__name__
            if name is not None and name:
                res.append(name)
            obj = obj.__parent__

        if not res:
            return PATH_SEP

        res = PATH_SEP.join(reversed(res))
        if not res.startswith(PATH_SEP):
            return PATH_SEP + res

        return res

    @property
    def ctx(self):
        """Return current context object.

        Bound to `ctx` in IPython shell
        """
        return self.context

    def providedBy(self, obj=None):
        if not obj:
            obj = self.ctx
        return list(zope.interface.providedBy(obj)) 



grokd = GrokDebug()

def get_context_by_path(context, path):
    for name in (p for p in path.split(PATH_SEP) if p):
        context = context[name]
    return context

def path_completer(self, event):
    """TAB path completer for `cdg` and `lsg` commands."""
    relpath = event.symbol

    context = grokd.get_start_context(relpath)

    # ends with '/'
    if relpath.endswith(PATH_SEP):
        context = get_context_by_path(context, relpath)
        return [relpath+obj.__name__ for obj in context.values()]

    head, tail = os.path.split(relpath)
    if head and not head.endswith(PATH_SEP):
        head += PATH_SEP
    context = get_context_by_path(context, head)

    return [head+obj.__name__ for obj in context.values()
            if obj.__name__.startswith(tail)]


def interactive_debug_prompt(zope_conf):
    banner = textwrap.dedent(
        """\
        IPython shell for Grok.

        Bound object names:
        -------------------
          root
          ctx

        Bound command names:
        --------------------
          cdg / ;cdg
          lsg / ;lsg
          providedBy
          security
          pwdg
          sync
          commit
        """)

    shell.user_ns.update(grokd.ns())
    shell.banner2=banner
    shell.set_hook('complete_command', path_completer, re_key='.*cdg|.*lsg')
    shell(local_ns=grokd.ns())
