import json
import os
from dotenv import load_dotenv

load_dotenv()

def load_config(file_path):
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config

def get_azure_openai_api_key():
    return os.getenv('AZURE_OPENAI_API_KEY')

def get_openai_base_url():
    config = load_config('model_gpt-4o-mini.json')
    return config['base_url']

def get_openai_model():
    config = load_config('model_gpt-4o-mini.json')
    return config['model']

def get_openai_api_version():
    config = load_config('model_gpt-4o-mini.json')
    return config['api_version']

def get_gemma2_base_url():
    config = load_config('model_gemma2.json')
    return config['base_url']

def get_gemma2_model():
    config = load_config('model_gemma2.json')
    return config['model']

def get_gemma2_api_type():
    config = load_config('model_gemma2.json') 
    return config['api_type']