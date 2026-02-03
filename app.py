import os
import requests
import logging
import pandas as pd

from scorer import make_pred

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

TEST_URL = "https://www.dropbox.com/scl/fi/mbuxvjd19jauuj1nrfukh/test.csv?rlkey=iw9v2oqj7mupk7nqpjr92wfic&st=xyuql6rx&dl=1"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_PATH = "/app/input/test.csv"
OUTPUT_PATH = "/app/output/sample_submission.csv"
MODEL_PATH = os.path.join(BASE_DIR, "models", "catboost_model.cbm")

def download_file(url: str, path: str):
    logger.info("Downloading %s", path)

    os.makedirs(os.path.dirname(path), exist_ok=True)
    r = requests.get(url)
    r.raise_for_status()
    with open(path, "wb") as f:
        f.write(r.content)

    logger.info("Saved to %s", path)

def generate_submission(test_csv: str, output_csv: str):
    logger.info("Generating submission using model")

    submission = make_pred(
        path_to_file=test_csv,
        model_path=MODEL_PATH
    )
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    submission.to_csv(output_csv, index=False)

    logger.info("Submission saved to %s", output_csv)

def main():
    logger.info("Starting service")

    download_file(TEST_URL, TEST_PATH)
    generate_submission(TEST_PATH, OUTPUT_PATH)

    logger.info("Service finished successfully")

if __name__ == "__main__":
    main()
