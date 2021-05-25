import re
from typing import List, Optional, Union, Iterable, Iterator


def _get_separated_list(value: Union[str, Iterable[str], None],
                        sep: Optional[str] = '.') -> Iterator[str]:
    if not value:
        return []
    if isinstance(value, str):
        return _get_separated_list(value.split(sep), sep)
    return map(str, value)


class VersionInfo:
    major: int = 0
    minor: int = 0
    patch: int = 0
    prerelease: List[str] = []
    build: List[str] = []

    version_regexp = re.compile(
        r"""
        ^[vV]?
        (?:
            (?P<major>0|[1-9]\d*)
            (?:
                \.(?P<minor>0|[1-9]\d*)
                (?:
                    \.(?P<patch>0|[1-9]\d*)
                )?
            )?
        )?
        (?:-(?P<prerelease>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]*)*))?
        (?:\+(?P<build>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]*)*))?
        $""",
        re.VERBOSE,
    )

    def __init__(self, version: Optional[str] = None):
        match = self.version_regexp.search(version or '')
        if not match:
            raise ValueError
        ver = match.groupdict()
        for key in ('major', 'minor', 'patch'):
            ver[key] = ver[key] or 0
        self.major = int(ver['major'])
        self.minor = int(ver['minor'])
        self.patch = int(ver['patch'])
        self.prerelease = list(_get_separated_list(ver['prerelease']))
        self.build = list(_get_separated_list(ver['build']))

    @classmethod
    def copy_constructor(cls, vi):
        if not isinstance(vi, VersionInfo):
            raise TypeError
        new_vi = cls()
        new_vi.major = vi.major
        new_vi.minor = vi.minor
        new_vi.patch = vi.patch
        new_vi.prerelease = vi.prerelease.copy()
        new_vi.build = vi.build.copy()
        return new_vi

    def __str__(self):
        from .printer import semver
        return semver(self)


class GitVersionInfo(VersionInfo):
    commit_num: int = 0
    commit_hash: str = ''

    def __init__(self, tag: Optional[str] = None, commit_num: int = 0,
                 commit_hash: str = ''):
        super().__init__(tag)
        self.commit_num = commit_num
        self.commit_hash = commit_hash
