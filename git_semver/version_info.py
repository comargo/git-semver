import re
from typing import List, Optional, Union, Iterable, Iterator


def _get_separated_list(value: Union[str, Iterable[str], None],
                        sep: Optional[str] = ".") -> Iterator[str]:
    if not value:
        return []
    if isinstance(value, str):
        return _get_separated_list(value.split(sep), sep)
    return map(str, value)


class VersionInfo:
    major: int = 0
    minor: int = 0
    patch: int = 0
    _prerelease: List[str] = []
    _build: List[str] = []

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
        (?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?
        (?:\+(?P<build>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?
        $""",
        re.VERBOSE,
    )

    @property
    def prerelease(self) -> Optional[str]:
        return ".".join(map(str, self._prerelease))

    @prerelease.setter
    def prerelease(self, value: Union[List[str], str, None]):
        self._prerelease = list(_get_separated_list(value))

    def prerelease_append(self, value: Union[List[str], str]):
        if isinstance(value, str):
            return self.prerelease_append([value])
        self._prerelease.extend(value)
        return self

    @property
    def build(self) -> Optional[str]:
        return ".".join(map(str, self._build))

    @build.setter
    def build(self, value: Union[List[str], str, None]):
        self._build = list(_get_separated_list(value))

    def build_append(self, value):
        if isinstance(value, str):
            return self.build_append([value])
        self._build.extend(value)
        return self

    def __init__(self, version: Optional[str] = None):
        match = self.version_regexp.search(version or "")
        if not match:
            raise ValueError
        ver = match.groupdict()
        for key in ('major', 'minor', 'patch'):
            ver[key] = ver[key] or 0
        self.major = int(ver['major'])
        self.minor = int(ver['minor'])
        self.patch = int(ver['patch'])
        self.prerelease = ver['prerelease']
        self.build = ver['build']

    def __str__(self):
        version = f"{self.major}.{self.minor}.{self.patch}"
        if self.prerelease:
            version += f"-{self.prerelease}"
        if self.build:
            version += f"+{self.build}"
        return version

    def __iter__(self):
        for key in ["major", "minor", "patch", "prerelease", "build"]:
            yield key, getattr(self, key)
