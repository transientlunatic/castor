__author__ = """Daniel Williams"""
__email__ = "mail@daniel-williams.co.uk"
__packagename__ = __name__

from pkg_resources import DistributionNotFound, get_distribution

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    __version__ = "dev"
    pass
