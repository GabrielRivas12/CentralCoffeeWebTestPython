from dotenv import get_key
from flask import Blueprint, flash, jsonify, render_template, redirect, request, url_for, session
import requests

assistant_bp = Blueprint('assistant', __name__)

api_key = get_key(".env", "API_KEY")
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

@assistant_bp.route('/chatbox')
def chatbox():
    return render_template('screens/Chatbox/chatbox.html')

@assistant_bp.route('/ask_gemini', methods=['POST'])
def ask_gemini():
    user_text = request.json.get("text", "")  
    if not user_text:
        return jsonify({"error": "Texto vacío"}), 400

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": user_text}
                ]
            }
        ]
    }

    try:
        response = requests.post(API_URL, json=payload)
        
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": f"Error de API: {response.status_code}"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@assistant_bp.route('/rci')
def rci():
    return render_template('screens/RCI/rci.html')