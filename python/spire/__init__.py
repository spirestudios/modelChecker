# This init declares "spire" as namespace package. This is so many independent rez packages can all be
# included in the "spire" namespace.
#
# Note that we are using a old school way of doing this. The more modern way of doing this trips up
# the rez builds.

from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)
