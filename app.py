import os
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)
BOT_TOKEN = os.environ.get("BOT_TOKEN")

@app.route("/send_ticket", methods=["POST"])
def send_ticket():
    try:
        data = request.json
        chat_id = data.get("chat_id")
        text = data.get("text")
        pieteikums_id = data.get("pieteikums_id")
        action = data.get("action")

        keyboard = None
        
        # Логика кнопок спрятана в облаке!
        # Button logic hidden in the cloud
        if action == "START_AND_FINISH":
            keyboard = {
                "inline_keyboard": [
                    [{"text": "Sakt izpildi!", "callback_data": f"PROCESA|{pieteikums_id}"}],
                    [{"text": "Darbs pabeigts", "callback_data": f"PABEIGTS|{pieteikums_id}"}]
                ]
            }
        elif action == "START_ONLY":
            keyboard = {
                "inline_keyboard": [
                    [{"text": "Sakt izpildi!", "callback_data": f"PROCESA|{pieteikums_id}"}]
                ]
            }
        elif action == "FINISH":
            keyboard = {
                "inline_keyboard": [
                    [{"text": "Darbs pabeigts", "callback_data": f"PABEIGTS|{pieteikums_id}"}]
                ]
            }
        # Если action == "CLOSE", keyboard остается None (сообщение без кнопок)

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
        
        if keyboard:
            payload["reply_markup"] = keyboard

        response = requests.post(url, json=payload)
        return jsonify(response.json()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
