import os
import sys
import argparse
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Добавляем корень проекта в PYTHONPATH
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from etl.config import CONFIG
from etl.logger import logger_func

# Настройка логирования
LOGS_PATH = os.path.join(BASE_DIR, "logs")
log_file = os.path.join(LOGS_PATH, "preprocess.log")
logger = logger_func("preprocess_stage", log_file=log_file, to_stdout=False)

def preprocess_and_save(input_path: str, output_path: str):
    """
    Выполняет предобработку CSV-файла и сохраняет результат.
    Предобработка включает: удаление ненужных колонок, кодирование,
    масштабирование признаков.
    """
    try:
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Входной файл не найден: {input_path}")

        # Загрузка данных
        df = pd.read_csv(input_path)
        logger.info(f"Файл прочитан: {input_path} — {df.shape[0]} строк")

        # Проверка наличия целевой переменной
        target_col = CONFIG["target_column"]
        if target_col not in df.columns:
            raise KeyError(f"Целевая переменная '{target_col}' отсутствует в таблице")

        # Удаление ненужных колонок
        df = df.drop(columns=["id", "Unnamed: 32", "target"], errors="ignore")

        # Перекодировка целевой переменной
        df[target_col] = df[target_col].map({"M": 1, "B": 0})
        if df[target_col].isnull().any():
            raise ValueError("Ошибка при кодировании целевой переменной")

        # Разделение на признаки и метку
        X = df.drop(columns=[target_col])
        y = df[target_col]

        # Масштабирование
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        if X_scaled.shape != X.shape:
            logger.warning("Размерности до и после масштабирования не совпадают")

        # Объединение в итоговый DataFrame
        df_transformed = pd.DataFrame(X_scaled, columns=X.columns)
        df_transformed[target_col] = y.values

        # Сохранение результата
        df_transformed.to_csv(output_path, index=False)
        logger.info(f"Предобработка завершена. Файл сохранён: {output_path}")

    except Exception as e:
        logger.exception(f"Произошла ошибка на этапе предобработки: {e}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Предобработка CSV-файла для обучения модели")
    parser.add_argument("--input-path", type=str, default=CONFIG["raw_data_path"])
    parser.add_argument("--output-path", type=str, default=CONFIG["preprocessed_data_path"])
    args = parser.parse_args()

    preprocess_and_save(args.input_path, args.output_path)
