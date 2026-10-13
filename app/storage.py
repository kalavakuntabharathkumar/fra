import os
from contextlib import contextmanager
import psycopg
from psycopg.rows import dict_row

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://fraud:fraud_dev_only@localhost:5432/frauddb")

@contextmanager
def connection():
    conn = psycopg.connect(DATABASE_URL, connect_timeout=2, row_factory=dict_row)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def initialize():
    try:
        with connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS transaction_scores (
                    transaction_id TEXT PRIMARY KEY,
                    amount NUMERIC(12,2) NOT NULL,
                    fraud_probability DOUBLE PRECISION NOT NULL,
                    decision TEXT NOT NULL,
                    model_version TEXT NOT NULL,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                )
            ''')
    except Exception:
        # API can still start in lightweight tests when PostgreSQL isn't available.
        pass

def save_score(tx, probability, decision, model_version):
    try:
        with connection() as conn:
            conn.execute('''
                INSERT INTO transaction_scores
                (transaction_id, amount, fraud_probability, decision, model_version)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (transaction_id) DO UPDATE SET
                fraud_probability = EXCLUDED.fraud_probability,
                decision = EXCLUDED.decision,
                model_version = EXCLUDED.model_version
            ''', (tx.transaction_id, tx.amount, probability, decision, model_version))
    except Exception:
        # Deliberate demo resilience; production should surface and monitor persistence failures.
        pass
