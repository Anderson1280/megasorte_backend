# backend/utils/verify_meta_hmac.py
import hmac
import hashlib
import base64

META_SECRET = b"how_011207_with_segura1980"  # mesma chave do outro arquivo

def verify_signature(text: str, signature: str) -> bool:
    expected = hmac.new(
        META_SECRET,
        text.encode("utf-8"),
        hashlib.sha256
    ).digest()

    return base64.b64encode(expected).decode() == signature

if __name__ == "__main__":
    t = input("Texto original: ")
    s = input("Assinatura: ")

    if verify_signature(t, s):
        print("Assinatura válida.")
    else:
        print("Assinatura inválida.")
