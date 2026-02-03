from __future__ import annotations

import json
import os
import time
from confluent_kafka import Consumer
from sqlalchemy import create_engine

from db import upsert_score


KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
SCORING_TOPIC = os.getenv("KAFKA_SCORING_TOPIC", "scoring")

def main() -> None:
    consumer_config = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'group.id': 'ml-scorer',
        'auto.offset.reset': 'earliest'
    }

    dsn = os.getenv("PG_DSN", "postgresql+psycopg2://fraud:fraud@postgres:5432/fraud")
    engine = create_engine(dsn, pool_pre_ping=True)
    engine.connect()

    consumer = Consumer(consumer_config)
    consumer.subscribe([SCORING_TOPIC])

    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            continue
        try:
            data = json.loads(msg.value().decode('utf-8'))[0]
            upsert_score(
                engine=engine,
                transaction_id=str(data["transaction_id"]),
                score=float(data["prediction"]),
                fraud_flag=int(data["fraud_flag"]),
            )
        except Exception as e:
            print("EXCEPTION")
            print(repr(e))
            time.sleep(0.1)


if __name__ == "__main__":
    main()
