import argparse
from git_semver import get_versions


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


if __name__ == '__main__':
    main()
