"""Reference heads for the event-chain check in RUNTIME-SPEC.md section 9."""
import hashlib
import struct

law = hashlib.sha256(b"law").digest()
head = hashlib.sha256(b"orlog-trace-0" + law).digest()
print("head0", head.hex())
events = [
    (b"S", 1, b"hello\n"),
    (b"A", 2, struct.pack(">I", 0) + b"I" + struct.pack(">q", 42)),
    (b"R", 3, b"OVERFLOW"),
]
for i, (kind, clause, payload) in enumerate(events, 1):
    head = hashlib.sha256(head + kind + struct.pack(">II", clause, len(payload)) + payload).digest()
    print("head%d" % i, head.hex())
