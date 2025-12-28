from db import get_db

def reset_por_concurso(novo_concurso: int):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        UPDATE acessos
        SET credits = 10
        WHERE premium = 1
    """)

    cur.execute("""
        INSERT OR REPLACE INTO sistema (chave, valor)
        VALUES ('concurso_atual', ?)
    """, (str(novo_concurso),))

    conn.commit()
    conn.close()