# Testing exceptions
from org.webpki.cbor import CBOR
from assertions import assert_true, assert_false, fail, success, check_exception

try:
    CBOR.decode(bytes([0xff]))
    fail("should not pass")
except CBOR.Exception as e:
    check_exception(e, "Unsupported tag: 0xff")

success()
