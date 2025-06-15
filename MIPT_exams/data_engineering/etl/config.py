import os

# Получаем абсолютный путь к корню проекта (на уровень выше текущего файла)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Пути к директориям проекта
DATA_DIR = os.path.join(BASE_DIR, 'data')                    # Для исходных (сырых) данных
LOGS_PATH = os.path.join(BASE_DIR, 'logs')                   # Для лог-файлов
PREPROCESSED_DIR = os.path.join(BASE_DIR, 'preprocessed')    # Для предобработанных данных
RESULTS_DIR = os.path.join(BASE_DIR, 'results')              # Для модели и метрик

# Создаём директории, если они ещё не существуют
for path in [DATA_DIR, LOGS_PATH, PREPROCESSED_DIR, RESULTS_DIR]:
    os.makedirs(path, exist_ok=True)

# Словарь с основными конфигурационными путями и параметрами
CONFIG = {
    # Путь к исходному датасету (будет сформирован/сохранён скриптом download.py)
    "raw_data_path": os.path.join(DATA_DIR, "breast_cancer.csv"),
    
    # Путь к предобработанным данным (выход из preprocess.py)
    "preprocessed_data_path": os.path.join(PREPROCESSED_DIR, "preprocessed_data.csv"),
    
    # Путь для сохранения обученной модели
    "model_path": os.path.join(RESULTS_DIR, "model.pkl"),
    
    # Путь для сохранения метрик модели в формате JSON
    "metrics_path": os.path.join(RESULTS_DIR, "metrics.json"),
    
    # Название целевой переменной в датасете
    "target_column": "diagnosis"
}
