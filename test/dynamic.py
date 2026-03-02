# Testing the "set_dynamic" method
from org.webpki.cbor import CBOR
from assertions import assert_true, assert_false, fail, success, check_exception

# Simple solution
def option_func(map_instance):
    if option:
        map_instance.set(CBOR.Int(1), CBOR.String(option))
    return map_instance

option = "on"
assert_true("dyn1", CBOR.Map()
    .set_dynamic(option_func)
    .set(CBOR.Int(2), CBOR.Boolean(True))
        .get(CBOR.Int(1)).get_string() == "on")

option = None
assert_true("dyn1", CBOR.Map()
    .set_dynamic(option_func)
    .set(CBOR.Int(2), CBOR.Boolean(True)).length == 1)

# Sophisticated parametric solution
class Options(object):
    def __init__(self, option):
        self.option = option

    def set_options(self, map_instance):
        if self.option:
            map_instance.set(CBOR.Int(1), CBOR.String(self.option))
        return map_instance
    
assert_true("dyn1", CBOR.Map()
    .set_dynamic(Options("on").set_options)
    .set(CBOR.Int(2), CBOR.Boolean(True))
        .get(CBOR.Int(1)).get_string() == "on")

assert_true("dyn1", CBOR.Map()
    .set_dynamic(Options(None).set_options)
    .set(CBOR.Int(2), CBOR.Boolean(True)).length == 1)

success()
