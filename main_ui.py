from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os
import markdown2
from sys_prompt import system_prompt

system_prompt=system_prompt

# Initialize the OpenAI client
dotenv_path = os.path.join(os.path.dirname(__file__), 'keys.env')
load_dotenv(dotenv_path)
open_ai_key = os.getenv('OPENAI_API_KEY') 
client = OpenAI(api_key=open_ai_key)

app = Flask(__name__)

def get_description_analysis(content, system_prompt):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": content}
    ]

    # Call the chat completions endpoint
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    # Return the response message
    return completion.choices[0].message.content

from flask import Flask, request, jsonify, render_template


app = Flask(__name__)

@app.route('/')
def index():
    # Serve the index.html file
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_job():
    data = request.json
    content = data.get('content')
    system_prompt = data.get('system_prompt')

    if not content or not system_prompt:
        return jsonify({"error": "Content and system prompt are required."}), 400

    # Generate analysis
    analysis = get_description_analysis(content, system_prompt)

    # Convert Markdown to HTML
    markdown_html = markdown2.markdown(analysis)
    return jsonify({"analysis": markdown_html})

if __name__ == '__main__':
    app.run(debug=True)

