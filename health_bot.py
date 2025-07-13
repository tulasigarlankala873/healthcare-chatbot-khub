from flask import Flask, request, jsonify, render_template
from google.cloud import dialogflow_v2 as dialogflow
from google.cloud.dialogflow_v2 import types
from google.oauth2 import service_account
import os

app = Flask(__name__)

# Configure path to service account key
SERVICE_ACCOUNT_FILE = 'service-account-key.json'
PROJECT_ID = 'healthcare-chatbot-465314'

# Authenticate with Dialogflow
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
session_client = dialogflow.SessionsClient(credentials=credentials)

# Route to load the chatbot HTML UI
@app.route('/')
def index():
    return render_template('index.html')  # Make sure this file is in the "templates" folder

# Route to handle chat messages
@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get("message")
        session = session_client.session_path(PROJECT_ID, 'unique-session-id')

        text_input = types.TextInput(text=user_message, language_code='en')
        query_input = types.QueryInput(text=text_input)

        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )

        bot_reply = response.query_result.fulfillment_text or "I'm not sure how to respond to that."
        return jsonify({"reply": bot_reply})
    except Exception as e:
        return jsonify({"reply": f"⚠️ Internal error: {str(e)}"}), 500

if __name__ == '__main__':
    # Ensure Flask reloads templates properly
    app.run(debug=True)
