import pytest

from git_semver import version_from_git
from git_semver.printer import semver, cmake

make_semver_test_data = [
    'value, expected_semver, expected_cmake',
    [
        ('', '0.0.0', '0.0.0'),
        ('a5e0daa', '0.0.0+a5e0daa', '0.0.0'),
        ('v0.0.1-5-gaf36311', '0.0.2-dev.5+gaf36311', '0.0.1.5'),
        ('0.0.1-5-gaf36311', '0.0.2-dev.5+gaf36311', '0.0.1.5'),
        ('0.0.2-pre.1-5-gaf36311', '0.0.2-pre.1.dev.5+gaf36311', '0.0.2.5'),
        ('0.0.2-pre.1+build.6-5-gaf36311',
         '0.0.2-pre.1.dev.5+build.6.gaf36311', '0.0.2.5'),
        ('v0.0.1-0-g68be31c', '0.0.1', '0.0.1'),
    ]]


@pytest.mark.parametrize(*make_semver_test_data)
def test_make_version(value, expected_semver, expected_cmake):
    vi = version_from_git(value)
    assert semver(vi) == expected_semver
    assert cmake(vi) == expected_cmake
