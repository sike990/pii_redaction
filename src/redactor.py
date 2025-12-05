class Redactor:
    """
    Handles the masking/redaction of sensitive information in text.
    """

    def redact(self, text, detected_items):
        """
        Replaces detected PII values in the text with a [REDACTED] placeholder.
        """
        redacted_text = text
        
        # We process unique values to avoid redundant replacements
        # We sort by length (descending) to ensure we replace longer matches first
        # Example: Replace "Jonathan Smith" before "Jonathan" to avoid partial masking errors.
        unique_values = set(item['value'] for item in detected_items)
        sorted_values = sorted(unique_values, key=len, reverse=True)

        for value in sorted_values:
            # Simple string replacement
            # format: [TYPE] is also an option, but we'll use a standard [REDACTED]
            redacted_text = redacted_text.replace(value, "[REDACTED]")
            
        return redacted_text
