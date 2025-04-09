import os
import yadisk
import pandas as pd

# Токен
yadisk_token = "token"

# Пути к файлам
csv_file_path = "/Users/nadezdaoskina/Документы/data_science/data/user_logs.csv"  # Новый путь!
xlsx_file_path = "/Users/nadezdaoskina/Документы/data_science/data/user_logs.xlsx"  # Новый путь!
disk_file_path = "nadarsa_bot.xlsx"

# Конвертируем csv в xlsx
def convert_csv_to_xlsx(csv_path, xlsx_path):
    
    try:
        data = pd.read_csv(csv_path)
        data.to_excel(xlsx_path, index=False)
        print(f"csv преобразован в excel: {xlsx_path}")
    except Exception as e:
        print(f"Ошибка при конвертации csv в excel: {e}")

# Отправляем в Яндекс.Диск
def transfer_to_yadisk(local_file_path, disk_file_path):
    client = yadisk.Client(token=yadisk_token)
    
    # Проверка токена
    if client.check_token():
        print('Токен валиден, можно приступать к работе с файлам на Яндекс.Диске')
    else:
        print('Токен не валиден, получите его заново')
        return 
        
    try:
        client.upload(local_file_path, disk_file_path, overwrite=True)
        print(f'Файл {local_file_path} успешно загружен на Яндекс.Диск')
    except Exception as e:
        print(f'Не удалось загрузить файл: {e}')        

if __name__ == "__main__":
    convert_csv_to_xlsx(csv_file_path, xlsx_file_path)
    transfer_to_yadisk(xlsx_file_path, disk_file_path)

    