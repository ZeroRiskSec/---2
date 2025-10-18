def get_positive_integer():
    """
    Функция для получения положительного целого числа от пользователя.
    
    Returns:
        int: Положительное целое число, введенное пользователем
    """
    while True:
        try:
            # Запрос ввода у пользователя
            user_input = input("Пожалуйста, введите положительное целое число: ").strip()
            
            # Проверка на пустой ввод
            if not user_input:
                print("Ошибка: Ввод не может быть пустым. Попробуйте снова.\n")
                continue
            
            # Преобразование в целое число
            number = int(user_input)
            
            # Проверка, что число положительное
            if number <= 0:
                print("Ошибка: Число должно быть положительным. Попробуйте снова.\n")
                continue
            
            # Если все проверки пройдены
            return number
            
        except ValueError:
            # Обработка случая, когда ввод не может быть преобразован в число
            print(f"Ошибка: '{user_input}' не является целым числом. Попробуйте снова.\n")


class PositiveIntegerValidator:
    """
    Класс для валидации положительных целых чисел с расширенными возможностями.
    """
    
    def __init__(self, min_value=1, max_value=None):
        """
        Инициализация валидатора.
        
        Args:
            min_value (int): Минимальное допустимое значение
            max_value (int): Максимальное допустимое значение (None - без ограничения)
        """
        self.min_value = min_value
        self.max_value = max_value
    
    def validate(self, number):
        """
        Проверка числа на соответствие требованиям.
        
        Args:
            number: Значение для проверки
            
        Returns:
            tuple: (bool, str) - (результат проверки, сообщение об ошибке)
        """
        # Проверка типа данных
        if not isinstance(number, int):
            return False, "Значение должно быть целым числом"
        
        # Проверка минимального значения
        if number < self.min_value:
            return False, f"Число должно быть не меньше {self.min_value}"
        
        # Проверка максимального значения
        if self.max_value is not None and number > self.max_value:
            return False, f"Число должно быть не больше {self.max_value}"
        
        return True, ""
    
    def get_input(self, prompt=None):
        """
        Получение корректного ввода от пользователя.
        
        Args:
            prompt (str): Сообщение для пользователя
            
        Returns:
            int: Валидное положительное целое число
        """
        if prompt is None:
            prompt = f"Пожалуйста, введите положительное целое число"
            if self.min_value != 1 or self.max_value is not None:
                range_info = f" от {self.min_value}"
                if self.max_value is not None:
                    range_info += f" до {self.max_value}"
                prompt += range_info
            prompt += ": "
        
        while True:
            try:
                user_input = input(prompt).strip()
                
                if not user_input:
                    print("Ошибка: Ввод не может быть пустым.\n")
                    continue
                
                number = int(user_input)
                is_valid, error_message = self.validate(number)
                
                if is_valid:
                    return number
                else:
                    print(f"Ошибка: {error_message}\n")
                    
            except ValueError:
                print(f"Ошибка: '{user_input}' не является целым числом.\n")


def show_menu():
    """
    Отображение главного меню программы.
    """
    print("\n" + "=" * 50)
    print("ГЛАВНОЕ МЕНЮ - ВВОД ПОЛОЖИТЕЛЬНЫХ ЦЕЛЫХ ЧИСЕЛ")
    print("=" * 50)
    print("1. Простой ввод положительного числа")
    print("2. Ввод числа с ограничениями")
    print("3. Проверить несколько чисел")
    print("4. Демонстрация работы программы")
    print("5. Тестирование")
    print("0. Выход")
    print("=" * 50)


def simple_input_mode():
    """
    Режим простого ввода числа.
    """
    print("\n--- РЕЖИМ ПРОСТОГО ВВОДА ---")
    number = get_positive_integer()
    print(f"✓ Вы успешно ввели число: {number}")
    
    # Дополнительные действия с числом
    print(f"✓ Квадрат числа: {number ** 2}")
    print(f"✓ Факториал числа: {factorial(number)}")
    input("\nНажмите Enter для продолжения...")


