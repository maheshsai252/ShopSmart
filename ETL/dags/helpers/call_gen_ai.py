import google.generativeai as genai
import os

genai.configure(api_key=os.getenv('gemini_key'))

def call_gemini_api(input_text):
    model = genai.GenerativeModel('models/gemini-1.0-pro')
    response = model.generate_content(input_text.strip(), safety_settings={'HARASSMENT':'block_none',
                                                     'HATE_SPEECH': 'block_none',
                                                     'HARM_CATEGORY_DANGEROUS_CONTENT': 'block_none',
                                                     'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'block_none'})
    try:
        print(response)
        print(response.text)
        return response.text
    except Exception as e:
        print(e)
        return "UNSAFE"