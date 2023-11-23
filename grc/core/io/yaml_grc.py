import ruamel.yaml as ryml
from ruamel.yaml.representer import RoundTripRepresenter as RTRepr

from collections import OrderedDict
from ..params.param import attributed_str

typ = 'grc'


def init_typ(self):
    self.Representer = GRCRepresenter
    # defaults for typ='rt'
    self.default_flow_style = False
    self.Emitter = ryml.emitter.Emitter
    self.Serializer = ryml.serializer.Serializer
    self.Scanner = ryml.scanner.RoundTripScanner
    self.Parser = ryml.parser.RoundTripParser
    self.Composer = ryml.composer.Composer
    self.Constructor = ryml.constructor.RoundTripConstructor


class GRCRepresenter(RTRepr):
    def __init__(self,
                 default_style=None,
                 default_flow_style=False,
                 dumper=None):
        RTRepr.__init__(self, default_style, default_flow_style, dumper)

    # TODO: remove
    def represent_ordered_mapping(self, data):
        value = []
        node = ryml.MappingNode(u'tag:yaml.org,2002:map',
                                value, flow_style=False)

        if self.alias_key is not None:
            self.represented_objects[self.alias_key] = node

        for item_key, item_value in data.items():
            node_key = self.represent_data(item_key)
            node_value = self.represent_data(item_value)
            value.append((node_key, node_value))

        return node

    def represent_ordered_mapping_flowing(self, data):
        return self.represent_mapping(u'tag:yaml.org,2002:map',
                                      data, flow_style=True)

    def represent_list_flowing(self, data):
        return self.represent_sequence(u'tag:yaml.org,2002:seq',
                                       data, flow_style=True)

    def represent_tuple(self, data):
        # TODO: represent tuple with parenthesis
        return self.represent_list_flowing(data)

    # TODO: remove
    def represent_ml_string(self, data):
        node = self.represent_str(data)
        node.style = '|'
        return node


class OrderedDictFlowing(OrderedDict):
    pass


class ListFlowing(list):
    pass


class MultiLineString(str):
    pass


##############################################################################
# Custom GRC-specific roundtrip representers
##############################################################################

# TODO: check usage - may be using CommentedMap or CommentedOrderedMap instead
GRCRepresenter.add_representer(
    OrderedDict,
    RTRepr.represent_dict
)

GRCRepresenter.add_representer(
    OrderedDictFlowing,
    GRCRepresenter.represent_ordered_mapping_flowing
)

GRCRepresenter.add_representer(
    ListFlowing,
    GRCRepresenter.represent_list_flowing
)

GRCRepresenter.add_representer(
    tuple,
    GRCRepresenter.represent_tuple
)

# TODO: check usage - may be using LiteralScalarString instead
GRCRepresenter.add_representer(
    MultiLineString,
    GRCRepresenter.represent_ml_string
)

# TODO: why does this exist?
GRCRepresenter.add_representer(
    attributed_str,
    RTRepr.represent_str
)

##############################################################################
# Default roundtrip representers
##############################################################################

GRCRepresenter.add_representer(
    type(None),
    RTRepr.represent_none
)

GRCRepresenter.add_representer(
    ryml.scalarstring.LiteralScalarString,
    RTRepr.represent_literal_scalarstring
)

GRCRepresenter.add_representer(
    ryml.scalarstring.FoldedScalarString,
    RTRepr.represent_folded_scalarstring
)

GRCRepresenter.add_representer(
    ryml.scalarstring.SingleQuotedScalarString,
    RTRepr.represent_single_quoted_scalarstring
)

GRCRepresenter.add_representer(
    ryml.scalarstring.DoubleQuotedScalarString,
    RTRepr.represent_double_quoted_scalarstring
)

GRCRepresenter.add_representer(
    ryml.scalarstring.PlainScalarString,
    RTRepr.represent_plain_scalarstring
)

GRCRepresenter.add_representer(
    ryml.scalarint.ScalarInt,
    RTRepr.represent_scalar_int
)

GRCRepresenter.add_representer(
    ryml.scalarint.BinaryInt,
    RTRepr.represent_binary_int
)

GRCRepresenter.add_representer(
    ryml.scalarint.OctalInt,
    RTRepr.represent_octal_int
)

GRCRepresenter.add_representer(
    ryml.scalarint.HexInt,
    RTRepr.represent_hex_int
)

GRCRepresenter.add_representer(
    ryml.scalarint.HexCapsInt,
    RTRepr.represent_hex_caps_int
)

GRCRepresenter.add_representer(
    ryml.scalarfloat.ScalarFloat,
    RTRepr.represent_scalar_float
)

GRCRepresenter.add_representer(
    ryml.scalarbool.ScalarBoolean,
    RTRepr.represent_scalar_bool
)

GRCRepresenter.add_representer(
    ryml.comments.CommentedSeq,
    RTRepr.represent_list
)

GRCRepresenter.add_representer(
    ryml.comments.CommentedMap,
    RTRepr.represent_dict
)

GRCRepresenter.add_representer(
    ryml.comments.CommentedOrderedMap,
    RTRepr.represent_ordereddict
)

GRCRepresenter.add_representer(
    ryml.comments.CommentedSet,
    RTRepr.represent_set
)

GRCRepresenter.add_representer(
    ryml.comments.TaggedScalar,
    RTRepr.represent_tagged_scalar
)

GRCRepresenter.add_representer(
    ryml.timestamp.TimeStamp,
    RTRepr.represent_datetime
)
