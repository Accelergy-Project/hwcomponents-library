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
        # Exact tag match - return the tag version (strip 'v' prefix if present)
        tag = version.format_with("{tag}")
        return tag.lstrip('v')

    # Get the base version from the tag (or fallback)
    if version.tag:
        # Strip 'v' prefix if present
        base_version = str(version.tag).lstrip('v')
    else:
        # No tag - use fallback or guess
        base_version = guess_next_version(version) or "1.0.0"

    # Get the distance from the last tag
    distance = version.distance or 0

    if distance == 0:
        # No commits after tag - return base version
        return base_version

    # Return as post-release version
    return f"{base_version}.post{distance}"


def post_release_local_scheme(version):
    """
    Local scheme that returns empty string (no local version identifier).
    PyPI doesn't allow local versions, so we skip them.
    """
    return ""
