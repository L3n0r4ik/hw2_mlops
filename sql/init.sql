CREATE TABLE IF NOT EXISTS scores (
  transaction_id TEXT PRIMARY KEY,
  score DOUBLE PRECISION NOT NULL,
  fraud_flag SMALLINT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_scores_created_at ON scores(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_scores_fraud_flag ON scores(fraud_flag);
