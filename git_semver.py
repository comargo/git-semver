import argparse
import re
import subprocess
import sys

from semver import VersionInfo

BASEVERSION = re.compile(
    r"""^[vV]?
    (?P<major>0|[1-9]\d*)
    (?:\.(?P<minor>0|[1-9]\d*)
        (?:\.(?P<patch>0|[1-9]\d*))?
        )?
    (?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?
    (?:\+(?P<build>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?
    $
    """,
    re.VERBOSE,
)


def coerce(version):
    """
    Convert an incomplete version string into a semver-compatible
    VersionInfo object.

    * Tries to detect a "basic" version string (
    ``major.minor.patch-prerelease+buildmetadata``).

    * If not enough components can be found, missing components are set to
    zero to obtain a valid semver version.

    :param str version: the version string to convert
    :return: a :class:`VersionInfo` instance
            (or ``VersionInfo(0)`` if it's not a version)
    :rtype: :class:`VersionInfo`
    """
    match = BASEVERSION.search(version)
    if not match:
        return VersionInfo(0)

    ver = match.groupdict()
    for key in ('major', 'minor', 'patch'):
        ver[key] = ver[key] or 0

    ver = VersionInfo(**ver)
    return ver


def make_semver(describe: str):
    describe = describe.split('-')
    commit = describe.pop()
    number = int(describe.pop()) if len(describe) else 0
    tag = '-'.join(describe)
    if not tag:
        return VersionInfo(0, build=commit)

    version = coerce(tag)
    if number == 0:
        return version

    if version.prerelease:
        version = version.replace(
            prerelease=f"{version.prerelease}.dev.{number}")
    else:
        version = version.bump_patch().replace(prerelease=f"dev.{number}")

    if version.build:
        version = version.replace(build=version.build + '.' + commit)
    else:
        version = version.replace(build=commit)
    return version


def main():
    parser = argparse.ArgumentParser(
        prog="git semver",
        description="Retrieving semantic versioning from git tags")
    parser.add_argument(
        '--debug', help='debug search strategy on stderr',
        action='store_true')
    parser.add_argument(
        '--tags', help='use any tag, even unannotated',
        action='store_true')
    parser.add_argument(
        '--first-parent', help='only follow first parent',
        action='store_true')
    parser.add_argument(
        '--abbrev',
        help='use <n> digits to display object names',
        action='store', metavar='<n>', type=int)
    parser.add_argument(
        '--match',
        help='only consider tags matching <pattern>. (default \'v*\')',
        metavar='<pattern>', default='v*')
    parser.add_argument(
        '--exclude',
        help='do not consider tags matching <pattern>',
        metavar='<pattern>')
    parser.add_argument(
        'commitish',
        help='Commit-ish object names to describe. '
             'Defaults to HEAD if omitted.',
        nargs='*')
    args = parser.parse_args()

    git_cmd = ['git', 'describe', '--always', '--long']
    if args.debug:
        git_cmd.append('--debug')
    if args.tags:
        git_cmd.append('--tags')
    if args.first_parent:
        git_cmd.append('--first-parent')
    if args.abbrev:
        git_cmd.extend(('--abbrev', str(args.abbrev)))
    if args.match:
        git_cmd.extend(('--match', args.match))
    if args.exclude:
        git_cmd.extend(('--exclude', args.exclude))
    git_cmd.extend(args.commitish)

    if args.debug:
        print(' '.join(git_cmd), file=sys.stderr)
    with subprocess.Popen(git_cmd, stdout=subprocess.PIPE,
                          text=True) as git_proc:
        for line in git_proc.stdout:
            version = make_semver(line.strip())
            print(version)
        if git_proc.returncode != 0:
            return git_proc.returncode

    return 0


if __name__ == '__main__':
    main()
