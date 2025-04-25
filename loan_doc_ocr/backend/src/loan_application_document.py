import re
from parser_generic import DocParser

class PrescriptionParser(DocParser):
    def __init__(self, text):
        super().__init__(text)

    def parse(self):
        return {
            "name": self.get_field("name"),
            "address": self.get_field("address"),
            "income_details": self.get_field("income_details"),
            "loan_amount": self.get_field("loan_amount")
        }

    def get_field(self, field_name):
        pattern_dict = {
            "name": {"pattern": r"Name:(.*)Date", "flags": 0},
            "address": {"pattern": r"Address:(.*)\n", "flags": 0},
            "income_details": {"pattern": r"Address:[^\n]*(.*)Directions", "flags": re.DOTALL},
            "loan_amount": {"pattern": r"Directions:.(.*)Refill", "flags": re.DOTALL},
        }

        pattern_object = pattern_dict.get(field_name)
        if pattern_object:
            matches = re.findall(pattern_object["pattern"], self.text, flags=pattern_object["flags"])
            return matches[0].strip() if matches else ""
        return ""
