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

    def represent_ordered_mapping_flowing(self, data):
        return self.represent_mapping(u'tag:yaml.org,2002:map',
                                      data, flow_style=True)

    def represent_list_flowing(self, data):
        return self.represent_sequence(u'tag:yaml.org,2002:seq',
                                       data, flow_style=True)

    def represent_tuple(self, data):
        # TODO: represent tuple with parenthesis
        return self.represent_list_flowing(data)


class OrderedDictFlowing(OrderedDict):
    pass


class ListFlowing(list):
    pass


##############################################################################
# Custom GRC-specific roundtrip representers
##############################################################################

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

# TODO: why does this exist?
GRCRepresenter.add_representer(
    attributed_str,
    RTRepr.represent_str
)