def constrained_input_mode():
    """
    Режим ввода числа с ограничениями.
    """
    print("\n--- РЕЖИМ ВВОДА С ОГРАНИЧЕНИЯМИ ---")
    
    # Настройка ограничений
    while True:
        try:
            min_input = input("Введите минимальное значение (по умолчанию 1): ").strip()
            min_val = int(min_input) if min_input else 1
            
            if min_val < 1:
                print("Ошибка: Минимальное значение должно быть положительным числом.")
                continue
                
            max_input = input("Введите максимальное значение (оставьте пустым для отсутствия ограничения): ").strip()
            max_val = int(max_input) if max_input else None
            
            if max_val is not None and max_val < min_val:
                print(f"Ошибка: Максимальное значение ({max_val}) не может быть меньше минимального ({min_val})")
                continue
                
            break
        except ValueError:
            print("Ошибка: Пожалуйста, введите целое число или оставьте пустым для значений по умолчанию.")
    
    print(f"\nУстановлены ограничения: от {min_val}" + (f" до {max_val}" if max_val else ""))
    
    validator = PositiveIntegerValidator(min_value=min_val, max_value=max_val)
    number = validator.get_input()
    
    print(f"✓ Вы успешно ввели число: {number}")
    print(f"✓ Число соответствует ограничениям: {min_val} ≤ {number}" + 
          (f" ≤ {max_val}" if max_val else ""))
    
    # Показать дополнительные числа в диапазоне
    if max_val is not None and (max_val - min_val) <= 10:
        print(f"✓ Все числа в диапазоне: {list(range(min_val, max_val + 1))}")
    
    input("\nНажмите Enter для продолжения...")


def check_multiple_numbers():
    """
    Режим проверки нескольких чисел.
    """
    print("\n--- ПРОВЕРКА НЕСКОЛЬКИХ ЧИСЕЛ ---")
    numbers = []
    
    # Настройка ограничений для проверки
    use_limits = input("Хотите установить ограничения для чисел? (д/н): ").strip().lower()
    min_val, max_val = 1, None
    
    if use_limits in ['д', 'y', 'да', 'yes']:
        while True:
            try:
                min_input = input("Введите минимальное значение (по умолчанию 1): ").strip()
                min_val = int(min_input) if min_input else 1
                
                if min_val < 1:
                    print("Ошибка: Минимальное значение должно быть положительным числом.")
                    continue
                    
                max_input = input("Введите максимальное значение (оставьте пустым для отсутствия ограничения): ").strip()
                max_val = int(max_input) if max_input else None
                
                if max_val is not None and max_val < min_val:
                    print(f"Ошибка: Максимальное значение ({max_val}) не может быть меньше минимального ({min_val})")
                    continue
                    
                break
            except ValueError:
                print("Ошибка: Пожалуйста, введите целое число.")
    
    validator = PositiveIntegerValidator(min_value=min_val, max_value=max_val)
    limit_info = f" (ограничения: от {min_val}" + (f" до {max_val}" if max_val else "") + ")"
    
    while True:
        print(f"\nТекущий список чисел: {numbers}")
        print(f"Ограничения: от {min_val}" + (f" до {max_val}" if max_val else " без верхнего ограничения"))
        
        choice = input("Добавить число? (д/н): ").strip().lower()
        
        if choice in ['н', 'n', 'нет', 'no']:
            break
        elif choice in ['д', 'y', 'да', 'yes']:
            try:
                user_input = input(f"Введите число{limit_info}: ").strip()
                
                if not user_input:
                    print("Ошибка: Ввод не может быть пустым.")
                    continue
                
                num = int(user_input)
                is_valid, message = validator.validate(num)
                
                if is_valid:
                    numbers.append(num)
                    print(f"✓ Число {num} добавлено")
                else:
                    print(f"✗ Ошибка: {message}")
            except ValueError:
                print("✗ Ошибка: Введенное значение не является целым числом")
        else:
            print("Пожалуйста, введите 'д' или 'н'")
    
    if numbers:
        print(f"\n✓ Итоговый список чисел: {numbers}")
        print(f"✓ Сумма: {sum(numbers)}")
        print(f"✓ Среднее: {sum(numbers) / len(numbers):.2f}")
        print(f"✓ Минимальное: {min(numbers)}")
        print(f"✓ Максимальное: {max(numbers)}")
        
        # Проверка соответствия ограничениям
        invalid_numbers = [num for num in numbers if num < min_val or (max_val is not None and num > max_val)]
        if invalid_numbers:
            print(f"⚠ Нарушают ограничения: {invalid_numbers}")
        else:
            print("✓ Все числа соответствуют установленным ограничениям")
    else:
        print("\nСписок чисел пуст.")
    
    input("\nНажмите Enter для продолжения...")


