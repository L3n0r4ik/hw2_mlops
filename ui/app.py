from __future__ import annotations

import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, text

st.set_page_config(page_title="Fraud scoring UI", layout="wide")

dsn = os.getenv("PG_DSN", "postgresql+psycopg2://fraud:fraud@localhost:5432/fraud")
engine = create_engine(dsn, pool_pre_ping=True)

st.title("Fraud scoring results")

if st.button("Посмотреть результаты"):
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Последние 10 fraud_flag == 1")
        q1 = text("""
            SELECT transaction_id, score, fraud_flag
            FROM scores
            WHERE fraud_flag = 1
            LIMIT 10
        """)
        df_fraud = pd.read_sql(q1, engine)
        if df_fraud.empty:
            st.info("Фродовых транзакций (fraud_flag=1) пока нет.")
        else:
            st.dataframe(df_fraud, use_container_width=True, hide_index=True)

    with col2:
        st.subheader("Гистограмма скоров последних 100 транзакций")
        q2 = text("""
            SELECT score
            FROM scores
            LIMIT 100
        """)
        df_scores = pd.read_sql(q2, engine)
        if df_scores.empty:
            st.info("В таблице пока нет записей.")
        else:
            fig, ax = plt.subplots(figsize=(7, 4))
            ax.hist(df_scores["score"].values, bins=20)
            ax.set_xlabel("score")
            ax.set_ylabel("count")
            ax.set_title("Score distribution (last 100)")
            st.pyplot(fig, clear_figure=True)

st.caption(f"PG_DSN: {dsn}")
