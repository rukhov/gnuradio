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
    def __init__(self, output=None):
        YAML.__init__(self, output=output)
        self.typ = [typ]
        init_typ(self)


def dump(data, stream, default_flow_style=False, indent=4):
    with GRCYAML(output=stream) as yaml:
        yaml.default_flow_style = default_flow_style
        yaml.indent = indent
        return yaml.dump(data)


def safe_load(stream):
    with GRCYAML() as yaml:
        return yaml.load(stream)
