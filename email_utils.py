import smtplib, os
from email.message import EmailMessage

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
FROM_EMAIL = os.getenv("FROM_EMAIL", SMTP_USER)

def send_games_email(to_email: str, games: list):
    msg = EmailMessage()
    msg["Subject"] = "Seus Jogos Premium — Mente Leve, Vida Plena"
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email
    body = "Olá!\n\nSegue seus jogos premium:\n\n"
    for idx, g in enumerate(games, 1):
        body += f"Jogo {idx}: {' '.join([str(n).zfill(2) for n in g])}\n"
    body += "\nBoa sorte!\nMente Leve, Vida Plena"
    msg.set_content(body)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(SMTP_USER, SMTP_PASS)
        smtp.send_message(msg)
