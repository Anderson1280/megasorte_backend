# Arquivo: backend/config.py
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Usando 3 barras para SQLite (relativo ao BASE_DIR, mas o SQLAlchemy usa o caminho absoluto)
SQLALCHEMY_DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'megasorte.db')}"

# JWT
SECRET_KEY = os.environ.get("JWT_SECRET", "megasorte_super_secret_key")
JWT_SECRET = SECRET_KEY # Consistência com o auth.py
JWT_ALGORITHM = "HS256"
# Define uma validade longa para simulação de Premium, mas você pode diminuir.
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 60*24*30))

# SMTP (configure suas credenciais em variáveis de ambiente em produção)
SMTP_HOST = os.environ.get("SMTP_HOST", "")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_PASS = os.environ.get("SMTP_PASS", "")
EMAIL_FROM = os.environ.get("EMAIL_FROM", "no-reply@megasorte.com")

# Admin / Frontend
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "undersomm@hotmail.com")
FRONTEND_ORIGIN = os.environ.get("FRONTEND_ORIGIN", "http://localhost:5173")