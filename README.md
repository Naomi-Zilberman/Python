# Python Flask Web Application - Hangman Game

This Python Flask web application provides user registration, login, and a hangman game functionality.

## Features

* **User Authentication:**
    * User registration with username and password validation.
    * User login with session management using cookies.
    * Logout functionality.
* **Hangman Game:**
    * Retrieves words from a `words.txt` file.
    * Allows users to start a new game and retrieves a word based on position.
    * Keeps track of user's game history, wins and played games.
    * Displays hangman stages from `hangman_stages.txt`.
* **User History:**
    * Retrieves user's game history, wins, and word history.
* **Session Management:**
    * Session expiration and renewal using cookies.
* **Data Storage:**
    * User data is stored in a `users.json` file.

## Requirements

* Python 3.6+
* Flask
* requests
* json
* datetime
* random
* secrets
* re
* colorama

## Installation

1.  Clone the repository:

    ```bash
    git clone <repository_url>
    ```

2.  Navigate to the project directory:

    ```bash
    cd <project_directory>
    ```

3.  Install the required packages:

    ```bash
    pip install Flask requests colorama
    ```

4.  Create a `words.txt` file with words, one word per line.
5.  Create a `hangman_stages.txt` file with hangman stages.
6.  Run the server application:

    ```bash
    python app.py
    ```

7.  Run the client application:

    ```bash
    python client.py
    ```

## Usage

* Register a new user by sending a POST request to `/register` with username and password.
* Login by sending a POST request to `/login` with username and password.
* Start a new game by sending a POST request to `/start_game` with position.
* Get user history by sending a GET request to `/get_history`.
* Update victory count by sending a POST request to `/update_victory`.
* Logout by sending a POST request to `/logout`.

## Notes

* Ensure that the `users.json`, `words.txt` and `hangman_stages.txt` files are in the same directory as the `app.py` file.
* The application uses cookies for session management.
* The application includes validation for username and password inputs.
* The client script will handle the user interaction for the hangman game, including game logic and display.

---

# אפליקציית ווב בפייתון Flask - משחק האיש התלוי

אפליקציית ווב זו בפייתון Flask מספקת רישום משתמשים, התחברות ופונקציונליות של משחק האיש התלוי.

## תכונות

* **אימות משתמשים:**
    * רישום משתמשים עם אימות שם משתמש וסיסמה.
    * התחברות משתמשים עם ניהול סשן באמצעות עוגיות.
    * פונקציונליות יציאה.
* **משחק תלוי איש:**
    * שליפת מילים מקובץ `words.txt`.
    * מאפשר למשתמשים להתחיל משחק חדש ושולף מילה לפי מיקום.
    * עוקב אחר היסטוריית המשחקים, הניצחונות והמשחקים ששוחקו של המשתמש.
    * מציג את שלבי המשחק מקובץ `hangman_stages.txt`.
* **היסטוריית משתמש:**
    * שולף את היסטוריית המשחקים, הניצחונות והמילים של המשתמש.
* **ניהול סשן:**
    * פקיעת תוקף סשן וחידוש באמצעות עוגיות.
* **אחסון נתונים:**
    * נתוני משתמש מאוחסנים בקובץ `users.json`.

## דרישות

* Python 3.6+
* Flask
* requests
* json
* datetime
* random
* secrets
* re
* colorama

## התקנה

1.  שכפל את המאגר:

    ```bash
    git clone <repository_url>
    ```

2.  נווט לספריית הפרויקט:

    ```bash
    cd <project_directory>
    ```

3.  התקן את החבילות הדרושות:

    ```bash
    pip install Flask requests colorama
    ```

4.  צור קובץ `words.txt` עם מילים, מילה אחת בכל שורה.
5.  צור קובץ `hangman_stages.txt` עם שלבי המשחק.
6.  הפעל את אפליקציית השרת:

    ```bash
    python app.py
    ```

7.  הפעל את אפליקציית הלקוח:

    ```bash
    python client.py
    ```

## שימוש

* רשום משתמש חדש על ידי שליחת בקשת POST ל-`/register` עם שם משתמש וסיסמה.
* התחבר על ידי שליחת בקשת POST ל-`/login` עם שם משתמש וסיסמה.
* התחל משחק חדש על ידי שליחת בקשת POST ל-`/start_game` עם מיקום.
* קבל את היסטוריית המשתמש על ידי שליחת בקשת GET ל-`/get_history`.
* עדכן את ספירת הניצחונות על ידי שליחת בקשת POST ל-`/update_victory`.
* התנתק על ידי שליחת בקשת POST ל-`/logout`.

## הערות

* ודא שהקבצים `users.json`, `words.txt` ו-`hangman_stages.txt` נמצאים באותה ספרייה כמו הקובץ `app.py`.
* האפליקציה משתמשת בעוגיות לניהול סשן.
* האפליקציה כוללת אימות עבור קלט שם משתמש וסיסמה.
* סקריפט הלקוח יטפל באינטראקציה עם המשתמש עבור משחק תלוי איש, כולל לוגיקת משחק ותצוגה.
