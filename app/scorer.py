import pandas as pd
import logging
import os
from catboost import CatBoostClassifier
from preprocessing import preprocess

logger = logging.getLogger(__name__)

logger.info('Importing pretrained model...')

model = CatBoostClassifier()
model.load_model('models/catboost_model.cbm')

def make_pred(dt, source_info="kafka"):
    print(dt.dtypes)
    processed_df = preprocess(dt)

    preds = model.predict_proba(processed_df)[:, 1]
    submission = pd.DataFrame({
        "index": dt.index,
        "prediction": preds,
        "fraud_flag": int(preds > 0.01)
    })

    logger.info("Prediction finished. Rows: %d", len(submission))
    return submission