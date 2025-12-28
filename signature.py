signature.py# backend/signature.py
import os
import hashlib
from jose import jwt, JWTError
from datetime import datetime

SECRET_KEY = "minha_chave_super_secreta_AnderAI"
ALGORITHM = "HS256"
CODE_DIR = os.path.dirname(__file__)  # pasta atual: backend
SIGNATURE_FILE = os.path.join(CODE_DIR, "signature.jwt")

def calculate_code_hash():
    """Gera hash SHA256 de todos os arquivos .py no backend"""
    sha = hashlib.sha256()
    for root, dirs, files in os.walk(CODE_DIR):
        for file in sorted(files):
            if file.endswith(".py") and file != "signature.py":
                path = os.path.join(root, file)
                with open(path, "rb") as f:
                    sha.update(f.read())
    return sha.hexdigest()

def generate_global_signature():
    """Gera JWT com hash do código e salva em signature.jwt"""
    code_hash = calculate_code_hash()
    payload = {
        "author": "AnderAI Solutions",
        "code_hash": code_hash,
        "date": datetime.utcnow().isoformat()
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    with open(SIGNATURE_FILE, "w") as f:
        f.write(token)
    return token

def verify_global_signature():
    """Verifica se código atual bate com o hash do JWT"""
    if not os.path.exists(SIGNATURE_FILE):
        return False
    with open(SIGNATURE_FILE, "r") as f:
        token = f.read()
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["code_hash"] == calculate_code_hash()
    except JWTError:
        return False
