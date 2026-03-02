# Testing "tag"
from org.webpki.cbor import CBOR
from assertions import assert_true, assert_false, fail, success, check_exception

object = CBOR.Array().add(CBOR.String("https://example.com/myobject")).add(CBOR.Int(6))
cbor = CBOR.Tag(CBOR.Tag.TAG_COTX, object).encode()
tag = CBOR.decode(cbor)
assert_true("t3", tag.get_tag_number()== CBOR.Tag.TAG_COTX)
assert_true("t3.1", object.equals(tag.get()))
assert_true("t3.2", tag.cotx_id == "https://example.com/myobject")
assert_true("t3.3", tag.cotx_object.equals(CBOR.Int(6)))
cbor = CBOR.Tag(0xf0123456789abcde, object).encode()
assert_true("t14", CBOR.decode(cbor).get_tag_number()== 0xf0123456789abcde)
assert_true("t5", cbor.hex() == 
    "dbf0123456789abcde82781c68747470733a2f2f6578616d706c652e636f6d2f6d796f626a65637406")

for tag_number in [-1, 0x10000000000000000]:
  try:
    CBOR.Tag(tag_number, CBOR.String("any"))
    fail("Should not")
  except Exception as e:
    check_exception(e, "out of range")


for tag_number in [2, 3]:
  try:
    CBOR.Tag(tag_number, CBOR.String("any"))
    fail("Should not")
  except Exception as e:
    check_exception(e, "'bigint'")

for tag_number in [0, 1]:
  try:
    CBOR.Tag(tag_number, CBOR.Boolean(True))
    fail("Should not")
  except Exception as e:
     check_exception(e, "CBOR.Boolean")

success()
