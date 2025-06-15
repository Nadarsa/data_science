import os
import sys
import argparse
import pandas as pd
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# Подключение корня проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from etl.config import CONFIG
from etl.logger import logger_func

# Логирование
LOGS_PATH = os.path.join(BASE_DIR, "logs")
log_file = os.path.join(LOGS_PATH, "train.log")
logger = logger_func("model_trainer", log_file=log_file, to_stdout=False)

def train_and_save_model(data_path: str, model_path: str):
    """
    Загружает предобработанные данные, обучает модель и сохраняет её в файл.
    """
    try:
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Предобработанные данные не найдены: {data_path}")

        # Загрузка данных
        df = pd.read_csv(data_path)
        logger.info(f"Загружено {df.shape[0]} строк из {data_path}")

        target_col = CONFIG["target_column"]
        if target_col not in df.columns:
            raise KeyError(f"В таблице отсутствует целевая переменная '{target_col}'")

        X = df.drop(columns=[target_col])
        y = df[target_col]

        # Разделение на обучающую и тестовую выборки
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Обучение модели
        model = LogisticRegression(max_iter=1000)
        model.fit(X_train, y_train)

        # Сохранение модели
        with open(model_path, "wb") as f:
            pickle.dump(model, f)

        logger.info(f"Модель успешно обучена и сохранена в {model_path}")

        return model, X_test, y_test

    except Exception as e:
        logger.exception(f"Ошибка при обучении модели: {e}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Обучение модели логистической регрессии")
    parser.add_argument("--data-path", type=str, default=CONFIG["preprocessed_data_path"])
    parser.add_argument("--model-path", type=str, default=CONFIG["model_path"])
    args = parser.parse_args()

    train_and_save_model(args.data_path, args.model_path)
