import re
import spacy

class PIIDetector:
    """
    detects Personally Identifiable Information (PII) 
    using Regular Expressions (Regex) and Natural Language Processing (Spacy).
    """

    def __init__(self, model_name="en_core_web_sm"):
        # Load the Spacy language model
        print(f"Loading Spacy model: {model_name}...")
        try:
            self.nlp = spacy.load(model_name)
        except OSError:
            print(f"Model {model_name} not found. Please run: python -m spacy download {model_name}")
            raise

        # Define Regex patterns for common PII
        # Email pattern: user@domain.com
        self.email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        
        # Phone pattern: 123-456-7890 (standard) or 123-4567-8901 (variations)
        self.phone_pattern = r'\b\d{3}[-.]?\d{3,4}[-.]?\d{4}\b'

        # Indian Context Patterns
        self.pan_pattern = r'[A-Z]{5}[0-9]{4}[A-Z]{1}'
        self.aadhaar_pattern = r'\b\d{4}\s\d{4}\s\d{4}\b'
        self.indian_mobile_pattern = r'(?:\+91[\-\s]?)?[6-9]\d{9}'

    def detect(self, text):
        """
        Scans the text and returns a list of detected PII items.
        Each item is a dictionary with type, value, and method details.
        """
        detected_items = []

        # 1. Regex Detection (Fast & Precise for structured data)
        
        # Find all emails
        emails = re.findall(self.email_pattern, text)
        for email in emails:
            detected_items.append({
                "type": "EMAIL",
                "value": email,
                "method": "REGEX"
            })

        # Find all phone numbers
        phones = re.findall(self.phone_pattern, text)
        for phone in phones:
            detected_items.append({
                "type": "PHONE",
                "value": phone,
                "method": "REGEX"
            })

        # Find PAN Cards
        pans = re.findall(self.pan_pattern, text)
        for pan in pans:
            detected_items.append({
                "type": "PAN_CARD",
                "value": pan,
                "method": "REGEX"
            })

        # Find Aadhaar Cards
        aadhaars = re.findall(self.aadhaar_pattern, text)
        for aadhaar in aadhaars:
            detected_items.append({
                "type": "AADHAAR_CARD",
                "value": aadhaar,
                "method": "REGEX"
            })

        # Find Indian Mobile Numbers
        ind_mobiles = re.findall(self.indian_mobile_pattern, text)
        for mobile in ind_mobiles:
            detected_items.append({
                "type": "INDIAN_MOBILE",
                "value": mobile,
                "method": "REGEX"
            })

        # 2. Spacy NLP Detection (Good for context-based entities like Names)
        
        doc = self.nlp(text)
        
        # List of Spacy entity labels we care about
        # PERSON: People, including fictional
        # ORG: Companies, agencies, institutions
        # GPE: Countries, cities, states (Location)
        target_labels = ["PERSON", "ORG", "GPE"]
        
        for ent in doc.ents:
            if ent.label_ in target_labels:
                detected_items.append({
                    "type": ent.label_, # e.g., PERSON
                    "value": ent.text,
                    "method": "NLP"
                })

        return detected_items
