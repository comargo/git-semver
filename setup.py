from setuptools import setup

try:
    from git_semver import get_versions
    from git_semver.printer import semver
except ImportError:
    def get_versions():
        return iter([])

    def semver(*args, **kwargs):
        return None


def _get_package_version():
    versions = get_versions()
    try:
        version = next(versions)
        return semver(version)
    except StopIteration:
        return None


def _patch_version():
    version = _get_package_version()
    if not version:
        return
    import configparser
    config = configparser.ConfigParser()
    config_filename = 'setup.cfg'
    config.read(config_filename)
    config['metadata']['version'] = version
    with open(config_filename, 'w') as configfile:
        config.write(configfile)


_patch_version()
setup()
