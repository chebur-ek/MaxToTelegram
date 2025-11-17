from flask import Flask, request, Response
import json
import requests
from datetime import datetime
import io

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = "7375275750:AAGSzNQ4rPkKD1jb1HoOVi2g5pCiDvj_6EY"
TELEGRAM_CHAT_ID = "-1002292466397"

def parse_webhook(data):
    """Парсит данные от Green API"""
    try:
        sender_data = data.get("senderData", {})
        message_data = data.get("messageData", {})
        
        sender_name = sender_data.get("senderName", "Unknown")
        message_type = message_data.get("typeMessage")
        chat_name = sender_data.get("chatName", "Unknown")
        
        result = {
            "SenderName": sender_name,
            "ChatName": chat_name,
            "MessageType": message_type
        }
        
        # Для текста
        if message_type == "textMessage":
            result["textMessage"] = message_data.get("textMessageData", {}).get("textMessage")
        
        # Для картинок, видео, документов
        elif message_type in ["imageMessage", "videoMessage", "documentMessage", "audioMessage"]:
            file_data = message_data.get("fileMessageData", {})
            result["downloadUrl"] = file_data.get("downloadUrl")
            result["caption"] = file_data.get("caption", "")
            result["mimeType"] = file_data.get("mimeType", "")
        
        return result
    except Exception as e:
        print(f"Ошибка парсера: {e}")
        return None

def send_photo_to_telegram(sender_name, chat_name, download_url, caption=""):
    """Скачивает и отправляет фото в Telegram"""
    try:
        print(f"📥 Скачиваю картинку с {download_url[:50]}...")
        
        # Скачиваем картинку
        photo_response = requests.get(download_url, timeout=30)
        
        if photo_response.status_code != 200:
            print(f"❌ Ошибка при скачивании: {photo_response.status_code}")
            return
        
        # Подготавливаем данные для отправки
        photo_bytes = io.BytesIO(photo_response.content)
        photo_bytes.name = "photo.jpg"
        
        # Форматируем подпись
        photo_caption = f"<b>Группа:</b> {chat_name}\n<b>От:</b> {sender_name}"
        if caption:
            photo_caption += f"\n<b>Описание:</b> {caption}"
        
        # Отправляем фото в Telegram
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
        
        files = {'photo': photo_bytes}
        data = {
            'chat_id': TELEGRAM_CHAT_ID,
            'caption': photo_caption,
            'parse_mode': 'HTML'
        }
        
        response = requests.post(url, files=files, data=data, timeout=30)
        
        if response.status_code == 200:
            print(f"✅ Фото отправлено в Telegram")
        else:
            print(f"❌ Ошибка Telegram: {response.text}")
    
    except Exception as e:
        print(f"❌ Ошибка при отправке фото: {e}")

def send_video_to_telegram(sender_name, chat_name, download_url, caption=""):
    """Скачивает и отправляет видео в Telegram"""
    try:
        print(f"📥 Скачиваю видео с {download_url[:50]}...")
        
        # Скачиваем видео
        video_response = requests.get(download_url, timeout=60)
        
        if video_response.status_code != 200:
            print(f"❌ Ошибка при скачивании видео: {video_response.status_code}")
            return
        
        video_bytes = io.BytesIO(video_response.content)
        video_bytes.name = "video.mp4"
        
        # Форматируем подпись
        video_caption = f"<b>Группа:</b> {chat_name}\n<b>От:</b> {sender_name}"
        if caption:
            video_caption += f"\n<b>Описание:</b> {caption}"
        
        # Отправляем видео в Telegram
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendVideo"
        
        files = {'video': video_bytes}
        data = {
            'chat_id': TELEGRAM_CHAT_ID,
            'caption': video_caption,
            'parse_mode': 'HTML'
        }
        
        response = requests.post(url, files=files, data=data, timeout=60)
        
        if response.status_code == 200:
           print(f"✅ Видео отправлено в Telegram")
        else:
            print(f"❌ Ошибка Telegram: {response.text}")
    
    except Exception as e:
        print(f"❌ Ошибка при отправке видео: {e}")

