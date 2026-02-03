from __future__ import annotations

from sqlalchemy import create_engine, text


def upsert_score(engine, transaction_id: str, score: float, fraud_flag: int) -> None:
    q = text("""
        INSERT INTO scores(transaction_id, score, fraud_flag)
        VALUES (:transaction_id, :score, :fraud_flag)
        ON CONFLICT (transaction_id)
        DO UPDATE SET score = EXCLUDED.score,
                      fraud_flag = EXCLUDED.fraud_flag,
                      created_at = now()
    """)
    with engine.begin() as conn:
        conn.execute(q, {"transaction_id": transaction_id, "score": score, "fraud_flag": fraud_flag})
