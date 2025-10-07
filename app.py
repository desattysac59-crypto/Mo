from flask import Flask, request, jsonify
import base64
import json
import datetime
import os
import requests

app = Flask(__name__)

# Настройки Telegram бота
TELEGRAM_BOT_TOKEN = "8039861900:AAF2T_ZLgxgGzBkiDQM08wSZ7uxVo8w7bnI"
TELEGRAM_CHAT_ID = "7537584350"

def send_telegram_alert(visitor_data):
    """Отправка уведомления в Telegram"""
    try:
        message = f"""
🔍 НОВОЕ ОТКРЫТИЕ PDF
🕐 Время: {visitor_data.get('time', 'N/A')}
🌐 IP: {visitor_data.get('ip', 'N/A')}
💻 Платформа: {visitor_data.get('platform', 'N/A')}
🔍 User Agent: {visitor_data.get('userAgent', 'N/A')}
        """
        
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message
        }
        
        requests.post(url, json=data, timeout=10)
    except Exception as e:
        print(f"Telegram error: {e}")

@app.route('/track', methods=['GET', 'POST'])
def track_visitor():
    """Основной endpoint для отслеживания"""
    try:
        if request.method == 'GET':
            encoded_data = request.args.get('data', '')
        else:
            encoded_data = request.form.get('info', '')
        
        if encoded_data:
            # Декодируем данные
            decoded_data = base64.b64decode(encoded_data).decode('utf-8')
            visitor_info = json.loads(decoded_data)
            
            # Логируем в консоль
            print("=" * 50)
            print(f"НОВЫЙ ПОСЕТИТЕЛЬ PDF:")
            for key, value in visitor_info.items():
                print(f"{key}: {value}")
            print("=" * 50)
            
            # Отправляем в Telegram
            send_telegram_alert(visitor_info)
            
    except Exception as e:
        print(f"Tracking error: {e}")
    
    # Возвращаем пустой ответ
    return '', 200

@app.route('/')
def home():
    return 'PDF Tracker Active'

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
