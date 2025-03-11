import json
from flask import Flask, request, jsonify, session, make_response
from datetime import datetime, timedelta
import random
import secrets
import re

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # יצירת מפתח סודי עבור האפליקציה

# פונקציה לטעינת משתמשים מקובץ JSON
def load_users():
    try:
        with open('users.json', 'r', encoding='utf-8') as file:  # פתיחת קריאה
            return json.load(file)  # אם הקובץ קיים, טוען את נתוני המשתמשים
    except FileNotFoundError:
        print("❌ שגיאה: 'users.json' לא נמצא. מתחילים עם רשימת משתמשים ריקה.")
        return {}
    except json.JSONDecodeError:
        print("❌ שגיאה: 'users.json' קובץ לא תקין. מתחילים עם רשימת משתמשים ריקה.")
        return {}

# פונקציה לשמירת משתמשים לקובץ JSON
def save_users():
    try:
        with open('users.json', 'w', encoding='utf-8') as file:  # פתיחת קובץ לשמירה
            json.dump(users, file, ensure_ascii=False, indent=4)  # שמירת המילון של המשתמשים בקובץ
    except IOError:
        print("❌ שגיאה: לא ניתן לשמור את המשתמשים לקובץ 'users.json'.")

# טוען את המשתמשים בהתחלה
users = load_users()

# פונקציה לטעינת מילים מקובץ
def load_words():
    try:
        with open('words.txt', 'r', encoding='utf-8') as file:  # פתיחת קובץ המילים לקריאה
            return [line.strip() for line in file.readlines()]  # הסרת רווחים מיותרים מכל שורה
    except FileNotFoundError:  # אם הקובץ לא נמצא
        print("❌ שגיאה: 'words.txt' לא נמצא.")
        return []
    except IOError:
        print("❌ שגיאה: לא ניתן לקרוא את הקובץ 'words.txt'.")
        return []

words = load_words()  # טוען את המילים
def is_valid_username(username):
    return re.match("^[a-zA-Z0-9_א-ת]{3,20}$", username) is not None  # תווך של 3-20 תווים, תווים חוקיים
def is_valid_password(password):
    return len(password) >= 6  # סיסמה חייבת להיות באורך מינימלי של 6 תווים

# רישום משתמש חדש
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']

    if not is_valid_username(username):
        return jsonify({'message': 'שם משתמש לא תקין! חייב להיות בין 3 ל-20 תווים ולהכיל רק תווים חוקיים.'}), 400

    if not is_valid_password(password):
        return jsonify({'message': 'סיסמה לא תקינה! חייבת להיות באורך מינימלי של 6 תווים.'}), 400

    if username in users:
        return jsonify({'message': 'המשתמש כבר קיים!'}), 400  # מחזיר הודעת שגיאה

    user_id = len(users) + 1
    users[username] = {
        'id': user_id,
        'password': password,
        'games_played': 0,
        'wins': 0,
        'word_history': []
    }

    save_users()  # שמירת המשתמש החדש בקובץ

    return jsonify({'message': 'ברכתינו, נרשמת בהצלחה!!!'})

# התחברות למערכת
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    if username not in users or users[username]['password'] != password:
        return jsonify({'message': 'שם משתמש או סיסמה לא תקינים!'}), 400

    session['username'] = username
    response = make_response(jsonify({'message': f'שלום {username}! ברוך הבא למשחק.'}))
    response.set_cookie('username', username)
    expiration_time = datetime.utcnow() + timedelta(minutes=10)
    response.set_cookie('session_expiration', expiration_time.strftime('%Y-%m-%d %H:%M:%S'), httponly=True)
    print(f"משתמש {username} נכנס בהצלחה.")

    return response

# פונקציה להארכת זמן הסשן
def check_session_expiration():
    session_expiration = request.cookies.get('session_expiration')
    if not session_expiration:
        return False
    #לוקחת את המחרוזת ואת הפורמט ומזירה אובייקט תאריך ושעה
    expiration_time = datetime.strptime(session_expiration, '%Y-%m-%d %H:%M:%S')
    return datetime.utcnow() < expiration_time #ו בודקת אם הזמן הנוכחי הוא לפני זמן התפוגה שנשמר באובייקט

