import os 
import google.generativeai as genai
from dotenv import load_dotenv
import json
import logging

logger = logging.getLogger(__name__)

load_dotenv()

class VisionGeminiClient:
    def __init__(self):
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is required but not set")
        
        genai.configure(api_key=api_key)
        
        model_name = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')
        # Only include vision-capable models; gemini-1.0-pro lacks vision support
        valid_models = ['gemini-1.5-flash', 'gemini-2.0-flash', 'gemini-1.5-pro']
        if model_name not in valid_models:
            raise ValueError(f"Invalid GEMINI_MODEL '{model_name}'. Must be one of: {', '.join(valid_models)}")
        
        self.model = genai.GenerativeModel(model_name)
        
        # Runtime check to ensure model supports vision capabilities
        try:
            model_info = genai.get_model(model_name)
            if 'vision' not in str(model_info.supported_generation_methods):
                logger.warning(f"Model {model_name} may not support vision capabilities. Image processing may fail.")
        except Exception as check_error:
            logger.warning(f"Could not verify vision capability for model {model_name}: {check_error}")  

    def extract_expense_details(self, image_path):
        #using a system prompt to guide the model to extract desire details and force json format
        system_prompt = """
        Analyse the provided image and extract the following details in JSON format:
            {
                "vendor": "Name of the vendor",
                "receipt_number": "Receipt number if available",
                "receiver": {
                    "account_title": "Name of the person who made the purchase",
                    "account_number": "Account number of the person who made the purchase"
                },
                "date": "Date of the transaction in YYYY-MM-DD format",
                "total_amount": "Total amount spent",
                "category": "Category of the expense (e.g., Food, Travel, etc.)",
                "currency": "Currency of the transaction (e.g., USD, EUR, etc.)",
                "items": [
                    {
                        "name": "Name of the item",
                        "quantity": "Quantity purchased",
                        "price": "Price per unit"
                    }
                ]
            }
            Return only JSON format, if any field is missing, return null
        """

        #loading the img 
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        sample_image = genai.upload_file(image_path)
        response = self.model.generate_content([system_prompt, sample_image])
        #cleaning the response
        json_text = response.text.replace("```json", "").replace("```", "").strip()
        try:
            return json.loads(json_text)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse model response as JSON: {e}")
    
if __name__ == "__main__":
    client = VisionGeminiClient()
    details = client.extract_expense_details(r'F:\AI-Automation\data_files\test_img.jpeg')
    print(details)  