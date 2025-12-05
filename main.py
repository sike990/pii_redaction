import sys
import os

# Add the current directory to path so we can import src modules easily
sys.path.append(os.getcwd())

from src.detector import PIIDetector
from src.redactor import Redactor
from src.classifier import Classifier

def main():
    # 1. Setup - Get input file
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_text_file>")
        print("Example: python main.py data/sample.txt")
        return

    input_file_path = sys.argv[1]
    
    if not os.path.exists(input_file_path):
        print(f"Error: File '{input_file_path}' not found.")
        return

    # 2. Read the file
    print(f"--- Processing: {input_file_path} ---")
    try:
        with open(input_file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # 3. Initialize Components
    detector = PIIDetector()
    classifier = Classifier()
    redactor = Redactor()

    # 4. Detect PII
    print("Scanning for PII...")
    detected_items = detector.detect(text)
    
    print(f"\nFound {len(detected_items)} potential PII items.")
    for item in detected_items:
        print(f" - [{item['type']}] {item['value']} (via {item['method']})")

    # 5. Classify Sensitivity
    sensitivity = classifier.classify(detected_items)
    print(f"\nDocument Sensitivity Level: {sensitivity}")

    # 6. Redact PII
    redacted_text = redactor.redact(text, detected_items)
    
    # 7. Output Results
    print("\n--- Redacted Text Preview ---")
    print(redacted_text)
    print("-----------------------------")

    # Save redacted file
    output_path = input_file_path + ".redacted.txt"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(redacted_text)
    
    print(f"\nRedacted file saved to: {output_path}")

if __name__ == "__main__":
    main()
