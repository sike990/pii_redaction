class Classifier:
    """
    Determines the sensitivity level of a document based on the PII found.
    """

    def classify(self, detected_items):
        """
        Returns 'High', 'Medium', or 'Low' sensitivity based on rules.
        """
        if not detected_items:
            return "Clean (No PII Detected)"

        # Extract all types found
        detected_types = {item['type'] for item in detected_items}

        # Rule 1: High Sensitivity if direct contact info is found
        if any(t in detected_types for t in ["EMAIL", "PHONE", "INDIAN_MOBILE", "PAN_CARD", "AADHAAR_CARD"]):
            return "High Sensitivity"

        # Rule 2: Medium Sensitivity if names or locations are found
        if "PERSON" in detected_types or "GPE" in detected_types:
            return "Medium Sensitivity"

        # Default for other types (like ORG)
        return "Low Sensitivity"