def factorial(n):
    """
    Вычисление факториала числа.
    """
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def demonstration_mode():
    """
    Режим демонстрации работы программы.
    """
    print("\n--- ДЕМОНСТРАЦИЯ РАБОТЫ ПРОГРАММЫ ---")
    
    # Демонстрация различных сценариев
    test_scenarios = [
        "123",      # корректное число
        "-5",       # отрицательное
        "0",        # ноль
        "abc",      # текст
        "12.5",     # дробное
        "",         # пустой ввод
        "  42  ",   # с пробелами
    ]
    
    print("Демонстрация обработки различных вводов:")
    for scenario in test_scenarios:
        print(f"\nТест: '{scenario}'")
        try:
            # Эмуляция ввода
            if scenario.strip():
                num = int(scenario.strip())
                validator = PositiveIntegerValidator()
                is_valid, message = validator.validate(num)
                if is_valid:
                    print(f"  Результат: ✓ ВАЛИДНО - число {num}")
                else:
                    print(f"  Результат: ✗ НЕВАЛИДНО - {message}")
            else:
                print(f"  Результат: ✗ НЕВАЛИДНО - пустой ввод")
        except ValueError:
            print(f"  Результат: ✗ НЕВАЛИДНО - не является целым числом")
    
    # Демонстрация работы с ограничениями
    print("\n" + "=" * 40)
    print("Демонстрация работы с ограничениями:")
    print("Установлены ограничения: от 10 до 50")
    
    validator_demo = PositiveIntegerValidator(min_value=10, max_value=50)
    test_numbers = [5, 10, 25, 50, 55, "текст"]
    
    for test_num in test_numbers:
        if isinstance(test_num, int):
            is_valid, message = validator_demo.validate(test_num)
            status = "✓ ВАЛИДНО" if is_valid else "✗ НЕВАЛИДНО"
            print(f"  {test_num}: {status} - {message if not is_valid else 'OK'}")
        else:
            print(f"  '{test_num}': ✗ НЕВАЛИДНО - не является числом")
    
    input("\nНажмите Enter для продолжения...")


def testing_mode():
    """
    Режим тестирования программы.
    """
    print("\n--- ТЕСТИРОВАНИЕ ПРОГРАММЫ ---")
    
    # Тесты для базовой валидации
    basic_test_cases = [
        ("5", True, "Корректное положительное число"),
        ("0", False, "Ноль"),
        ("-5", False, "Отрицательное число"),
        ("abc", False, "Текст вместо числа"),
        ("12.5", False, "Дробное число"),
        ("", False, "Пустой ввод"),
        (" 7 ", True, "Число с пробелами"),
        ("1000000", True, "Большое число"),
    ]
    
    # Тесты для ограничений
    limit_test_cases = [
        (5, 1, 10, True, "Число в диапазоне"),
        (0, 1, 10, False, "Ниже минимального"),
        (15, 1, 10, False, "Выше максимального"),
        (10, 1, 10, True, "На границе максимума"),
        (1, 1, 10, True, "На границе минимума"),
    ]
    
    validator_basic = PositiveIntegerValidator()
    passed = 0
    total = len(basic_test_cases) + len(limit_test_cases)
    
    print("Базовые тесты валидации:")
    for test_input, expected, description in basic_test_cases:
        try:
            if test_input == "":
                result = False
            else:
                number = int(test_input.strip())
                result, _ = validator_basic.validate(number)
            
            status = result == expected
            passed += 1 if status else 0
            
            status_symbol = "✓" if status else "✗"
            print(f"  {status_symbol} {description} ('{test_input}') - {'ПРОЙДЕН' if status else 'НЕ ПРОЙДЕН'}")
            
        except ValueError:
            status = False
            status_symbol = "✓" if status == expected else "✗"
            passed += 1 if status == expected else 0
            print(f"  {status_symbol} {description} ('{test_input}') - {'ПРОЙДЕН' if status == expected else 'НЕ ПРОЙДЕН'}")
    
    print("\nТесты с ограничениями:")
    for number, min_val, max_val, expected, description in limit_test_cases:
        validator = PositiveIntegerValidator(min_value=min_val, max_value=max_val)
        result, _ = validator.validate(number)
        status = result == expected
        passed += 1 if status else 0
        
        status_symbol = "✓" if status else "✗"
        range_info = f" ({min_val}-{max_val})"
        print(f"  {status_symbol} {description}: {number}{range_info} - {'ПРОЙДЕН' if status else 'НЕ ПРОЙДЕН'}")
    
    print(f"\nРезультаты тестирования: {passed}/{total} тестов пройдено")
    input("\nНажмите Enter для продолжения...")


def main():
    """
    Основная функция программы с непрерывным циклом работы.
    """
    print("Добро пожаловать в программу для ввода положительных целых чисел!")
    
    while True:
        # Отображение меню
        show_menu()
        
        # Запрос выбора пользователя
        choice = input("Выберите опцию (0-5): ").strip()
        
        # Обработка выбора
        if choice == "0":
            print("\nСпасибо за использование программы! До свидания!")
            break
        elif choice == "1":
            simple_input_mode()
        elif choice == "2":
            constrained_input_mode()
        elif choice == "3":
            check_multiple_numbers()
        elif choice == "4":
            demonstration_mode()
        elif choice == "5":
            testing_mode()
        else:
            print("\nОшибка: Неверный выбор. Пожалуйста, выберите опцию от 0 до 5.")
            input("Нажмите Enter для продолжения...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем. До свидания!")
    except Exception as e:
        print(f"\nПроизошла непредвиденная ошибка: {e}")
        print("Программа будет перезапущена...")
        input("Нажмите Enter для продолжения...")
        main()
