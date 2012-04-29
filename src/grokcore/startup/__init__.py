##############################################################################
#
# Copyright (c) 2006-2007 Zope Foundation and Contributors.
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
# Make this a package.
from grokcore.startup.startup import (application_factory,
                                      debug_application_factory,
                                      interactive_debug_prompt,)



def get_debugger(zope_conf):
    """Get an interactive debugger.

    If IPython is available you get an IPython-based debugger with
    lots of fancy features (see :mod:`grokcore.startup.debug` for
    details.

    Otherwise you get a plain debugger in pdb style.
    """
    try:
        import IPython
    except ImportError:
        return interactive_debug_prompt(zope_conf)
    # late import: the debug module is only importable with IPython
    # available.
    from grokcore.startup.debug import ipython_debug_prompt
    return ipython_debug_prompt(zope_conf)

