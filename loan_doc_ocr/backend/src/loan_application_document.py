import re
from parser_generic import MedicalDocParser
class PrescriptionParser(MedicalDocParser):
    def __init__(self, text):
        MedicalDocParser.__init__(self, text)
    def parse(self):
        return{
            "name": self.get_field("name"),
            "address": self.get_field("address"),
            "income_details": self.get_field("income_details"),
            "loan_amount": self.get_field("loan_amount")
        }        
    def get_field(self, field_name):
        pattern_dict = {
            "name": {"pattern": "Name:(.*)Date", "flags": 0},
            "address": {"pattern": "Address:(.*)\n", "flags": 0},
            "income_details": {"pattern": "Address:[^\n]*(.*)Directions", "flags": re.DOTALL},
            "loan_amount": {"pattern": "Directions:.(.*)Refill", "flags": re.DOTALL},
        }
        pattern_object = pattern_dict.get(field_name)
        if pattern_object:
            matches = re.findall(pattern_object["pattern"], self.text, flags=pattern_object["flags"])
            if len(matches) > 0:
                return matches[0].strip()

if __name__ == "__main__":
    document_text = """
Dr John Smith, M.D
2 Non-Important Street,
New York, Phone (000)-111-2222

Name: Marta Sharapova Date: 5/11/2022

Address: 9 tennis court, new Russia, DC

Prednisone 20 md
Lialda 2.4 gram

Directions:

Prednisone, Taper 5 mg every 3 days,
Finish in 2.5 weeks 7
Lialda - take 2 pill everyday for 1 month

Refill: _2_times"""

    pp = PrescriptionParser(document_text)
    print(pp.parse())
