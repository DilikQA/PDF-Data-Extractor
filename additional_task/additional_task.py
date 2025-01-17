import json


def process_table(table, base_ws):
    """
    Преобразует таблицу в JSON-запрос, сопоставляя ключи таблицы с значениями из base_ws.

    Args:
        table (list of dict): Таблица с данными.
        base_ws (dict): Базовые значения из вебсокета.

    Returns:
        dict: Собранный результат в формате JSON.
    """
    result = {}

    for row in table:
        for key, value in row.items():
            # Если ключ присутствует в base_ws, добавляем его в результат
            if key in base_ws:
                result[key] = base_ws[key]
            else:
                # Обработка случая, когда ключ отсутствует в base_ws
                print(f"Warning: Key '{key}' not found in base_ws. Skipping this key.")

    # Возвращаем собранный результат в формате JSON
    return json.dumps(result, ensure_ascii=False, indent=4)


# Пример данных
my_table = [
    {"key1": "value1"},
    {"key2": "value2"},
    {"key3": "value3"},
]

base_ws_response = {
    "key1": "base_value1",
    "key2": "base_value2",
    "key4": "base_value4",  # Пример лишнего ключа

}

# Преобразование таблицы в запрос
result_json = process_table(my_table, base_ws_response)

# Вывод результата
print("Result JSON:")
print(result_json)
