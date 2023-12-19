import hashlib
import time
import random


def generate_address(key):
    private_key = key.to_bytes(32, byteorder="big")
    extended_key = b"\x80" + private_key
    first_hash = hashlib.sha256(extended_key).digest()
    second_hash = hashlib.sha256(first_hash).digest()
    checksum = second_hash[:4]
    final_key = extended_key + checksum
    return base58(final_key)


def base58(s):
    BASE58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    n = int.from_bytes(s, byteorder="big")
    res = ""
    while n > 0:
        n, remainder = divmod(n, 58)
        res = BASE58_ALPHABET[remainder] + res
    return res

def check_wallet(start_key, end_key, target_wallet):
    checked_keys = 0
    while checked_keys <= (end_key - start_key):
        current_key = random.randint(start_key, end_key)
        address = generate_address(current_key)
        if address == target_wallet:
            return f"Wallet gefunden! Schlüssel: {current_key}, Adresse: {address}"
        checked_keys += 1
        print(address)
    return "Wallet nicht gefunden im definierten Bereich."

start_key = 0x2000000000000000
end_key = 0x3FFFFFFFFFFFFFFF
target_wallet = "13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so"

result = check_wallet(start_key, end_key, target_wallet)
print(result)
