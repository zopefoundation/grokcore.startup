##############################################################################
#
# Copyright (c) 2006-2012 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
import os.path
import textwrap
from pprint import pprint

import transaction
import zope.app.debug
import zope.app.wsgi
from IPython.frontend.terminal.embed import InteractiveShellEmbed
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.securitypolicy.zopepolicy import settingsForObject


shell = InteractiveShellEmbed()


PATH_SEP = '/'


class GrokDebug:

    def __init__(self, debugger):
        debugger = debugger
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
                    sec=self.get_security_settings,
                    gu=getUtility,
                    gma=getMultiAdapter,
                    sync=self.sync,
                    pby=self.providedBy,
                    commit=transaction.commit)

    def update_ns(self):
        shell.user_ns.update(self.ns())

    def get_security_settings(self, path):
        pprint(settingsForObject(get_context_by_path(
                    self.get_start_context(path), path)))

    def sync(self):
        self.root._p_jar.sync()

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


def get_context_by_path(context, path):
    for name in (p for p in path.split(PATH_SEP) if p):
        context = context[name]
    return context


def path_completer(self, event):
    """TAB path completer for `cdg` and `lsg` commands."""
    relpath = event.symbol

    context = grokd.get_start_context(relpath)  # noqa: F821 undefined name

    # ends with '/'
    if relpath.endswith(PATH_SEP):
        context = get_context_by_path(context, relpath)
        return [relpath + obj.__name__ for obj in context.values()]

    head, tail = os.path.split(relpath)
    if head and not head.endswith(PATH_SEP):
        head += PATH_SEP
    context = get_context_by_path(context, head)

    return [head + obj.__name__ for obj in context.values()
            if obj.__name__.startswith(tail)]


def ipython_debug_prompt(debugger):
    grokd = GrokDebug(debugger)
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
          sec / ;sec
          gu  / ;gu
          gma / ;gma
          pby (providedBy)
          pwdg
          sync
          commit
        """)

    shell.user_ns.update(grokd.ns())
    shell.banner2 = banner
    shell.set_hook('complete_command', path_completer, re_key='.*cdg|.*lsg')
    shell(local_ns=grokd.ns())
