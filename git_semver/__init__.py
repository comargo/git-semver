import argparse
import subprocess
import sys
from typing import List, Optional, Generator
from git_semver.version_info import VersionInfo


def make_semver(describe: str) -> VersionInfo:
    describe = describe.split('-')
    commit = describe.pop()
    number = int(describe.pop()) if len(describe) else 0
    tag = '-'.join(describe)
    if not tag:
        return VersionInfo(f"+{commit}")

    version = VersionInfo(tag)
    if number == 0:
        return version
    if not version.prerelease:
        version.patch += 1
    version \
        .prerelease_append(["dev", number]) \
        .build_append(commit)
    return version


def get_versions(commitish: List[str] = None,
                 debug: bool = False,
                 empty_tags: bool = False,
                 first_parent: bool = False,
                 abbrev: Optional[int] = None,
                 match: Optional[List[str]] = None,
                 exclude: Optional[List[str]] = None
                 ) -> Generator[str, None, None]:
    git_cmd = ['git', 'describe', '--always', '--long']
    if debug:
        git_cmd.append('--debug')
    if empty_tags:
        git_cmd.append('--tags')
    if first_parent:
        git_cmd.append('--first-parent')
    if abbrev:
        git_cmd.extend(('--abbrev', str(abbrev)))
    for single_match in match or ["v*"]:
        git_cmd.extend(('--match', single_match))
    for single_exclude in exclude or []:
        git_cmd.extend(('--exclude', single_exclude))
    git_cmd.extend(commitish or [])

    if debug:
        print(' '.join(git_cmd), file=sys.stderr)
    git_proc = subprocess.check_output(git_cmd, text=True)
    for line in str(git_proc).split():
        yield make_semver(line.strip())


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
        metavar='<pattern>', default='v*', nargs='*')
    parser.add_argument(
        '--exclude',
        help='do not consider tags matching <pattern>',
        metavar='<pattern>', nargs='*')
    parser.add_argument(
        'commitish',
        help='Commit-ish object names to describe. '
             'Defaults to HEAD if omitted.',
        nargs='*')
    args = parser.parse_args()

    versions = get_versions(debug=args.debug,
                            empty_tags=args.tags,
                            first_parent=args.first_parent,
                            abbrev=args.abbrev,
                            match=args.match,
                            exclude=args.exclude,
                            commitish=args.commitish)
    for version in versions:
        print(version)


def __version__():  # noqa: ignore=N807
    try:
        return str(next(get_versions()))
    except subprocess.CalledProcessError:
        return "0.0.0+non.git.build"
