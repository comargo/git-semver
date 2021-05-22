from datetime import datetime
import pytest

from git_semver.version_info import _get_separated_list, VersionInfo


class TestSeparatedList:
    def test_none(self):
        assert list(_get_separated_list(None)) == []

    def test_array(self):
        assert list(_get_separated_list(["qwe", "rty"])) == ["qwe", "rty"]
        assert list(_get_separated_list(["qwe", 1, 2])) == ["qwe", "1", "2"]
        assert list(_get_separated_list(["qwe.rty"])) == ["qwe.rty"]
        assert list(_get_separated_list(["qwe", None])) == ["qwe", "None"]

    def test_generator(self):
        def generator():
            for i in range(5):
                yield f"{i}"

        generated_sequence = ["0", "1", "2", "3", "4"]
        assert list(_get_separated_list(range(5))) == generated_sequence
        assert list(_get_separated_list(generator())) == generated_sequence

    def test_string(self):
        assert list(_get_separated_list("qwe.rty")) == ["qwe", "rty"]
        assert list(_get_separated_list("qwe")) == ["qwe"]
        assert list(_get_separated_list("qwe..rty")) == ["qwe", "", "rty"]

    def test_invalid_type(self):
        with pytest.raises(TypeError):
            # noinspection PyTypeChecker
            _get_separated_list(1)
        with pytest.raises(TypeError):
            # noinspection PyTypeChecker
            _get_separated_list(datetime.now())

    def test_semicolon_sep(self):
        assert list(_get_separated_list("qwe:rty", ":")) == ["qwe", "rty"]


class TestVersionInfo:
    constructor_test_data = [
        (None, "0.0.0",
         {'major': 0, 'minor': 0, 'patch': 0, 'prerelease': '', 'build': ''}),
        ("1", "1.0.0",
         {'major': 1, 'minor': 0, 'patch': 0, 'prerelease': '', 'build': ''}),
        ("1.2", "1.2.0",
         {'major': 1, 'minor': 2, 'patch': 0, 'prerelease': '', 'build': ''}),
        ("1.2.3", "1.2.3",
         {'major': 1, 'minor': 2, 'patch': 3, 'prerelease': '', 'build': ''}),
        ("1.2.3-pre.1", "1.2.3-pre.1",
         {'major': 1, 'minor': 2, 'patch': 3, 'prerelease': 'pre.1',
          'build': ''}),
        ("1.2.3-pre.1+dev.2", "1.2.3-pre.1+dev.2",
         {'major': 1, 'minor': 2, 'patch': 3, 'prerelease': 'pre.1',
          'build': 'dev.2'}),
        ("1.2-pre.1+dev.2", "1.2.0-pre.1+dev.2",
         {'major': 1, 'minor': 2, 'patch': 0, 'prerelease': 'pre.1',
          'build': 'dev.2'}),
        ("1-pre.1+dev.2", "1.0.0-pre.1+dev.2",
         {'major': 1, 'minor': 0, 'patch': 0, 'prerelease': 'pre.1',
          'build': 'dev.2'}),
        ("1+dev.2", "1.0.0+dev.2",
         {'major': 1, 'minor': 0, 'patch': 0, 'prerelease': '',
          'build': 'dev.2'}),
        ("-pre", "0.0.0-pre",
         {'major': 0, 'minor': 0, 'patch': 0, 'prerelease': 'pre',
          'build': ''}),
        ("+dev", "0.0.0+dev",
         {'major': 0, 'minor': 0, 'patch': 0, 'prerelease': '',
          'build': 'dev'})
    ]

    @pytest.mark.parametrize("test_input, expected_str, expected_dict",
                             constructor_test_data)
    def test_constructor(self, test_input, expected_str, expected_dict):
        vi = VersionInfo(test_input)
        assert dict(vi) == expected_dict
        assert str(vi) == expected_str

    @pytest.mark.parametrize("test_input, expected_str, expected_dict",
                             constructor_test_data)
    def test_constructor_v(self, test_input, expected_str, expected_dict):
        if test_input is None:  # skip None value
            return
        vi = VersionInfo(f"v{test_input}")
        assert dict(vi) == expected_dict
        assert str(vi) == expected_str

    def test_invalid_constructor(self):
        with pytest.raises(ValueError):
            VersionInfo("v1a")
        with pytest.raises(ValueError):
            VersionInfo("something")

    def test_prerelease_append(self):
        vi = VersionInfo("v1.2.3-pre.1+build.1")
        vi.prerelease_append("pre2")
        assert dict(vi) == {'major': 1, 'minor': 2, 'patch': 3,
                            'prerelease': 'pre.1.pre2', 'build': 'build.1'}
        vi.prerelease_append(["dev", 1])
        assert dict(vi) == {'major': 1, 'minor': 2, 'patch': 3,
                            'prerelease': 'pre.1.pre2.dev.1',
                            'build': 'build.1'}

    def test_build_append(self):
        vi = VersionInfo("v1.2.3-pre.1+build.1")
        vi.build_append("012345")
        assert dict(vi) == {'major': 1, 'minor': 2, 'patch': 3,
                            'prerelease': 'pre.1', 'build': 'build.1.012345'}
        vi.build_append(["date", 20210521])
        assert dict(vi) == {'major': 1, 'minor': 2, 'patch': 3,
                            'prerelease': 'pre.1',
                            'build': 'build.1.012345.date.20210521'}
