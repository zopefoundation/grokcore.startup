Changes
*******

5.1 (unreleased)
================

- Nothing changed yet.


5.0 (2025-06-18)
================

- Replace ``pkg_resources`` namespace with PEP 420 native namespace.


4.2 (2025-05-28)
================

- Add support for Python 3.13.

- Drop support for Python 3.7, 3.8.


4.1 (2024-05-22)
================

- Add support for Python 3.12.

- Update ``debug.py`` to run with ``IPython >= 8``. Also requiring at least
  that version of IPython.


4.0 (2023-07-14)
================

- Drop support for Python 2.7, 3.4, 3.5, 3.6.

- Add support for Python 3.7, 3.8, 3.9, 3.10, 3.11.


3.0.1 (2018-01-12)
==================

- Rearrange tests such that Travis CI can pick up all functional tests too.

3.0.0 (2018-01-10)
==================

- Python 3 compatibility.

1.2.1 (2016-02-15)
==================

- Update tests.

1.2 (2012-05-02)
================

- Added new IPython-based interactive debugger which is used
  automatically when IPython is available. Otherwise the gdb-style
  debugger is provided.

1.1 (2010-10-26)
================

- Drop zdaemon support.

- Close the database explicitely when execing a script through the
  ``interactive_debug_prompt``. This came to light in tests on Windows, as the
  tests would try to delete the temp directory it created with the still
  unclosed database file in there.

1.0.2 (2010-10-05)
==================

- Somehow the intended fix in 1.0.1 did not actually get included in that
  release. We make the fix again.

1.0.1 (2010-08-18)
==================

- When passing a script to the interactive_debug_prompt command, one would
  expect to be able to do: `if __name__ == '__main__':`, however __name__ would
  be "__builtin__". This is fixed.

1.0 (2010-05-20)
================

- Amend the interactive_debug_prompt function to behave more or less like the
  "old" zopectl command. Whenever there's commandline arguments passed to the
  command, the first one is assumed to be a python script that is 'execfile'd.
  This allows ad hoc scripts to run against the setup application.

- Make package comply to zope.org repository policy.

- The upgrade notes will be moved to the Grok upgrade notes.

- Define entry points for main and debug application factories in
  grokcore.startup.

- Use the groktoolkit.

0.4 (2009-10-06)
================

- Fix documentation bugs.

0.3 (2009-10-02)
================

* Add a ``debug_application_factory`` function that allows for the
  ``exempt-exceptions`` configuration option. The value for this option
  should be a comma seperated list of dotted names for each of the exceptions
  that should not be re-raised during debugging.

  This for one allow the IUnauthorized exception to still be handled by zope
  and thus have the normal authentication mechanisms still work.

* Bring versions.cfg in line with current grok versions.cfg.

0.2 (2009-02-21)
================

* Made main functions available package wide.

0.1 (2009-01-15)
================

* Added support for local ``zope_conf`` parameter.
  Fix bug https://bugs.launchpad.net/grok/+bug/320644

* Created ``grokcore.startup`` in January 2009 by factoring paster
  related application code out of grokcore templates.
