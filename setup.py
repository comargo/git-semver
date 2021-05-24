from setuptools import setup

try:
    from git_semver import get_versions
except ImportError:
    def get_versions():
        return iter([])


def _get_package_version():
    versions = get_versions()
    try:
        version = next(versions)
        version_str = f"{version.major}.{version.minor}.{version.patch}"
        if version.prerelease:
            version_str += f".{version.prerelease}"
        if version.build:
            version_str += f"+{version.build}"
        return version_str
    except StopIteration:
        return None


def _patch_version():
    version = _get_package_version()
    if not version:
        return
    import configparser
    config = configparser.ConfigParser()
    config_filename = "setup.cfg"
    config.read(config_filename)
    config['metadata']['version'] = version
    with open(config_filename, 'w') as configfile:
        config.write(configfile)


_patch_version()
setup()