def send_document_to_telegram(sender_name, chat_name, download_url, caption=""):
    """Скачивает и отправляет документ в Telegram"""
    try:
        print(f"📥 Скачиваю документ с {download_url[:50]}...")
        
        doc_response = requests.get(download_url, timeout=60)
        
        if doc_response.status_code != 200:
            print(f"❌ Ошибка при скачивании документа: {doc_response.status_code}")
            return
        
        doc_bytes = io.BytesIO(doc_response.content)
        doc_bytes.name = "document"
        
        doc_caption = f"<b>Группа:</b> {chat_name}\n<b>От:</b> {sender_name}"
        if caption:
            doc_caption += f"\n<b>Файл:</b> {caption}"
        
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
        
        files = {'document': doc_bytes}
        data = {
            'chat_id': TELEGRAM_CHAT_ID,
            'caption': doc_caption,
            'parse_mode': 'HTML'
        }
        
        response = requests.post(url, files=files, data=data, timeout=60)
        
        if response.status_code == 200:
            print(f"✅ Документ отправлен в Telegram")
        else:
            print(f"❌ Ошибка Telegram: {response.text}")
    
    except Exception as e:
        print(f"❌ Ошибка при отправке документа: {e}")

def send_text_to_telegram(sender_name, chat_name, text_message):
    """Отправляет текст в Telegram"""
    try:
        message = f"<b>Группа:</b> {chat_name}\n<b>От:</b> {sender_name}\n\n{text_message}"
        
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        
        response = requests.post(url, json=data, timeout=10)
        
        if response.status_code == 200:
            print(f"✅ Текст отправлен в Telegram")
        else:
            print(f"❌ Ошибка Telegram: {response.text}")
    
    except Exception as e:
        print(f"❌ Ошибка при отправке текста: {e}")

@app.route('/', methods=['POST'])
def webhook_handler():
    try:
        data = request.json
        
        print("\n" + "="*60)
        print(f"📩 ПОЛУЧЕНО ОТ GREEN API [{datetime.now().strftime('%H:%M:%S')}]")
        print("="*60)
        
        # ПАРСИМ ДАННЫЕ
        parsed = parse_webhook(data)
        
        if parsed:
            sender_name = parsed.get("SenderName", "Unknown")
            chat_name = parsed.get("ChatName", "Unknown")
            message_type = parsed.get("MessageType")
            
            print(f"✅ Распарсено:")
            print(f"   От: {sender_name}")
            print(f"   Группа: {chat_name}")
            print(f"   Тип: {message_type}\n")
            
            # Обработка разных типов сообщений
            if message_type == "textMessage":
                text = parsed.get("textMessage")
                print(f"   Текст: {text}")
                send_text_to_telegram(sender_name, chat_name, text)
            
            elif message_type == "imageMessage":
                url = parsed.get("downloadUrl")
                caption = parsed.get("caption", "")
                print(f"   Картинка: {url}")
                send_photo_to_telegram(sender_name, chat_name, url, caption)
            
            elif message_type == "videoMessage":
                url = parsed.get("downloadUrl")
                caption = parsed.get("caption", "")
                print(f"   Видео: {url}")
                send_video_to_telegram(sender_name, chat_name, url, caption)
            
            elif message_type == "documentMessage":
                url = parsed.get("downloadUrl")
                caption = parsed.get("caption", "")
                print(f"   Документ: {url}")
                send_document_to_telegram(sender_name, chat_name, url, caption) 
            else:
                print(f"   Неизвестный тип: {message_type}")
    
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
    
    print("="*60 + "\n")
    return Response(status=200)

if __name__ == '__main__':
    print("🚀 Вебхук сервер запущен")
    print("📱 Картинки скачиваются и отправляются в Telegram")
    app.run(host='0.0.0.0', port=5000, debug=False)