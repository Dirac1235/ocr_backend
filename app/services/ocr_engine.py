import pytesseract
from PIL import Image
import io
from app.services.text_processor import IDProcessor

# NOTE: If you are on Windows, you might need to point to the executable:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

processor = IDProcessor()

def read_image_stream(file_bytes: bytes) -> Dict[str, str]:
    """
    Helper function to process image bytes and return text.
    """
    try:
        # 1. Load the image from the byte stream
        image = Image.open(io.BytesIO(file_bytes))

        # 2. Preprocessing (Optional but recommended for IDs)
        # Convert to grayscale to improve Tesseract accuracy
        image = image.convert('L') 
        
        # 3. Perform OCR
        # lang='eng' can be changed or extended (e.g. 'eng+spa')
        text = pytesseract.image_to_string(image, lang='eng+amh')
        extracted_text = [txt for txt in text.strip().split("\n") if txt]
        pasrsed_data = processor.parse(extracted_text)
    
        return pasrsed_data

    except Exception as e:
        raise ValueError(f"Error processing image: {str(e)}")