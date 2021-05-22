==========
git-semantic-version
==========

Retrieving semantic versioning from git tags

Usage:
-----

::

    $git semver -h
    usage: git semver [-h] [--debug] [--tags] [--first-parent] [--abbrev <n>] [--match [<pattern> ...]] [--exclude [<pattern> ...]] [commitish ...]

positional arguments:

commitish
    Commit-ish object names to describe. Defaults to HEAD if omitted.

optional arguments:

-h, --help           show this help message and exit
--debug              debug search strategy on stderr
--tags               use any tag, even unannotated
--first-parent       only follow first parent
--abbrev <n>         use <n> digits to display object names
--match <pattern>    only consider tags matching <pattern>. (default 'v*')
--exclude <pattern>  do not consider tags matching <pattern>
