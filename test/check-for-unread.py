# Testing unread elements operations
from org.webpki.cbor import CBOR
from assertions import assert_true, assert_false, fail, success, check_exception

def oneTurn(statement, access, message=None):
    # print(":" + statement)
    should_fail = message is not None
    error = ""
    res = eval(statement)
    try:
        res.check_for_unread()
        assert_true(statement, access is None and not should_fail)
    except Exception as e:
        error = repr(e)
        # print(statement + " " + error)
        assert_true(statement, access or should_fail)
        check_exception(e, "never read")
    if access:
        try:
            eval("res." + access)
            res.check_for_unread()
            assert_false(statement, should_fail)
        except Exception as e:
            error = repr(e)
            # print(statement + " " + error)
            assert_true(statement, should_fail)
            check_exception(e, "never read")
    if should_fail and (error.find(message) < 0):
        fail("not" + repr(message) + error)

MAP_KEY_1 = CBOR.Int(1)
MAP_KEY_2 = CBOR.Int(2)

oneTurn("CBOR.Array()", None)
oneTurn("CBOR.Map()", None)
oneTurn("CBOR.Tag(45, CBOR.Map())", "get()")

oneTurn("CBOR.Tag(45, CBOR.Map().set(MAP_KEY_1, CBOR.Int(6)))", "get().get(MAP_KEY_1)",
    "Map key 1 with argument Int with value=6 was never read")

oneTurn("CBOR.Tag(45, CBOR.Map().set(MAP_KEY_1, CBOR.Int(6)))", "get().get(MAP_KEY_1).get_int64()")
oneTurn("CBOR.Array().add(CBOR.Tag(45, CBOR.Map()))", "get(0)",
    "Tagged object 45 of type Map was never read")

oneTurn("CBOR.Array().add(CBOR.Tag(45, CBOR.Map()))", "get(0).get()")

oneTurn("CBOR.Array().add(CBOR.Tag(45, CBOR.Int(6)))", "get(0).get()",
    "Tagged object 45 of type Int with value=6 was never read")

oneTurn("CBOR.Array().add(CBOR.Tag(45, CBOR.Int(6)))", "get(0).get().get_int64()")

oneTurn("CBOR.Array().add(CBOR.String('Hi!'))", "get(0)",
    "Array element of type String with value=\"Hi!\" was never read")

oneTurn("CBOR.Array().add(CBOR.Int(6))", "get(0).get_int64()")

oneTurn("CBOR.Map().set(MAP_KEY_1, CBOR.Array())", None,
    "Map key 1 with argument Array was never read")

oneTurn("CBOR.Map().set(MAP_KEY_1, CBOR.Array())", "get(MAP_KEY_1)")

oneTurn("CBOR.Tag(45, CBOR.Map().set(MAP_KEY_1, CBOR.Int(6)))", "get().get(MAP_KEY_1).get_int64()")

oneTurn("CBOR.Array().add(CBOR.Array())", "get(0)")

oneTurn("CBOR.Array().add(CBOR.Array())", None,
    "Array element of type Array was never read")

oneTurn("CBOR.Array().add(CBOR.Array())", "scan()")

oneTurn("CBOR.Int(6)", "get_int64()")

oneTurn("CBOR.Simple(8)", "get_simple()")

# Date time specials
oneTurn("CBOR.Tag(0, CBOR.String(\"2025-02-20T14:09:08Z\"))",
        "get()",
        "Tagged object 0 of type String with value=\"2025-02-20T14:09:08Z\" was never read")

oneTurn("CBOR.Tag(0, CBOR.String(\"2025-02-20T14:09:08Z\"))",
        "get_date_time()")

# COTX
oneTurn("CBOR.Tag(1010, CBOR.Array().add(CBOR.String(\"uri\")).add(CBOR.Map()))", "get()",
    "Array element of type String with value=\"uri\" was never read")

res = CBOR.Tag(1010, CBOR.Array().add(CBOR.String("uri")).add(CBOR.Boolean(True)))
assert_true("String problems", res.cotx_id == "uri")
assert_true("Object problems", res.cotx_object.get_boolean() == True)
res.check_for_unread()

res = CBOR.Tag(1010, CBOR.Array().add(CBOR.String("uri")).add(CBOR.Map()))
assert_true("String problems", res.cotx_id == "uri")
assert_true("Map problems", res.cotx_object.to_diagnostic(False) == "{}")
res.check_for_unread()

oneTurn("CBOR.Array().add(CBOR.Array())", "scan()")

# a slightly more elaborate example
res = CBOR.Map().set(MAP_KEY_2, CBOR.Array()).set(MAP_KEY_1, CBOR.String("Hi!"))
res.get(MAP_KEY_2).add(CBOR.Int(700))
assert_true("integer problems", res.get(MAP_KEY_2).get(0).get_int64() == 700)
assert_true("String problems", res.get(MAP_KEY_1).get_string() == "Hi!")
res.check_for_unread() # all is good

MAP_KEY_3 = CBOR.Array().add(CBOR.Int(5)).add(CBOR.Map())
oneTurn("CBOR.Map().set(MAP_KEY_3, CBOR.String('Hi!'))", None,
    "Map key [5,{}] with argument String with value=\"Hi!\" was never read")

oneTurn("CBOR.Map().set(MAP_KEY_3, CBOR.String('Hi!'))", "get(MAP_KEY_3).get_string()")

success()