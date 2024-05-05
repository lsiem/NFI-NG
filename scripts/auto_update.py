import subprocess
import requests
import os


def check_for_updates():
    subprocess.run(['git', 'fetch'], cwd='../user_data/strategies')
    status = subprocess.run(['git', 'status', '-uno'], cwd='../user_data/strategies', capture_output=True, text=True)
    if 'Your branch is behind' in status.stdout:
        return True
    return False


def update_strategy():
    subprocess.run(['git', 'pull'], cwd='../user_data/strategies')


def send_telegram_notification():
    message = "Crypto Bot strategy has been updated to the latest version."
    url = f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN')}/sendMessage"
    data = {
        'chat_id': os.getenv('TELEGRAM_CHAT_ID'),
        'text': message,
        'parse_mode': 'Markdown'
    }
    response = requests.post(url, data=data)
    print("Notification sent:", response.status_code)


if __name__ == '__main__':
    if check_for_updates():
        update_strategy()
        send_telegram_notification()
