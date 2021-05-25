from typing import Callable

from .version_info import VersionInfo, GitVersionInfo


def _semver_git(vi: GitVersionInfo) -> str:
    new_vi = VersionInfo.copy_constructor(vi)
    if not vi.commit_hash:
        pass
    elif semver(new_vi) == '0.0.0':
        new_vi.build.extend([vi.commit_hash])
    elif vi.commit_num:
        if not new_vi.prerelease:
            new_vi.patch += 1
        new_vi.prerelease.extend(['dev', vi.commit_num])
        new_vi.build.extend([vi.commit_hash])
    return semver(new_vi)


def semver(vi: VersionInfo) -> str:
    if isinstance(vi, GitVersionInfo):
        return _semver_git(vi)
    ver_str = f'{vi.major}.{vi.minor}.{vi.patch}'
    if vi.prerelease:
        ver_str += '-' + '.'.join(map(str, vi.prerelease))
    if vi.build:
        ver_str += '+' + '.'.join(map(str, vi.build))
    return ver_str


def cmake(vi: VersionInfo) -> str:
    ver_str = f'{vi.major}.{vi.minor}.{vi.patch}'
    if isinstance(vi, GitVersionInfo) and vi.commit_num:
        ver_str += f'.{vi.commit_num}'
    return ver_str


printers: dict[str, Callable[[VersionInfo], str]] = {
    'semver': semver,
    'cmake': cmake,
}
