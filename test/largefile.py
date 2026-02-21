# largefile.py

from org.webpki.cbor import CBOR
from cryptography.hazmat.primitives import hashes
import http.client

FILE_LABEL = CBOR.String("file")
SHA256_LABEL = CBOR.String("sha256")
CBOR_MAX_LENGTH = 1000
CHUNK_SIZE = 1000

# Initiate the hash method
digest = hashes.Hash(hashes.SHA256())

# Perform an HTTP request
conn = http.client.HTTPSConnection("cyberphone.github.io")
conn.request("GET", "/CBOR.py/doc/app-notes/large-payloads/payload.bin")
response = conn.getresponse()

# Show the response status
print(response.status, response.reason)

# Decode CBOR using the received stream handle
decoder = CBOR.init_decoder(response, CBOR.SEQUENCE_MODE, CBOR_MAX_LENGTH)
metadata = decoder.decode_with_options()

# Print CBOR object
print(metadata)
print("CBOR bytes: " + str(decoder.get_byte_count()))

# The rest of the stream is supposed to contain the file.
# Read data in moderately-sized chunks until EOF.
total_bytes = 0
while True:
    chunk = response.read(CHUNK_SIZE)
    if chunk:
        # Hash the chunk.
        digest.update(chunk)
        # Update counter.
        total_bytes += len(chunk)
        ###################################################
        # Store the chunk in an application-specific way. #
        ###################################################
    else: break

# Now verify that the calculated hash is identical to the declared hash.
if digest.finalize() != metadata.get(SHA256_LABEL).get_bytes():
    print("Failed at SHA256")
else:
    print("Succesfully received: {:s} ({:n}))"
          .format(metadata.get(FILE_LABEL).get_string(), total_bytes))