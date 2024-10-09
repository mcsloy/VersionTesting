from packaging.version import Version
import re
import argparse


def increment_major(version: Version) -> Version:
    """Increments the major version component of the given version.

    Arguments:
        version: A `Version` object representing the current version.

    Returns:
        new_version: A new `Version` object where the major version is
            incremented by 1, and the minor/micro components are reset to 0.
    """
    # "2.4.8" -> "3.0.0"
    return Version(f"{version.major + 1}.{0}.0")


def increment_minor(version: Version) -> Version:
    """Increments the minor  version component of the given version.

    Arguments:
        version: A `Version` object representing the current version.

    Returns:
        new_version: A new `Version` object where the minor version is
            incremented by 1, and the micro component is reset to 0, while the
            major version remains unchanged.
    """
    # "2.4.8" -> "2.5.0"
    return Version(f"{version.major}.{version.minor + 1}.0")


def increment_micro(version: Version) -> Version:
    """Increments the micro (patch) version component of the given version.

    Arguments:
        version: A `Version` object representing the current version.

    Returns:
        new_version: A new `Version` object where the micro version is
            incremented by 1, while the major and minor versions remain
            unchanged.
    """
    # "2.4.8" -> "2.4.9"
    return Version(f"{version.major}.{version.minor}.{version.micro + 1}")


def increment(version: Version, component: str) -> Version:
    """Increments the specified version component of the given version.

    Arguments:
        version: A `Version` object representing the current version.
        component: A string specifying which version component to increment. It
            must be one of the following: 'major', 'minor', or 'micro'.

    Returns:
        new_version: A `Version` object where the specified component has
            been incremented by 1. The other components will either be reset
            (if a higher-level component is incremented) or remain unchanged.
    """
    return {
        "major": increment_major,
        "minor": increment_minor,
        "micro": increment_micro
    }[component](version)


def version_from_file(path: str) -> Version:
    """Extracts and returns the version from a Python file.

    The file is expected to contain a line that assigns a version string
    to the `__version__` variable, following the format 'X.Y.Z', where
    X, Y, and Z are numbers.

    Arguments:
        path: A string representing the path to the file, typically the
              `__init__.py` file of a Python package.

    Returns:
        version: A `Version` object that represents the version number
                 extracted from the file.
    """

    # Open the provided __init__.py file and read the value assigned to the
    # __version__ variable contained within it.
    with open(path, "r") as file:
        version_string = re.search(
            r'^__version__\s*=\s*[\'"]([0-9]+(\.[0-9]+){2})[\'"]\s*$',
            file.read(), re.MULTILINE).group(1)

    # Convert that into a `Version` instance and return it
    return Version(version_string)




if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fetch, increment, or set python package version number.")

    parser.add_argument("path", help="path to the package's \"__init__.py\" file.")

    parser.add_argument(
        "--increment", "-i",
        type=str.lower,
        choices=["major", "minor", "micro"],
        help=
        "Specify which version component to increment before returning it. "
        "Options: 'major', 'minor', 'micro'. If unset, the current version "
        "will be returned in an unmodified state."
    )

    # Run the parser
    args = parser.parse_args()

    current_version = version_from_file(args.path)

    if args.increment is None:
        print(current_version, end="")
    else:
        print(increment(current_version, args.increment), end="")
