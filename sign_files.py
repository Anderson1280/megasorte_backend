# backend/sign_files.py
import os, hmac, hashlib
SECRET = b"mudar_para_variavel_de_ambiente_em_producao"

def sign_file(path):
    with open(path, "rb") as f:
        data = f.read()
    tag = hmac.new(SECRET, data, hashlib.sha256).hexdigest()
    ext = os.path.splitext(path)[1].lower()
    header = f"/* AnderAI-Signature: {tag} */\n"
    if ext in [".py", ".js", ".jsx", ".html", ".css"]:
        with open(path, "r", encoding="utf-8") as f:
            original = f.read()
        with open(path, "w", encoding="utf-8") as f:
            f.write(header + original)
    return tag

def sign_all(root):
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            if fn.endswith((".py", ".js", ".jsx", ".html", ".css")):
                p = os.path.join(dirpath, fn)
                print("Signing:", p, sign_file(p))

if __name__ == "__main__":
    sign_all(os.path.dirname(__file__))
