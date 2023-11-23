# Copyright 2016 Free Software Foundation, Inc.
# This file is part of GNU Radio
#
# SPDX-License-Identifier: GPL-2.0-or-later
#

from ruamel.yaml import YAML
from .yaml_grc import (typ, init_typ,
                       ListFlowing, OrderedDictFlowing, MultiLineString)
from io import StringIO

__all__ = ['dump', 'safe_load',
           'ListFlowing', 'OrderedDictFlowing', 'MultiLineString']


class GRCYAML(YAML):
    def __init__(self):
        YAML.__init__(self)
        self.typ = [typ]
        init_typ(self)


def dump(data, stream=None, default_flow_style=False, indent=4, Dumper=None):
    # TODO: custom Dumper for the modtool
    yaml = GRCYAML()
    yaml.default_flow_style = default_flow_style
    yaml.indent = indent

    # TODO: disallow writing to string buffer
    if stream is None:
        sstream = StringIO()
        yaml.dump_all([data], sstream)
        return sstream.getvalue()

    # TODO: use context manager?
    return yaml.dump(data, stream)


def safe_load(stream):
    with GRCYAML() as yaml:
        return yaml.load(stream)
