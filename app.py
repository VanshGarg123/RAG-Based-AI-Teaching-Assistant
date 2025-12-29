from flask import Flask, render_template, request, jsonify
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import requests
import joblib
import os

app = Flask(__name__)

# Load the dataframe from the joblib file
df = joblib.load("models/embeddings.joblib")

HF_TOKEN = os.getenv("HF_TOKEN")
EMBEDDING_MODEL = "bge-m3"
LLM_MODEL = "meta-llama/Llama-3.2-3B-Instruct"

def create_embedding(text_list):
    try:
        headers = {
            "Authorization": f"Bearer {HF_TOKEN}",
            "Content-Type": "application/json"
        }

        r = requests.post(
            "https://router.huggingface.co/hf-inference/models/BAAI/bge-large-en-v1.5/pipeline/feature-extraction",
            headers=headers,
            json={
                "inputs": text_list[0] if len(text_list) == 1 else text_list
            },
            timeout=60
        )
        result = r.json()
        
        # Check for errors
        if isinstance(result, dict) and "error" in result:
            print(f"Embedding API Error: {result['error']}")
            return None
        
        # If single input (string), result is a single embedding list
        # If multiple inputs (list), result is list of embeddings
        if isinstance(result, list):
            # Check if it's a single embedding or list of embeddings
            if len(text_list) == 1 and isinstance(result[0], (int, float)):
                # Single embedding returned as flat list
                return [result]
            else:
                # Multiple embeddings or already in correct format
                return result
        
        return None

    except Exception as e:
        print(f"Embedding error: {e}")
        return None

def inference(prompt):
    try:
        headers = {
            "Authorization": f"Bearer {HF_TOKEN}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": LLM_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 400,
            "temperature": 0.4,
            "top_p": 0.9
        }

        r = requests.post(
            "https://router.huggingface.co/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=120
        )
        result = r.json()
        
        # Check for errors
        if "error" in result:
            print(f"LLM API Error: {result['error']}")
            return None
        
        # Extract the response using the new format
        if "choices" in result and len(result["choices"]) > 0:
            return {
                "response": result["choices"][0]["message"]["content"]
            }
        else:
            print(f"Unexpected response format: {result}")
            return None

    except Exception as e:
        print(f"LLM error: {e}")
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    try:
        data = request.get_json()
        incoming_query = data.get('question', '')
        
        if not incoming_query:
            return jsonify({'error': 'No question provided'}), 400
        
        # Create embedding for the question
        question_embedding = create_embedding([incoming_query])
        if question_embedding is None:
            return jsonify({'error': 'Failed to create embedding'}), 500
        
        question_embedding = question_embedding[0]
        
        # Calculate similarities
        similarities = cosine_similarity(
            np.vstack(df['embedding'].values), 
            [question_embedding]
        ).flatten()
        
        # Get top 5 results
        top_results = 5
        max_idx = similarities.argsort()[::-1][0:top_results]
        new_df = df.loc[max_idx]
        
        # Create prompt
        prompt = f'''I am teaching web development in my Sigma web development course. Here are video subtitle chunks containing video title, video number, start time in seconds, end time in seconds, the text at that time:

        {new_df[["title", "number", "start", "end", "text"]].to_json(orient="records")}
        ---------------------------------
        "{incoming_query}"
        User asked this question related to the video chunks, you have to answer in a human way (dont mention the above format, its just for you) where and how much content is taught in which video (in which video and at what timestamp) and guide the user to go to that particular video. If user asks unrelated question, tell him that you can only answer questions related to the course
        '''
        
        # Get response from LLM
        llm_response = inference(prompt)
        if llm_response is None:
            return jsonify({'error': 'Failed to get response from LLM'}), 500
        
        response_text = llm_response.get("response", "")
        
        return jsonify({
            'success': True,
            'response': response_text
        })
        
    except Exception as e:
        print(f"Error processing question: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)