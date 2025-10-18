import random
import json
import time
import os
from datetime import datetime

class NumberGuessingGame:
    def __init__(self):
        # Используем домашнюю директорию для файлов
        home_dir = os.path.expanduser("~")
        self.stats_file = os.path.join(home_dir, "number_guess_game_stats.json")
        self.save_file = os.path.join(home_dir, "number_guess_game_save.json")
        self.stats = self.load_stats()
        self.current_game = None
        
    def get_safe_file_path(self, filename):
        """Получает безопасный путь для файла"""
        # Пробуем несколько мест для сохранения
        possible_paths = [
            os.path.expanduser("~"),  # Домашняя директория
            os.getcwd(),  # Текущая рабочая директория
            os.path.join(os.path.expanduser("~"), "Documents"),  # Документы
        ]
        
        for path in possible_paths:
            file_path = os.path.join(path, filename)
            try:
                # Проверяем, можем ли мы писать в эту директорию
                test_file = os.path.join(path, "test_write.tmp")
                with open(test_file, 'w') as f:
                    f.write("test")
                os.remove(test_file)
                return file_path
            except (IOError, OSError):
                continue
        
        # Если ни одна директория не подошла, используем текущую
        return filename
    
    def load_stats(self):
        """Загрузка статистики из файла"""
        try:
            if os.path.exists(self.stats_file):
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️ Не удалось загрузить статистику: {e}")
            print("📊 Будет создана новая статистика")
        
        # Стандартная статистика
        return {
            "total_games": 0,
            "wins": 0,
            "best_score": float('inf'),
            "average_attempts": 0,
            "games_history": []
        }
    
    def save_stats(self):
        """Сохранение статистики в файл"""
        try:
            # Создаем директорию, если её нет
            os.makedirs(os.path.dirname(self.stats_file), exist_ok=True)
            
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"⚠️ Не удалось сохранить статистику: {e}")
            print("📊 Статистика будет сохранена только в памяти")
            return False
    
    def save_game(self):
        """Сохранение текущей игры"""
        if self.current_game:
            try:
                save_data = {
                    "number": self.current_game["number"],
                    "attempts": self.current_game["attempts"],
                    "max_attempts": self.current_game["max_attempts"],
                    "range_min": self.current_game["range_min"],
                    "range_max": self.current_game["range_max"],
                    "start_time": self.current_game["start_time"],
                    "hints_used": self.current_game["hints_used"]
                }
                
                # Создаем директорию, если её нет
                os.makedirs(os.path.dirname(self.save_file), exist_ok=True)
                
                with open(self.save_file, 'w', encoding='utf-8') as f:
                    json.dump(save_data, f, ensure_ascii=False, indent=2)
                print("💾 Игра сохранена! Вы можете продолжить позже.")
                return True
            except Exception as e:
                print(f"⚠️ Не удалось сохранить игру: {e}")
                return False
        return False
    
    def load_game(self):
        """Загрузка сохраненной игры"""
        try:
            if os.path.exists(self.save_file):
                with open(self.save_file, 'r', encoding='utf-8') as f:
                    save_data = json.load(f)
                
                # Восстанавливаем состояние игры
                self.current_game = {
                    "number": save_data["number"],
                    "attempts": save_data["attempts"],
                    "max_attempts": save_data["max_attempts"],
                    "range_min": save_data["range_min"],
                    "range_max": save_data["range_max"],
                    "start_time": save_data["start_time"],
                    "hints_used": save_data["hints_used"],
                    "remaining_attempts": save_data["max_attempts"] - len(save_data["attempts"])
                }
                
                print("🎮 Загружена сохраненная игра!")
                print(f"📊 Попыток сделано: {len(self.current_game['attempts'])}")
                print(f"🎯 Диапазон: {self.current_game['range_min']}-{self.current_game['range_max']}")
                return True
        except Exception as e:
            print(f"⚠️ Не удалось загрузить сохраненную игру: {e}")
        return False
    
    def safe_file_operation(self, operation, file_path):
        """Безопасное выполнение файловых операций"""
        try:
            return operation(file_path)
        except PermissionError:
            print(f"❌ Нет прав доступа к файлу: {file_path}")
            return False
        except OSError as e:
            print(f"❌ Ошибка файловой системы: {e}")
            return False
    
    def display_instructions(self):
        """Отображение инструкций по игре"""
        print("\n" + "="*50)
        print("🎯 ДОБРО ПОЖАЛОВАТЬ В ИГРУ 'УГАДАЙ ЧИСЛО'!")
        print("="*50)
        print("📋 ПРАВИЛА ИГРЫ:")
        print("   • Я загадаю число в указанном диапазоне")
        print("   • Вы должны угадать это число")
        print("   • После каждой попытки я подскажу, больше или меньше ваше число")
        print("   • У вас ограниченное количество попыток")
        print("\n🎮 КОМАНДЫ:")
        print("   • 'hint' - получить подсказку (стоит 1 попытку)")
        print("   • 'save' - сохранить игру")
        print("   • 'quit' - выйти из игры")
        print("   • 'stats' - показать статистику")
        print("   • 'restart' - начать новую игру")
        print("="*50)
    
    def choose_difficulty(self):
        """Выбор уровня сложности"""
        print("\n🎯 ВЫБЕРИТЕ УРОВЕНЬ СЛОЖНОСТИ:")
        print("1. Легкий (1-50, 10 попыток)")
        print("2. Средний (1-100, 8 попыток)")
        print("3. Сложный (1-200, 6 попыток)")
        print("4. Эксперт (1-500, 5 попыток)")
        print("5. Настроить вручную")
        
        while True:
            choice = input("\nВаш выбор (1-5): ").strip()
            if choice == '1':
                return 1, 50, 10
            elif choice == '2':
                return 1, 100, 8
            elif choice == '3':
                return 1, 200, 6
            elif choice == '4':
                return 1, 500, 5
            elif choice == '5':
                return self.custom_settings()
            else:
                print("❌ Неверный выбор. Попробуйте снова.")
    
    def custom_settings(self):
        """Настройка пользовательских параметров"""
        print("\n⚙️ НАСТРОЙКА ПАРАМЕТРОВ ИГРЫ:")
        
        while True:
            try:
                min_range = int(input("Минимальное число: "))
                max_range = int(input("Максимальное число: "))
                if min_range >= max_range:
                    print("❌ Минимальное число должно быть меньше максимального!")
                    continue
                
                max_attempts = int(input("Количество попыток: "))
                if max_attempts <= 0:
                    print("❌ Количество попыток должно быть положительным!")
                    continue
                
                return min_range, max_range, max_attempts
            except ValueError:
                print("❌ Пожалуйста, введите целое число!")
    
    def get_hint(self, attempts, max_attempts, number, range_min, range_max):
        """Предоставление подсказки"""
        if max_attempts - len(attempts) <= 1:
            print("⚠️ Нельзя использовать подсказку - осталась последняя попытка!")
            return False
        
        hint_type = random.choice(['range', 'even_odd', 'multiple'])
        
        if hint_type == 'range':
            # Подсказка о диапазоне
            range_size = (range_max - range_min) // 4
            lower_bound = max(range_min, number - range_size)
            upper_bound = min(range_max, number + range_size)
            print(f"💡 Подсказка: Число между {lower_bound} и {upper_bound}")
        
        elif hint_type == 'even_odd':
            # Подсказка о четности
            if number % 2 == 0:
                print("💡 Подсказка: Число четное")
            else:
                print("💡 Подсказка: Число нечетное")
        
        elif hint_type == 'multiple':
            # Подсказка о кратности
            multiples = [2, 3, 5, 10]
            for multiple in multiples:
                if number % multiple == 0:
                    print(f"💡 Подсказка: Число делится на {multiple}")
                    break
            else:
                print("💡 Подсказка: Число простое")
        
        return True
    
    def validate_input(self, user_input, range_min, range_max):
        """Валидация пользовательского ввода"""
        # Специальные команды
        if user_input.lower() in ['hint', 'save', 'quit', 'stats', 'restart']:
            return user_input.lower()
        
        try:
            number = int(user_input)
            if range_min <= number <= range_max:
                return number
            else:
                print(f"❌ Число должно быть в диапазоне {range_min}-{range_max}!")
                return None
        except ValueError:
            print("❌ Пожалуйста, введите целое число или команду!")
            return None
    
    def display_progress(self, attempts, max_attempts, number):
        """Отображение прогресса игры"""
        remaining = max_attempts - len(attempts)
        print(f"\n📊 Прогресс: {len(attempts)}/{max_attempts} попыток")
        print(f"🎯 Осталось попыток: {remaining}")
        
        if attempts:
            last_attempt = attempts[-1]
            if last_attempt < number:
                print("📈 Последняя попытка: СЛИШКОМ МАЛЕНЬКОЕ число")
            else:
                print("📉 Последняя попытка: СЛИШКОМ БОЛЬШОЕ число")
        
        # Визуальный индикатор прогресса
        progress_bar = "[" + "█" * len(attempts) + "○" * remaining + "]"
        print(f"📏 {progress_bar}")
    
    def show_stats(self):
        """Отображение статистики"""
        stats = self.stats
        print("\n" + "="*40)
        print("📈 СТАТИСТИКА ИГРЫ")
        print("="*40)
        print(f"🎮 Всего игр: {stats['total_games']}")
        print(f"🏆 Побед: {stats['wins']}")
        
        if stats['wins'] > 0:
            win_rate = (stats['wins'] / stats['total_games']) * 100
            print(f"📊 Процент побед: {win_rate:.1f}%")
            print(f"⭐ Лучший результат: {stats['best_score']} попыток")
            print(f"📊 Среднее количество попыток: {stats['average_attempts']:.1f}")
        
        if stats['games_history']:
            print(f"\n📅 Последние игры:")
            for game in stats['games_history'][-5:]:  # Последние 5 игр
                status = "🏆 Выиграл" if game['won'] else "💀 Проиграл"
                print(f"   • {game['date']}: {status} за {game['attempts']} попыток")
        
        # Показываем где хранится статистика
        print(f"\n💾 Файл статистики: {self.stats_file}")
        print("="*40)
    
    def update_stats(self, won, attempts_count, number_range):
        """Обновление статистики"""
        self.stats['total_games'] += 1
        
        if won:
            self.stats['wins'] += 1
            if attempts_count < self.stats['best_score']:
                self.stats['best_score'] = attempts_count
            
            # Обновление среднего количества попыток
            total_wins = self.stats['wins']
            if total_wins == 1:
                self.stats['average_attempts'] = attempts_count
            else:
                current_avg = self.stats['average_attempts']
                self.stats['average_attempts'] = (current_avg * (total_wins - 1) + attempts_count) / total_wins
        
        # Добавление в историю
        game_record = {
            'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'won': won,
            'attempts': attempts_count,
            'range': f"{number_range[0]}-{number_range[1]}"
        }
        self.stats['games_history'].append(game_record)
        
        # Сохраняем только последние 20 игр
        if len(self.stats['games_history']) > 20:
            self.stats['games_history'] = self.stats['games_history'][-20:]
        
        # Пытаемся сохранить статистику, но не прерываем игру при ошибке
        if not self.save_stats():
            print("💡 Статистика будет сохранена только в памяти этой сессии")
    
    def play_game(self):
        """Основная игровая логика"""
        # Загрузка сохраненной игры или начало новой
        if not self.load_game():
            range_min, range_max, max_attempts = self.choose_difficulty()
            number = random.randint(range_min, range_max)
            
            self.current_game = {
                "number": number,
                "attempts": [],
                "max_attempts": max_attempts,
                "range_min": range_min,
                "range_max": range_max,
                "start_time": time.time(),
                "hints_used": 0,
                "remaining_attempts": max_attempts
            }
        
        print(f"\n🎮 ИГРА НАЧАЛАСЬ!")
        print(f"🎯 Угадайте число от {self.current_game['range_min']} до {self.current_game['range_max']}")
        print(f"📊 У вас {self.current_game['max_attempts']} попыток")
        
        game_won = False
        
        while len(self.current_game['attempts']) < self.current_game['max_attempts']:
            self.display_progress(
                self.current_game['attempts'], 
                self.current_game['max_attempts'], 
                self.current_game['number']
            )
            
            user_input = input("\n🎲 Ваша догадка (или команда): ").strip()
            
            # Валидация ввода
            validated_input = self.validate_input(
                user_input, 
                self.current_game['range_min'], 
                self.current_game['range_max']
            )
            
            if validated_input is None:
                continue
            
            # Обработка команд
            if validated_input == 'hint':
                if self.get_hint(
                    self.current_game['attempts'],
                    self.current_game['max_attempts'],
                    self.current_game['number'],
                    self.current_game['range_min'],
                    self.current_game['range_max']
                ):
                    self.current_game['attempts'].append(-1)  # Специальная отметка для подсказки
                    self.current_game['hints_used'] += 1
                continue
            
            elif validated_input == 'save':
                self.save_game()
                continue
            
            elif validated_input == 'quit':
                save_choice = input("Сохранить игру перед выходом? (y/n): ").lower()
                if save_choice in ['y', 'yes', 'да']:
                    self.save_game()
                print("👋 До свидания!")
                return
            
            elif validated_input == 'stats':
                self.show_stats()
                continue
            
            elif validated_input == 'restart':
                restart = input("Начать новую игру? Текущий прогресс будет потерян. (y/n): ").lower()
                if restart in ['y', 'yes', 'да']:
                    # Удаляем файл сохранения
                    try:
                        if os.path.exists(self.save_file):
                            os.remove(self.save_file)
                    except:
                        pass  # Игнорируем ошибки удаления
                    return self.play_game()
                continue
            
            # Обработка числового ввода
            guess = validated_input
            self.current_game['attempts'].append(guess)
            
            if guess == self.current_game['number']:
                game_won = True
                break
            elif guess < self.current_game['number']:
                print("📈 СЛИШКОМ МАЛЕНЬКОЕ число! Попробуйте еще раз.")
            else:
                print("📉 СЛИШКОМ БОЛЬШОЕ число! Попробуйте еще раз.")
        
        # Завершение игры
        game_time = time.time() - self.current_game['start_time']
        attempts_count = len([x for x in self.current_game['attempts'] if x != -1])  # Исключаем подсказки
        
        print("\n" + "="*50)
        if game_won:
            print("🎉 ПОЗДРАВЛЯЕМ! ВЫ УГАДАЛИ ЧИСЛО! 🎉")
            print(f"🔢 Загаданное число: {self.current_game['number']}")
            print(f"📊 Количество попыток: {attempts_count}")
            print(f"⏱️ Время игры: {game_time:.1f} секунд")
            if self.current_game['hints_used'] > 0:
                print(f"💡 Использовано подсказок: {self.current_game['hints_used']}")
        else:
            print("💀 ИГРА ОКОНЧЕНА! ВЫ НЕ УГАДАЛИ ЧИСЛО")
            print(f"🔢 Загаданное число было: {self.current_game['number']}")
            print(f"📊 Сделано попыток: {attempts_count}")
        
        print("="*50)
        
        # Обновление статистики
        self.update_stats(
            game_won, 
            attempts_count,
            (self.current_game['range_min'], self.current_game['range_max'])
        )
        
        # Удаление файла сохранения
        try:
            if os.path.exists(self.save_file):
                os.remove(self.save_file)
        except:
            pass  # Игнорируем ошибки удаления
    
    def main_menu(self):
        """Главное меню программы"""
        while True:
            self.display_instructions()
            
            print("\n🎮 ГЛАВНОЕ МЕНЮ:")
            print("1. Начать новую игру")
            print("2. Продолжить сохраненную игру")
            print("3. Показать статистику")
            print("4. Выйти из игры")
            
            choice = input("\nВаш выбор (1-4): ").strip()
            
            if choice == '1':
                # Удаляем предыдущее сохранение
                try:
                    if os.path.exists(self.save_file):
                        os.remove(self.save_file)
                except:
                    pass
                self.play_game()
            elif choice == '2':
                if not self.load_game():
                    print("❌ Нет сохраненной игры!")
                    continue
                self.play_game()
            elif choice == '3':
                self.show_stats()
            elif choice == '4':
                print("👋 Спасибо за игру! До свидания!")
                break
            else:
                print("❌ Неверный выбор. Попробуйте снова.")

def main():
    """Основная функция программы"""
    try:
        game = NumberGuessingGame()
        game.main_menu()
    except KeyboardInterrupt:
        print("\n\n👋 Игра прервана. До свидания!")
    except Exception as e:
        print(f"\n❌ Произошла непредвиденная ошибка: {e}")
        print("Пожалуйста, перезапустите игру.")

if __name__ == "__main__":
    main()
