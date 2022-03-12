import collections

ConvretTo = collections.namedtuple("ConvretTo", ["source", "target"])

ALLOW_CONVERT = [
    ConvretTo("PDF", "IMAGE")
]