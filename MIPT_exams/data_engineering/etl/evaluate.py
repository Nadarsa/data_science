import os
import sys
import argparse
import json
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Подключение проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from etl.config import CONFIG
from etl.logger import logger_func
from etl.train_model import train_and_save_model

# Логирование
LOGS_PATH = os.path.join(BASE_DIR, "logs")
log_file = os.path.join(LOGS_PATH, "evaluate.log")
logger = logger_func("evaluator", log_file=log_file, to_stdout=False)

def evaluate_model(data_path: str, model_path: str, metrics_path: str):
    """
    Обучает модель, рассчитывает метрики и сохраняет их в JSON-файл.
    """
    try:
        model, X_test, y_test = train_and_save_model(data_path, model_path)

        y_pred = model.predict(X_test)

        metrics = {
            "accuracy": round(accuracy_score(y_test, y_pred), 4),
            "precision": round(precision_score(y_test, y_pred), 4),
            "recall": round(recall_score(y_test, y_pred), 4),
            "f1_score": round(f1_score(y_test, y_pred), 4)
        }

        with open(metrics_path, "w") as f:
            json.dump(metrics, f, indent=4)

        logger.info(f"Метрики сохранены в {metrics_path}")
        for name, value in metrics.items():
            logger.info(f"{name}: {value}")

    except Exception as e:
        logger.exception(f"Ошибка при оценке модели: {e}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Оценка модели и сохранение метрик")
    parser.add_argument("--data-path", type=str, default=CONFIG["preprocessed_data_path"])
    parser.add_argument("--model-path", type=str, default=CONFIG["model_path"])
    parser.add_argument("--metrics-path", type=str, default=CONFIG["metrics_path"])
    args = parser.parse_args()

    evaluate_model(args.data_path, args.model_path, args.metrics_path)
