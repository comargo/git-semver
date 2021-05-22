import pytest

from git_semver import make_semver

make_semver_test_data = [
    ("a5e0daa",
     {'major': 0, 'minor': 0, 'patch': 0,
      'prerelease': '', 'build': 'a5e0daa'}),
    ("v0.0.1-5-gaf36311",
     {'major': 0, 'minor': 0, 'patch': 2,
      'prerelease': 'dev.5', 'build': 'gaf36311'}),
    ("0.0.1-5-gaf36311",
     {'major': 0, 'minor': 0, 'patch': 2,
      'prerelease': 'dev.5', 'build': 'gaf36311'}),
    ("0.0.2-pre.1-5-gaf36311",
     {'major': 0, 'minor': 0, 'patch': 2,
      'prerelease': 'pre.1.dev.5', 'build': 'gaf36311'}),
    ("0.0.2-pre.1+build.6-5-gaf36311",
     {'major': 0, 'minor': 0, 'patch': 2,
      'prerelease': 'pre.1.dev.5', 'build': 'build.6.gaf36311'}),
    ("v0.0.1-0-g68be31c",
     {'major': 0, 'minor': 0, 'patch': 1,
      'prerelease': '', 'build': ''}),
]


@pytest.mark.parametrize(("value", "expected_dict"), make_semver_test_data)
def test_make_semver(value, expected_dict):
    assert dict(make_semver(value)) == expected_dict


def test_make_semver_empty_string():
    with pytest.raises(ValueError):
        make_semver("")
