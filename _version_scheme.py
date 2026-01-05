"""
Custom version scheme for setuptools-scm that creates post-release versions
instead of dev versions, making them installable by default.
"""
from setuptools_scm.version import guess_next_version


def post_release_version_scheme(version):
    """
    Custom version scheme that creates post-release versions.
    Instead of 1.1.0.dev17, creates 1.1.0.post17
    Post-release versions are installable by default (not pre-releases).
    """
    if version.exact:
        return version.format_with("{tag}")

    # Get the next version (e.g., 1.1.0)
    next_version = guess_next_version(version)

    # Get the distance from the last tag
    distance = version.distance or 0

    # Return as post-release version
    return f"{next_version}.post{distance}"


def post_release_local_scheme(version):
    """
    Local scheme that returns empty string (no local version identifier).
    PyPI doesn't allow local versions, so we skip them.
    """
    return ""
