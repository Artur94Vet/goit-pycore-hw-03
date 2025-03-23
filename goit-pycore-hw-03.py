'''
Вітаю!
Доьашнє завдання до модуля 4.
Також використовував Chat GPT для створення якоїсь інтерактивної логіки (самому виявилось ще занадто важко), щоб було цікавіше
З подальших конспектів я розумію, що варто було розділити на різні модулі, але тут все лишив в одному..
Відповідно домашнє завдання можна перевірити з терміналу..
'''
# імпортую всі необхідні модулі для виконання завдань
from datetime import datetime, date, timedelta
import random
import re


#-------------------------Функції для виконання завдань

# Завдання №1: Обчислення кількості днів від введеної дати
# def створюю функцію
def get_days_from_today(date_str):
    try:
        input_date = datetime.strptime(date_str, "%Y-%m-%d").date() # перетворюю введене значення у формат дати
        today = date.today() # визначаю дату сьогодні
        diff = today - input_date # просто обчислюю різницю
        return diff.days # повертаю значення
    except ValueError: # якщо помилка, то нічого не повертаю
        return None

# Завдання №2: Лотерея - генерує виграшну комбінацію чисел
# def створюю функцію
def get_numbers_ticket(min_num, max_num, quantity):
    if not (1 <= min_num <= max_num <= 1000 and quantity <= (max_num - min_num + 1)): # прописуємо умови (але для чого в завданні не більше 1000, не розумію, оскільки є чіткі умови відбору)
        return []
    numbers = random.sample(range(min_num, max_num + 1), quantity) # формуємо список з рандомних чисел (згідно вищеописаних умов)
    return sorted(numbers) # повертаємо відсортований список

# Завдання №3: Нормалізація телефонних номерів для SMS-розсилки
# def створюю функцію (в завданні були чітко описані приклади)
def normalize_phone(phone_number):
    cleaned_number = re.sub(r"[^\d+]", "", phone_number) # очищаємо масив з номерами від всих зайвих знаків
    if cleaned_number.startswith("+380"): # створюємо умову для перевірки початку номеру, враховуючи, що це український оператор
        return cleaned_number
    elif cleaned_number.startswith("380"):
        return "+" + cleaned_number
    else:
        return "+38" + cleaned_number
# на майбутнє варто розглянути телефонні номера інших країн, оскільки їх обрабка в коді не передбачена

# Завдання №4: Визначення колег, яких потрібно привітати з днем народження
# def створюю функцію (уявний список внизу модуля)
def get_upcoming_birthdays(users):
    today = datetime.today().date() # визначеємо дату сьогодні (лише дату)
    upcoming_birthdays = [] # створюємо список
    
    for user in users:
        birthday = datetime.strptime(user["birthday"], "%Y.%m.%d").date() # перетворюємо на формат дати
        birthday_this_year = birthday.replace(year=today.year)# Формуємо дату дня народження для поточного року
        if birthday_this_year < today:
            birthday_this_year = birthday.replace(year=today.year + 1) # Якщо день народження цього року вже пройшов (або сьогодні його не досягли),використовуємо дату наступного року
        days_difference = (birthday_this_year - today).days# Обчислюємо кількість днів до наступного дня народження
        if 0 <= days_difference <= 7:# Якщо наступний день народження припадає на 7 або менше днів від сьогодні
            # Якщо дата дня народження припадає на вихідний (субота або неділя),
            # переносимо привітання на наступний понеділок
            if birthday_this_year.weekday() >= 5:  # 5 – субота, 6 – неділя
                days_to_monday = 7 - birthday_this_year.weekday()
                congratulation_date = birthday_this_year + timedelta(days=days_to_monday)
            else:
                congratulation_date = birthday_this_year
            
            upcoming_birthdays.append({
                "Ім'я": user["name"],
                "День народження:": congratulation_date.strftime("%Y.%m.%d")
            })
    
    return upcoming_birthdays

#-------------------------Логіка роботи з користувачем

# Головне меню
def main():
    while True:
        print("\nОберіть завдання для перевірки:")
        print("1. Завдання №1: Обчислення днів від введеної дати")
        print("2. Завдання №2: Лотерея")
        print("3. Завдання №3: Нормалізація телефонних номерів")
        print("4. Завдання №4: Привітання з днем народження")
        print("5. Завершити роботу")
        
        choice = input("Введіть номер завдання (1-4) або 5 для виходу: ").strip()
        
        if choice == "5":
            print("Вихід з програми. Гарного дня!")
            break
        
        if choice == "1":
            # Завдання №1
            while True:
                date_input = input("Введіть дату у форматі YYYY-MM-DD або 'назад' для повернення в головне меню: ").strip()
                if date_input.lower() == "назад":
                    break
                result = get_days_from_today(date_input)
                if result is not None:
                    print(f"Кількість днів від введеної дати: {result}")
                    break
                else:
                    print("Невірний формат дати! Спробуйте ще раз.")
        
        elif choice == "2":
            # Завдання №2
            while True:
                print("Лотерея: Введіть свої 6 чисел, розділяючи їх пробілом:")
                user_numbers_input = input("Ваші числа: ")
                user_numbers = user_numbers_input.strip().split()
                if len(user_numbers) != 6 or not all(num.isdigit() for num in user_numbers):
                    print("Ви повинні ввести рівно 6 цілих чисел. Спробуйте ще раз.")
                    continue
                user_numbers = sorted(int(num) for num in user_numbers)
                winning_combination = get_numbers_ticket(1, 49, 6)
                print(f"Ваші числа: {user_numbers}")
                print(f"Виграшна комбінація: {winning_combination}")
                play_again = input("Хочете зіграти ще? (так/ні): ").strip().lower()
                if play_again != "так":
                    break
        
        elif choice == "3":
            # Завдання №3
            raw_numbers = [
                "067\t123 4567",
                "(095) 234-5678\n",
                "+380 44 123 4567",
                "380501234567",
                "    +38(050)123-32-34",
                "     0503451234",
                "(050)8889900",
                "38050-111-22-22",
                "38050 111 22 11   ",
            ]
            sanitized_numbers = [normalize_phone(num) for num in raw_numbers]
            print("Нормалізовані номери телефонів:")
            for number in sanitized_numbers:
                print(number)
            input("Натисніть Enter для повернення в головне меню...")
        
        elif choice == "4":
            # Завдання №4
            users = [
                {"name": "Тетяна", "birthday": "1985.01.23"},
                {"name": "Аліна", "birthday": "1990.01.27"},
                {"name": "Світлана", "birthday": "1988.09.25"},
                {"name": "Шеф", "birthday": "1974.03.25"},
                {"name": "Анатолій", "birthday": "1990.01.27"},
                {"name": "Сергій", "birthday": "1995.05.27"},
                {"name": "Артур", "birthday": "1994.01.28"},
                {"name": "Ігор", "birthday": "1990.03.27"},
                {"name": "Микола", "birthday": "1990.03.28"},
                {"name": "Валентин", "birthday": "1992.04.27"}
            ]
            upcoming_birthdays = get_upcoming_birthdays(users)
            print("Список привітань на цьому тижні:")
            for record in upcoming_birthdays:
                print(record)
            input("Натисніть Enter для повернення в головне меню...")
        
        else:
            print("Невірний вибір. Будь ласка, оберіть правильний номер завдання.")

if __name__ == "__main__":
    main()
