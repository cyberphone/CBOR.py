# Testing datetime and epoch methods
from org.webpki.cbor import CBOR
from assertions import assert_true, assert_false, fail, success, check_exception
import datetime

def one_get_date_time(epoch, isoString):
  assert_true("date1", CBOR.String(isoString).get_date_time().timestamp() == epoch)
  cbor = CBOR.decode(CBOR.String(isoString).encode())
  assert_true("date2", cbor.get_date_time().timestamp() == epoch)
 # assert_true("date3", CBOR.Tag(0n, CBOR.String(isoString)).get_date_time().timestamp() == epoch)
  timestamp = CBOR.String(isoString).get_date_time()
  assert_true("date4", (int(timestamp.timestamp() * 1000 + 0.5) / 1000.0) ==
    CBOR.create_date_time(timestamp, isoString.find(".") > 0, 
      isoString.find("Z") > 0).get_date_time().timestamp())

one_get_date_time(1740060548.000, "2025-02-20T14:09:08+00:00")
one_get_date_time(1740060548.000, "2025-02-20T14:09:08Z")
one_get_date_time(1740060548.000, "2025-02-20T15:09:08+01:00")
one_get_date_time(1740060548.000, "2025-02-20T15:39:08+01:30")
one_get_date_time(1740060548.000, "2025-02-20T12:09:08-02:00")
one_get_date_time(1740060548.000, "2025-02-20T11:39:08-02:30")
one_get_date_time(1740060548.123, "2025-02-20T11:39:08.123-02:30")
one_get_date_time(1740060548.930, "2025-02-20T14:09:08.930Z")
# Ugly!
one_get_date_time(1771201728.000, "2026-02-15T23:05:48-01:23")
one_get_date_time(1771201728.000, "2026-02-16T00:28:48Z")
# Date change!
one_get_date_time(1771200348.000, "2026-02-15T23:05:48-01:00")
one_get_date_time(1771200348.000, "2026-02-16T01:05:48+01:00")
one_get_date_time(1771200348.000, "2026-02-16T00:05:48Z")
# Next: Truncates!
one_get_date_time(1740060548.9305, "2025-02-20T14:09:08.9305Z")
# Limits
one_get_date_time(           0.000, "1970-01-01T00:00:00Z")
one_get_date_time(253402300799.000, "9999-12-31T23:59:59Z")

def one_create_date_time(epoch, millis, utc):
  instant = datetime.datetime.fromtimestamp(epoch, datetime.UTC)
  assert_true("now/date_time", 
    CBOR.create_date_time(instant, millis, utc).get_date_time().timestamp() == epoch)
  assert_true("now/epoch_time", 
    CBOR.create_epoch_time(instant, millis).get_epoch_time().timestamp() == epoch)

# Roundtripping...
now = datetime.datetime.now().timestamp()
millis = int(now * 1000 + 0.5) / 1000
seconds = int(now + 0.5)

one_create_date_time(millis, True, False)
one_create_date_time(millis, True, True)
one_create_date_time(seconds, False, False)
one_create_date_time(seconds, False, True)

success()