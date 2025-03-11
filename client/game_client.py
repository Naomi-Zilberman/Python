import requests
import time
import re
from datetime import datetime, timezone
from colorama import Fore, Back, Style, init
init(autoreset=True)
import time
import os
BASE_URL = 'http://127.0.0.1:5000'

# 1. הלוגו של המשחק
def display_logo():
    os.system('cls' if os.name == 'nt' else 'clear')#ניקוי המסך
    print(f"{Fore.BLUE}{Style.BRIGHT}🚀 ברוכים הבאים למשחק המדהים שלנו! 🚀\n")
    time.sleep(0.5)
    final_logo = f"""
{Fore.YELLOW}    _    _  
{Fore.YELLOW}   | |  | | 
{Fore.YELLOW}   | |__| | {Fore.GREEN}__ _ _ __   __ _ _ __ ___   __ _ _ __
{Fore.YELLOW}   |  __  | {Fore.GREEN}/ _` | '_ \\ / _` | '_ ` _ \\ / _` | '_ \\
{Fore.YELLOW}   | |  | | {Fore.GREEN}(_| | | | | (_| | | | | | | (_| | | | |
{Fore.YELLOW}   |_|  |_| {Fore.GREEN}\\__,_|_| |_|\\__, |_| |_| |_|\\__,_|_| |_|
{Fore.GREEN}                        __/ | 
{Fore.GREEN}                       |___/ 
{Style.BRIGHT}
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    print(final_logo)
    print(f"{Fore.CYAN}{Style.BRIGHT}✨ הבה נתחיל... ✨\n")

# פונקציה לבדוק אם שם המשתמש תקין
def is_valid_username(username):
    return re.match("^[a-zA-Z0-9_א-ת]{3,20}$", username) is not None
# פונקציה לבדוק אם הסיסמה תקינה
def is_valid_password(password):
    return len(password) >= 6  # סיסמה חייבת להיות באורך מינימלי של 6 תווים

# 2. הרשמה
def register():
    while True:
        username = input(Style.BRIGHT + "🔑 הזן שם משתמש: ")
        password = input(Style.BRIGHT + "🔒 הזן סיסמה: ")
        if not is_valid_username(username):
            print(Fore.RED +"❌ שם משתמש לא תקין! חייב להיות בין 3 ל-20 תווים ולהכיל רק תווים חוקיים.")
            continue
        if not is_valid_password(password):
            print( Fore.RED +"❌ סיסמה לא תקינה! חייבת להיות באורך מינימלי של 6 תווים.")
            continue

        url = f'{BASE_URL}/register'
        data = {'username': username, 'password': password}
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("✅" +Fore.YELLOW + response.json()['message'])
            return username, password
        else:
            print(Fore.RED +f"❌ שגיאה: {response.json()['message']}")

# 3. התחברות
def login():
    while True:
        username = input(Style.BRIGHT + "🔑 הזן שם משתמש לצורך התחברות למערכת: ")
        password = input(Style.BRIGHT + "🔒 הזן סיסמה: ")

        if not is_valid_username(username):
            print(Fore.RED + "❌ שם משתמש לא תקין! חייב להיות בין 3 ל-20 תווים ולהכיל רק תווים חוקיים.")
            continue

        if not is_valid_password(password):
            print(Fore.RED + "❌ סיסמה לא תקינה! חייבת להיות באורך מינימלי של 6 תווים.")
            continue

        url = f'{BASE_URL}/login'
        data = {'username': username, 'password': password}
        response = requests.post(url, json=data)

        if response.status_code == 200:
            print(Fore.YELLOW + f"✅ {response.json()['message']}")
            cookies = response.cookies  # שומר את הקוקיז של המשתמש המחובר
            return cookies  # מחזיר את ה-cookies ומסיים את הפונקציה
        else:
            print(Fore.RED + f"❌ שגיאה: {response.json()['message']}")

# 4. התחלת משחק
def start_game(cookies,position):
    cookies = check_cookie_expiration(cookies)
    if cookies is None:
        return

    print(type(position))
    url = f'{BASE_URL}/start_game'
    data = {'position': position}
    username = cookies.get('username')
    if not username:
        print(Fore.RED +"❌ שגיאה: המשתמש לא מחובר!")
        return None

    response = requests.post(url, json=data, cookies=cookies)
    if response.status_code == 200:
        selected_word = response.json().get('selected_word')
        return selected_word
    else:
        print(Fore.RED +f"❌ שגיאה: {response.json()['message']}")
        return None

# 5. התנתקות
def logout(cookies):
    url = f'{BASE_URL}/logout'
    response = requests.post(url, cookies=cookies)
    if response.status_code == 200:
        print("✅ " +Fore.GREEN + response.json()['message'])
    else:
        print(Fore.RED +f"❌ שגיאה: {response.json()['message']}")

# 6. משחק
def load_hangman_stages(file_path):
    try:
        with open('hangman_stages.txt', 'r', encoding='utf-8') as file:
            stages = file.read().split('\n\n')  # פיצול לשלבים לפי רווחים בקובץ
            return stages
    except FileNotFoundError:
        print(Fore.RED +"❌ שגיאה: קובץ שלבי הציור לא נמצא.")
        return []

def update_game_status(cookies):

    url = f'{BASE_URL}/update_victory'
    response = requests.post(url, cookies=cookies)
    if response.status_code == 200:
        print(Fore.GREEN +"✅ מספר המשחקים עודכן בהצלחה!")
    else:
        print(Fore.RED +f"❌ שגיאה: {response.json()['message']}")

def play_game(cookies):
    cookies = check_cookie_expiration(cookies)
    if cookies is None:
        return

    hangman_stages = load_hangman_stages("hangman_stages")
    if not hangman_stages:
        print(Fore.RED +"❌ לא ניתן להתחיל את המשחק ללא שלבי הציור.")
        return

    # בקשה מהמשתמש להזין מספר למיקום עם בדיקת תקינות
    while True:
        user_input = input("אנא הזן מספר: ")

        try:
            position = int(user_input)  # מנסה להמיר למספר עשרוני
            print(f"הערך שהוזן הוא מספר: {position}")
            break
        except ValueError:
            print("שגיאה: הערך שהוזן אינו תקין.")
    cookies = check_cookie_expiration(cookies)
    if cookies is None:
        print(Fore.RED +"❌ הסשן פג. אנא התחבר שוב.")
        return
    word = start_game(cookies, position)  # שולח את המספר שהוזן

    if word:
        masked_word = ["_" if letter != " " else " " for letter in word]  # מחליף אותיות במרכאות ומציג רווחים
        print(f"🔤 מילה: {''.join(masked_word)}")

        incorrect_guesses = 0
        max_incorrect = len(hangman_stages)  # מספר השלבים הוא מספר הפסילות המרבי
        print(f'📉 מספר הפסילות: {max_incorrect}')
        guessed_letters = []

        while incorrect_guesses < max_incorrect:

            guess = input("🔤 נחש אות: ").lower()

            cookies = check_cookie_expiration(cookies)
            if cookies is None:
                print(Fore.RED +"❌ הסשן פג. אנא התחבר שוב.")
                return

            if guess in guessed_letters:
                print(Fore.RED +f"❌ כבר ניחשת את {guess}. נסה שוב.")
                continue

            guessed_letters.append(guess)

            if guess in word:
                print(f"👍 ניחוש טוב! {guess} נמצא במילה.")
                for i, letter in enumerate(word):
                    if letter == guess:
                        masked_word[i] = letter
                print(f"🔤 מילה: {''.join(masked_word)}")

                if "_" not in masked_word:
                    print(Fore.GREEN +"🎉 מזל טוב, ניצחת!")
                    # קריאה לפונקציית עדכון מספר המשחקים
                    update_game_status(cookies)
                    break
            else:
                incorrect_guesses += 1
                print(Fore.RED +f"❌ ניחוש שגוי. נותרו {max_incorrect - incorrect_guesses} ניסיונות.")
                if incorrect_guesses < len(hangman_stages):  # בדיקה שהאינדקס בתווך
                    print(hangman_stages[incorrect_guesses])  # מציג את הציור של שלב הפסילה
                else:
                    print("🚫 אין עוד שלבים left.")

        # אחרי ניצחון או הפסד, מבקש מהמשתמש לבחור:
        action = input("מה תרצה לעשות עכשיו? (1) לשחק שוב (2) התנתקות (3) צפייה בהיסטוריה: ")
        if action == '1':
            play_game(cookies)  # מתחיל משחק חדש
        elif action == '2':
            logout(cookies)  # התנתקות
        elif action == '3':
            view_history(cookies)  # מציג את ההיסטוריה

def view_history(cookies):
    cookies = check_cookie_expiration(cookies)
    if cookies is None:
        return  #
    # שליפת נתוני ההיסטוריה
    url = f'{BASE_URL}/get_history'
    username = cookies.get('username')
    if not username:
        print(Fore.RED +"❌ שגיאה: המשתמש לא מחובר!")
        action = input("מה תרצה לעשות עכשיו? התנתקות (1) התחבר (2): ")
        if action == '2':
            cookies = login()
            if cookies:
                play_game(cookies)
            else:
                print("🚪 מתנתק...")
                logout(cookies)
                return None

        return

    response = requests.get(url, cookies=cookies)
    if response.status_code == 200:
        user_history = response.json()
        print(f"🕹️ משחקים ששוחקו: {user_history['games_played']}")
        print(f"🏆 ניצחונות: {user_history['wins']}")
        print("🔤 מילים ששוחקו:")
        for word in user_history['word_history']:
            print(word)
    else:
        print(Fore.RED +f"❌ שגיאה: {response.json()['message']}")

def check_cookie_expiration(cookies):

    session_expiration = cookies.get('session_expiration')
    if session_expiration:
        session_expiration = session_expiration.strip('"')
        expiration_time = datetime.strptime(session_expiration, '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
    else:
        print(Fore.RED +"❌ הסשן שלך פג. אנא התחבר שוב.")
        action = input("מה תרצה לעשות? (1) התנתקות (2) התחבר: ")
        if action == '1':
            logout(cookies)
            return None
        elif action == '2':
            cookies = login()
            if cookies:
                return cookies
            else:
                print(Fore.RED +"❌ התחברות נכשלה. אנא נסה שוב.")
                return None

    if datetime.now(timezone.utc) >= expiration_time:
        print( Fore.RED +"❌ הסשן שלך פג. אנא התחבר שוב.")
        action = input("מה תרצה לעשות? (1) התנתקות (2) התחבר: ")
        if action == '1':
            logout(cookies)
            return None
        elif action == '2':
            cookies = login()
            if cookies:
                return cookies
            else:
                print(Fore.RED +"❌ התחברות נכשלה. אנא נסה שוב.")
                return None

    return cookies

def main():
    display_logo()
    while True:
        action = input("מה תרצה לעשות? (1) התחבר (2) הרשמה: ")
        if action == '1':
            cookies = login()
            break  # יציאה מהלולאה אם ההתחברות הצליחה
        elif action == '2':
            username, password = register()
            cookies = login()
            break  # יציאה מהלולאה אם ההתחברות הצליחה
        else:
            print("שגיאה: אנא הזן 1 או 2.")  # טיפול במקרה של קלט לא תקין
    if cookies and check_cookie_expiration(cookies):
        play_game(cookies)

if __name__ == "__main__":
    main()
print()