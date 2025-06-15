import os
import sys
import logging
import argparse
import pandas as pd

# Добавление корня проекта в sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from etl.config import CONFIG
from etl.logger import logger_func

# Настройка логирования
LOGS_PATH = os.path.join(BASE_DIR, 'logs')
os.makedirs(LOGS_PATH, exist_ok=True)
log_file = os.path.join(LOGS_PATH, "load_data.log")

logger = logger_func(
    name="data_loader",
    log_file=log_file,
    to_stdout=False,
    to_file=True,
    level=logging.INFO
)

def fetch_and_store_dataset(destination_path: str):
    """
    Загружает встроенный датасет breast_cancer из sklearn,
    выполняет базовую проверку и сохраняет его в CSV.
    """
    from sklearn.datasets import load_breast_cancer

    try:
        dataset = load_breast_cancer(as_frame=True)
        df = dataset.frame

        # Проверка на корректные признаки
        expected = set(dataset.feature_names.tolist() + ["target"])
        actual = set(df.columns)
        missing = expected - actual
        if missing:
            raise ValueError(f"В данных отсутствуют ожидаемые признаки: {missing}")

        # Проверка на пропущенные значения
        if df.isnull().values.any():
            raise ValueError("В загруженном датасете обнаружены пропущенные значения.")

        # Преобразуем целевую переменную
        df[CONFIG["target_column"]] = df["target"].map({0: "B", 1: "M"})
        if df[CONFIG["target_column"]].isnull().any():
            raise ValueError("Ошибка при преобразовании целевой переменной.")

        df.to_csv(destination_path, index=False)
        logger.info(f"Данные успешно сохранены по пути: {destination_path}")

    except Exception as error:
        logger.warning(f"Ошибка при загрузке основного датасета: {error}")
        fallback_path = os.path.join(os.path.dirname(destination_path), "backup_data.csv")

        if os.path.exists(fallback_path):
            logger.info(f"Используется резервная копия: {fallback_path}")
            fallback_df = pd.read_csv(fallback_path)

            if fallback_df.isnull().values.any():
                logger.error("Резервные данные содержат пропущенные значения. Завершаем.")
                sys.exit(1)

            fallback_df.to_csv(destination_path, index=False)
            logger.info(f"Резервные данные скопированы в {destination_path}")
        else:
            logger.error("Резервная копия не найдена. Завершаем работу.")
            sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Загрузка breast cancer датасета из sklearn и сохранение в CSV.")
    parser.add_argument(
        "--output-path",
        type=str,
        default=CONFIG["raw_data_path"],
        help="Куда сохранить загруженный датасет (по умолчанию — путь из конфигурации)"
    )
    args = parser.parse_args()

    fetch_and_store_dataset(args.output_path)
