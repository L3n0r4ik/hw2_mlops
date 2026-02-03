import pandas as pd
import logging
import os
from catboost import CatBoostClassifier
from preprocessing import preprocess
from artifacts import save_feature_importances, save_prediction_distribution

logger = logging.getLogger(__name__)


def load_model(model_path: str):
    model = CatBoostClassifier()
    model.load_model(model_path)

    logger.info("Model loaded from %s", model_path)
    return model

def make_pred(path_to_file: str, model_path: str) -> pd.DataFrame:
    logger.info("Reading input file: %s", path_to_file)

    raw_df = pd.read_csv(path_to_file, sep=",")
    processed_df = preprocess(raw_df)

    logger.info("Path to model: %s", model_path)
    model = load_model(model_path)
    preds = model.predict_proba(processed_df)[:, 1]
    submission = pd.DataFrame({
        "index": raw_df.index,
        "prediction": preds
    })

    save_feature_importances(
        model=model,
        feature_names=processed_df.columns.tolist(),
        output_path="/app/output/feature_importances.json"
    )

    save_prediction_distribution(
        preds,
        "/app/output/prediction_distribution.png"
    )

    logger.info("Prediction finished. Rows: %d", len(submission))
    return submission
