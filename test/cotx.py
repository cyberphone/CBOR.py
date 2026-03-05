# Testing the COTX identifier
from org.webpki.cbor import CBOR
from assertions import assert_true, assert_false, fail, success, check_exception

def oneTurn(hex, dn, ok):
  try:
    object = CBOR.decode(bytes.fromhex(hex))
    assert_true("Should not execute", ok)
    if (object.to_string() != dn or not object.equals(CBOR.decode(object.encode()))):
      fail("non match:" + dn + " " + object.to_string())
  except Exception as e:
    if ok: print(repr(e))
    assert_false("Must succeed", ok)

oneTurn('d903f2623737', '1010("77")', False)
oneTurn('d903f281623737', '1010(["77"])', False)
oneTurn('d903f28206623737', '1010([6, "77"])', False)
oneTurn('d903f28262373707', '1010(["77", 7])', True)

t = CBOR.Tag(1010, CBOR.Array().add(CBOR.String("uri")).add(CBOR.Array().add(CBOR.Map())))
assert_true("objectId", t.cotx_id == "uri")
assert_true("Object", t.cotx_object.get(0).to_string() == "{}")
t.check_for_unread()

assert_true("cotx", t == CBOR.create_cotx_tag("uri", CBOR.Array().add(CBOR.Map())))

success()
