import cbor2


def encode_receipt_cbor(receipt_dict: dict) -> bytes:
    return cbor2.dumps(receipt_dict)


def decode_receipt_cbor(encoded: bytes) -> dict:
    return cbor2.loads(encoded)
