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
                                      debug_application_factory)

def get_debugger(zope_conf):
    try:
        import IPython
        from grokcore.startup.debug import GrokDebug
        grokd = GrokDebug(zope_conf)
        from grokcore.startup.debug import interactive_debug_prompt
        return interactive_debug_prompt(zope_conf, grokd)
    except ImportError:
        from grokcore.startup.startup import interactive_debug_prompt
        return interactive_debug_prompt(zope_conf)
