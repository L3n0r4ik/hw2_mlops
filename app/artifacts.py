import json
import os
import matplotlib.pyplot as plt
import logging
logger = logging.getLogger(__name__)


def save_feature_importances(model, feature_names, output_path, top_k=5):
    importances = model.get_feature_importance()
    fi = dict(zip(feature_names, importances))
    fi_sorted = dict(
        sorted(fi.items(), key=lambda x: x[1], reverse=True)[:top_k]
    )
    with open(output_path, "w") as f:
        json.dump(fi_sorted, f, indent=2)

    logger.info("Feature importances saved to %s", output_path)

def save_prediction_distribution(preds, output_path):
    plt.figure(figsize=(8, 5))
    plt.hist(preds, bins=50, density=True, alpha=0.7)
    plt.title("Prediction score distribution")
    plt.xlabel("Score")
    plt.ylabel("Density")
    plt.grid(True)
    plt.savefig(output_path)
    plt.close()

    logger.info("Prediction distribution saved to %s", output_path)
