# dynamic tests
from org.webpki.cbor import CBOR
from assertions import assert_true, assert_false, fail, success, check_exception

def option_func(map_instance, argument):
    if argument:
        map_instance.set(CBOR.Int(1), CBOR.String(argument))
    return map_instance


assert_true("dyn", CBOR.Map().set_dynamic(option_func, "on").get(CBOR.Int(1)).get_string() == "on")
assert_true("dyn", CBOR.Map().set_dynamic(option_func, None).length == 0)


success()