# פונקציה לקבלת שם המשתמש מתוך העוגיה
def get_user_name_from_cookies():
    username = request.cookies.get('username')
    if not username:
        return None
    return username

# קריאת היסטוריית המשחקים של המשתמש
@app.route('/get_history', methods=['GET'])
def get_history():
    user_name = get_user_name_from_cookies()  # קריאה לעוגיה לקבלת שם המשתמש
    if not user_name:  # אם המשתמש לא מחובר
        return jsonify({'message': 'המשתמש לא מחובר!'}), 400

    user_data = users.get(user_name)
    if not user_data:
        return jsonify({'message': 'נתוני המשתמש לא נמצאו!'}), 400

    # יצירת אובייקט ההיסטוריה
    history_data = {
        'games_played': user_data.get('games_played', 0),
        'wins': user_data.get('wins', 0),
        'word_history': user_data.get('word_history', [])
    }

    return jsonify(history_data), 200

# התחלת משחק חדש
@app.route('/start_game', methods=['POST'])
def start_game():
    if not check_session_expiration():  # בדיקה אם העוגיה פגה
        return jsonify({'message': 'הסשן פג. אנא התחבר שוב.'}), 400

    # הארכת זמן הסשן
    expiration_time = datetime.utcnow() + timedelta(minutes=10)
    response = make_response(jsonify({'message': 'המשחק התחיל.'}))
    response.set_cookie('session_expiration', expiration_time.strftime('%Y-%m-%d %H:%M:%S'), httponly=True)

    data = request.get_json()
    position = data.get('position', 0)

    # בדיקת תקינות שהתקבל מספר
    if not isinstance(position, int):
        return jsonify({'message': 'המיקום חייב להיות מספר שלם!'}), 400

    user_name = get_user_name_from_cookies()
    if not user_name:
        return jsonify({'message': 'המשתמש לא מחובר!'}), 400

    user_data = users.get(user_name)
    if not user_data:
        return jsonify({'message': 'נתוני המשתמש לא נמצאו!'}), 400

    if 'word_history' not in user_data:
        user_data['word_history'] = []

    user_data['games_played'] += 1  # עדכון מספר המשחקים ששחקן שיחק

    # ערבוב המילים
    available_words = [word for word in words if word not in user_data['word_history']]
    random.shuffle(available_words)

      # אם יש מילים זמינות
        # בחירת המילה לפי position
    selected_word_index = position % len(available_words)  # חישוב המיקום המעגלי
    selected_word = available_words[selected_word_index]  # בחר מילה לפי המיקום
    if selected_word not in user_data['word_history']:
        user_data['word_history'].append(selected_word)  # הוספת המילה להיסטוריה

    save_users()  # שמירה במשתמשים
    return jsonify({'selected_word': selected_word})  # מחזיר את המילה שנבחרה


# פונקציה לעדכון מספר הניצחונות של המשתמש
@app.route('/update_victory', methods=['POST'])
def update_victory():
    user_name = get_user_name_from_cookies()  # קריאה לעוגיה לקבלת שם המשתמש
    if not user_name:
        return jsonify({'message': 'המשתמש לא מחובר!'}), 400

    user_data = users.get(user_name)
    if not user_data:
        return jsonify({'message': 'נתוני המשתמש לא נמצאו!'}), 400

    # עדכון מספר הניצחונות
    user_data['wins'] += 1

    save_users()

    return jsonify({'message': 'מספר הניצחונות עודכן בהצלחה!'}), 200

# יציאה מהמערכת
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()  # מנקה את הסשן
    response = make_response(jsonify({'message': 'התנתקת בהצלחה!'}))
    response.delete_cookie('session_expiration')  # מוחק את עוגיית הזמן
    print("המשתמש התנתק בהצלחה.")
    return response

# הפעלת השרת
if __name__ == '__main__':
    app.run(debug=True)
