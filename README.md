# Python Flask Web Application - Hangman Game
# אפליקציית ווב בפייתון Flask - משחק תלוי איש

This Python Flask web application provides user registration, login, and a hangman game functionality.
# אפליקציית ווב זו בפייתון Flask מספקת רישום משתמשים, התחברות ופונקציונליות של משחק תלוי איש.

## Features
## תכונות

* **User Authentication:**
* **אימות משתמשים:**
    * User registration with username and password validation.
    * רישום משתמשים עם אימות שם משתמש וסיסמה.
    * User login with session management using cookies.
    * התחברות משתמשים עם ניהול סשן באמצעות עוגיות.
    * Logout functionality.
    * פונקציונליות יציאה.
* **Hangman Game:**
* **משחק תלוי איש:**
    * Retrieves words from a `words.txt` file.
    * שליפת מילים מקובץ `words.txt`.
    * Allows users to start a new game and retrieves a word based on position.
    * מאפשר למשתמשים להתחיל משחק חדש ושולף מילה לפי מיקום.
    * Keeps track of user's game history, wins and played games.
    * עוקב אחר היסטוריית המשחקים, הניצחונות והמשחקים ששוחקו של המשתמש.
    * Displays hangman stages from `hangman_stages.txt`.
    * מציג את שלבי המשחק מקובץ `hangman_stages.txt`.
* **User History:**
* **היסטוריית משתמש:**
    * Retrieves user's game history, wins, and word history.
    * שולף את היסטוריית המשחקים, הניצחונות והמילים של המשתמש.
* **Session Management:**
* **ניהול סשן:**
    * Session expiration and renewal using cookies.
    * פקיעת תוקף סשן וחידוש באמצעות עוגיות.
* **Data Storage:**
* **אחסון נתונים:**
    * User data is stored in a `users.json` file.
    * נתוני משתמש מאוחסנים בקובץ `users.json`.

## Requirements
## דרישות

* Python 3.6+
* Python 3.6+
* Flask
* Flask
* requests
* requests
* json
* json
* datetime
* datetime
* random
* random
* secrets
* secrets
* re
* re
* colorama
* colorama

## Installation
## התקנה

1.  Clone the repository:
1.  שכפל את המאגר:

    ```bash
    git clone <repository_url>
    ```

2.  Navigate to the project directory:
2.  נווט לספריית הפרויקט:

    ```bash
    cd <project_directory>
    ```

3.  Install the required packages:
3.  התקן את החבילות הדרושות:

    ```bash
    pip install Flask requests colorama
    ```

4.  Create a `words.txt` file with words, one word per line.
4.  צור קובץ `words.txt` עם מילים, מילה אחת בכל שורה.
5.  Create a `hangman_stages.txt` file with hangman stages.
5.  צור קובץ `hangman_stages.txt` עם שלבי המשחק.
6.  Run the server application:
6.  הפעל את אפליקציית השרת:

    ```bash
    python app.py
    ```

7.  Run the client application:
7.  הפעל את אפליקציית הלקוח:

    ```bash
    python client.py
    ```

## Usage
## שימוש

* Register a new user by sending a POST request to `/register` with username and password.
* רשום משתמש חדש על ידי שליחת בקשת POST ל-`/register` עם שם משתמש וסיסמה.
* Login by sending a POST request to `/login` with username and password.
* התחבר על ידי שליחת בקשת POST ל-`/login` עם שם משתמש וסיסמה.
* Start a new game by sending a POST request to `/start_game` with position.
* התחל משחק חדש על ידי שליחת בקשת POST ל-`/start_game` עם מיקום.
* Get user history by sending a GET request to `/get_history`.
* קבל את היסטוריית המשתמש על ידי שליחת בקשת GET ל-`/get_history`.
* Update victory count by sending a POST request to `/update_victory`.
* עדכן את ספירת הניצחונות על ידי שליחת בקשת POST ל-`/update_victory`.
* Logout by sending a POST request to `/logout`.
* התנתק על ידי שליחת בקשת POST ל-`/logout`.

## Notes
## הערות

* Ensure that the `users.json`, `words.txt` and `hangman_stages.txt` files are in the same directory as the `app.py` file.
* ודא שהקבצים `users.json`, `words.txt` ו-`hangman_stages.txt` נמצאים באותה ספרייה כמו הקובץ `app.py`.
* The application uses cookies for session management.
* האפליקציה משתמשת בעוגיות לניהול סשן.
* The application includes validation for username and password inputs.
* האפליקציה כוללת אימות עבור קלט שם משתמש וסיסמה.
* The client script will handle the user interaction for the hangman game, including game logic and display.
* סקריפט הלקוח יטפל באינטראקציה עם המשתמש עבור משחק תלוי איש, כולל לוגיקת משחק ותצוגה.
