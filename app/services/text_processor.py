import re
from typing import List, Dict

class IDProcessor:
    def __init__(self):
        # Regex patterns for specific fields
        self.fin_pattern = r"FIN\d{4}-\d{4}-\d{3}-\d{5}"  # Looks for FIN format
        self.phone_pattern = r"\+251\s?\d{3}\s?\d{3}\s?\d{3}" # Looks for +251...
        self.date_pattern = r"\d{4}/[A-Za-z]{3}/\d{2}" # Looks for YYYY/Mmm/DD

    def parse(self, ocr_lines: List[str]) -> Dict[str, str]:
        data = {
            "full_name_amharic": None,
            "full_name_english": None,
            "dob_gc": None,
            "sex": None,
            "expiry_date_gc": None,
            "phone": None,
            "nationality": None,
            "region": None,
            "fin": None
        }

        # Iterate through lines to find context
        for i, line in enumerate(ocr_lines):
            line = line.strip()
            
            # --- Name Extraction ---
            # Usually the name appears right after the Title line
            if "Ethiopian Digital ID Card" in line:
                # The next two lines are usually Amharic Name then English Name
                if i + 1 < len(ocr_lines):
                    data["full_name_amharic"] = ocr_lines[i+1].strip()
                if i + 2 < len(ocr_lines):
                    data["full_name_english"] = ocr_lines[i+2].strip()

            # --- Date of Birth ---
            if "Date of Birtt" in line or "የትውልድ ቀን" in line:
                # The next line usually contains the dates. 
                # Example: "25/01/1995 | 2002/Oct/05"
                if i + 1 < len(ocr_lines):
                    date_line = ocr_lines[i+1]
                    # We want the GC date (usually the second one formatted with Month Text)
                    dates = re.findall(self.date_pattern, date_line)
                    if dates:
                        data["dob_gc"] = dates[0]

            # --- Sex ---
            if "Sex" in line or "Pt" in line: # OCR often reads 'Sex' as 'Pt' or garbled text
                if i + 1 < len(ocr_lines):
                    sex_line = ocr_lines[i+1]
                    if "Male" in sex_line:
                        data["sex"] = "Male"
                    elif "Female" in sex_line:
                        data["sex"] = "Female"

            # --- Expiry Date ---
            if "Date of Expiry" in line:
                if i + 1 < len(ocr_lines):
                    exp_line = ocr_lines[i+1]
                    dates = re.findall(self.date_pattern, exp_line)
                    if dates:
                        data["expiry_date_gc"] = dates[0]

            # --- Phone Number ---
            # Phone can be identified by +251 regex directly
            phone_match = re.search(self.phone_pattern, line)
            if phone_match:
                data["phone"] = phone_match.group(0)

            # --- Nationality ---
            if "Nationality" in line:
                # Usually 2 lines down is the answer
                if i + 2 < len(ocr_lines):
                    if "Ethiopian" in ocr_lines[i+2]:
                        data["nationality"] = "Ethiopian"

            # --- Address (Region) ---
            if "Address" in line:
                # The English region usually appears 2 lines down (Oromia)
                if i + 2 < len(ocr_lines):
                    data["region"] = ocr_lines[i+2].strip()

            # --- FIN Number ---
            # Sometimes the label "FIN" is messed up in OCR, so we regex the whole line
            # The pattern is usually alphanumeric or specific hyphens
            # Based on your input: "sett | FIN1234-1234-314-13411"
            if "FIN" in line:
                # split by 'FIN' and take the rest
                parts = line.split("FIN")
                if len(parts) > 1:
                    # Clean up non-numeric characters except dashes
                    clean_fin = parts[1].replace(",", "").strip() 
                    data["fin"] = clean_fin

        return data