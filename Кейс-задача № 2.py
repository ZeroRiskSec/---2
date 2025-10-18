import math
import sys

def calculate_factorial_optimized(n):
    """
    Вычисляет факториал числа с использованием math.factorial
    с обработкой больших чисел и ошибок
    """
    try:
        # Проверка на отрицательное число
        if n < 0:
            raise ValueError("Факториал определен только для неотрицательных чисел")
        
        # Вычисление факториала с помощью math.factorial
        result = math.factorial(n)
        return result
        
    except ValueError as e:
        raise e
    except Exception as e:
        raise RuntimeError(f"Ошибка при вычислении факториала: {e}")

def get_user_input():
    """
    Получает и проверяет пользовательский ввод
    """
    while True:
        try:
            user_input = input("Введите целое неотрицательное число для вычисления факториала: ")
            
            # Проверка на команды выхода
            if user_input.lower() in ['выход', 'exit', 'quit', 'q']:
                return None
                
            # Преобразование в целое число
            number = int(user_input)
            
            # Проверка на отрицательное число
            if number < 0:
                print("❌ Ошибка: Факториал определен только для неотрицательных чисел!")
                print("   Пожалуйста, введите число ≥ 0")
                continue
                
            return number
            
        except ValueError:
            print("❌ Ошибка: Введите корректное целое число!")
            print("   Примеры: 0, 5, 10, 100")
            print("   Для выхода введите 'выход', 'exit' или 'quit'")
        except KeyboardInterrupt:
            print("\n\nПрограмма прервана пользователем")
            sys.exit(0)

def format_large_number(number):
    """
    Форматирует большие числа для удобного отображения
    """
    if number < 10**6:
        return str(number)
    else:
        return f"{number:.2e}".replace('e+', ' × 10^')

def display_factorial_info(n, result):
    """
    Отображает информацию о вычисленном факториале
    """
    print("\n" + "="*50)
    print(f"🎯 РЕЗУЛЬТАТ ВЫЧИСЛЕНИЯ ФАКТОРИАЛА")
    print("="*50)
    print(f"📊 Введенное число: {n}")
    print(f"🔢 Факториал {n}! = {format_large_number(result)}")
    print(f"📏 Количество цифр в результате: {len(str(result))}")
    print("="*50)

def calculate_single_factorial():
    """
    Функция для вычисления одного факториала
    """
    try:
        # Получение ввода от пользователя
        number = get_user_input()
        
        # Если пользователь ввел команду выхода
        if number is None:
            return False
        
        # Вычисление факториала
        print(f"\n⏳ Вычисляем факториал числа {number}...")
        
        result = calculate_factorial_optimized(number)
        
        # Отображение результата
        display_factorial_info(number, result)
        
        # Дополнительная информация для больших чисел
        if number > 20:
            print("\n💡 Интересные факты:")
            print(f"   - Факториал {number}! содержит {len(str(result))} цифр")
            if number > 50:
                print("   - Для таких больших чисел используется оптимизированная")
                print("     реализация из библиотеки math")
        
        return True
        
    except MemoryError:
        print("❌ Ошибка: Недостаточно памяти для вычисления такого большого факториала!")
        return True
    except OverflowError:
        print("❌ Ошибка: Результат слишком велик для представления!")
        return True
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")
        return True

def test_factorials():
    """
    Функция для тестирования на различных значениях
    """
    test_cases = [0, 1, 5, 10, 20, 50, 100]
    
    print("\n🧪 ТЕСТИРОВАНИЕ НА РАЗЛИЧНЫХ ЗНАЧЕНИЯХ:")
    print("-" * 40)
    
    for n in test_cases:
        try:
            result = calculate_factorial_optimized(n)
            digits = len(str(result))
            print(f"{n:3}! = {format_large_number(result):>20} ({digits:2} цифр)")
        except Exception as e:
            print(f"{n:3}! = Ошибка: {e}")

def show_menu():
    """
    Показывает главное меню программы
    """
    print("\n" + "="*50)
    print("🔢 ВЫЧИСЛИТЕЛЬ ФАКТОРИАЛА")
    print("="*50)
    print("1. Вычислить факториал")
    print("2. Запустить тесты")
    print("3. Показать справку")
    print("4. Выйти из программы")
    print("="*50)

def show_help():
    """
    Показывает справку по программе
    """
    print("\n📖 СПРАВКА ПО ПРОГРАММЕ:")
    print("-" * 30)
    print("• Программа вычисляет факториал введенного числа")
    print("• Факториал числа n - это произведение всех целых")
    print("  чисел от 1 до n")
    print("• Пример: 5! = 1 × 2 × 3 × 4 × 5 = 120")
    print("• Поддерживаются очень большие числа")
    print("• Для выхода из режима ввода используйте:")
    print("  'выход', 'exit', 'quit' или 'q'")
    print("-" * 30)

def main():
    """
    Основная функция программы с циклом
    """
    print("🔢 ДОБРО ПОЖАЛОВАТЬ В ВЫЧИСЛИТЕЛЬ ФАКТОРИАЛА!")
    print("Программа будет работать до тех пор, пока вы не выберете выход.")
    
    while True:
        show_menu()
        
        try:
            choice = input("\nВыберите действие (1-4): ").strip()
            
            if choice == '1':
                # Режим вычисления факториала
                print("\n🎯 РЕЖИМ ВЫЧИСЛЕНИЯ ФАКТОРИАЛА")
                print("Для возврата в меню введите 'выход'")
                print("-" * 40)
                
                while True:
                    if not calculate_single_factorial():
                        break  # Выход из режима вычисления
                    
                    # Спросить, хочет ли пользователь продолжить вычисления
                    continue_calc = input("\nВычислить еще один факториал? (y/n): ").lower()
                    if continue_calc not in ['y', 'yes', 'да', 'д']:
                        break
            
            elif choice == '2':
                # Запуск тестов
                test_factorials()
                input("\nНажмите Enter для возврата в меню...")
            
            elif choice == '3':
                # Показать справку
                show_help()
                input("\nНажмите Enter для возврата в меню...")
            
            elif choice == '4':
                # Выход из программы
                print("\n✨ Спасибо за использование программы! До свидания! 👋")
                break
            
            else:
                print("❌ Неверный выбор. Пожалуйста, введите число от 1 до 4.")
        
        except KeyboardInterrupt:
            print("\n\n👋 Программа прервана пользователем. До свидания!")
            break
        except Exception as e:
            print(f"❌ Произошла ошибка: {e}")
            print("Продолжаем работу...")

if __name__ == "__main__":
    main()
