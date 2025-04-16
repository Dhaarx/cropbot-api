from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from google.genai import types # type: ignore
import os

app = Flask(__name__)
CORS(app)

client = genai.Client(api_key='AIzaSyAHq2x31inehTL4HRk4L280WWpMyhmFFbw')

crop_system_prompt = """
You are AgriBot, a helpful AI assistant that answers only agriculture-related questions. Your primary tasks include:
- Crop disease prediction and prevention
- Fertilizer recommendation
- Soil and climate suitability
- Plant health and yield optimization

⚠️ If the user asks anything unrelated to agriculture (e.g., technology, history, sports, general knowledge , livestock), respond strictly with:
"I'm sorry, I can only help with agriculture-related queries."

Stick to agriculture topics only. Be informative, polite, and focused.
You are an agriculture expert bot. Summarize any given plant-related explanation into 5-8 points.
"""

livestock_system_prompt = """
You are LivestockBot, a helpful AI assistant that answers only livestock-related questions. Your primary tasks include:
- Animal health and disease management
- Feed and nutrition guidance
- Breeding practices and reproduction
- Shelter and hygiene maintenance
- Livestock productivity improvement
- Common issues in cattle, poultry, goats, sheep, and pigs

⚠️ If the user asks anything unrelated to livestock (e.g., crops, technology, history, general knowledge,sports), respond strictly with:
"I'm sorry, I can only help with livestock-related queries."

Stick to livestock topics only. Be informative, polite, and focused.
You are an animal husbandry expert bot. Summarize any given livestock-related explanation into 5-8 points.
"""


@app.route('/')
def home():
    return "Welcome to AgriBot API!"

@app.route('/favicon.ico')
def favicon():
    return '', 204

def crop_query_gemini(user_input):
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=user_input,
        config=types.GenerateContentConfig(
            system_instruction=crop_system_prompt,
            max_output_tokens=1000,
            temperature=0.5,
            top_k=2,
            top_p=0.5,
            seed=42,
            tools=[types.Tool(google_search=types.GoogleSearch())]
        )
    )
    return response.text

def livestock_query_gemini(user_input):
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=user_input,
        config=types.GenerateContentConfig(
            system_instruction=livestock_system_prompt,
            max_output_tokens=1000,
            temperature=0.5,
            top_k=2,
            top_p=0.5,
            seed=42,
            tools=[types.Tool(google_search=types.GoogleSearch())]
        )
    )
    return response.text
 
@app.route('/crops', methods=['POST'])
def crops_query():
    data = request.get_json()
    user_input = data.get('message','')
    if not user_input:
        return jsonify({'error': 'Empty input'}), 400
    answer = crop_query_gemini(user_input)
    return jsonify({'response': answer})

@app.route('/livestock', methods=['POST'])
def livestock_query():
    data = request.get_json()
    user_input = data.get('message','')
    if not user_input:
        return jsonify({'error': 'Empty input'}), 400
    answer = livestock_query_gemini(user_input)
    return jsonify({'response': answer})


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
