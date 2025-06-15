import os
import sys
import logging
from typing import Optional

def logger_func(
    name: str,
    log_file: Optional[str] = None,
    to_stdout: bool = True,
    to_file: bool = True,
    level: int = logging.INFO,
    encoding: str = "utf-8"
) -> logging.Logger:
    """
    Создаёт настраиваемый логгер с возможностью логирования в файл и/или stdout.

    :param name: Имя логгера
    :param log_file: Путь к лог-файлу (если нужно сохранять)
    :param to_stdout: Выводить в терминал
    :param to_file: Сохранять в файл
    :param level: Уровень логирования
    :param encoding: Кодировка лог-файла
    :return: Инициализированный логгер
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Удаляем старые обработчики, чтобы избежать дублирования
    if logger.hasHandlers():
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

    formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")

    # Добавляем вывод в файл
    if to_file and log_file:
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

        file_handler = logging.FileHandler(log_file, encoding=encoding)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Добавляем вывод в консоль
    if to_stdout:
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    return logger
