from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.ocr_engine import read_image_stream
from app.services.text_processor import IDProcessor
from app.services.image_utils import check_image_quality
from PIL import Image
import io

router = APIRouter()
processor = IDProcessor()


@router.post("/extract-id")
async def extract_id_data(file: UploadFile = File(...)):
    """
    Endpoint to receive an image stream and return OCR text.
    """
    # Validate file type
    if file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload JPEG or PNG.")

    try:
        # Read the stream
        file_content = await file.read()
        
        # Process OCR
        extracted_text = read_image_stream(file_content)
        
        return {
            "filename": file.filename,
            "content_type": file.content_type,
            "data": extracted_text
        }

    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred during processing.")


@router.post("/check-blur")
async def validate_image(file: UploadFile = File(...)):
    """
    Checks if the uploaded image is sharp enough for OCR.
    Returns 200 OK if clear, or an error message if blurry.
    """
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid format")

    content = await file.read()
    image = Image.open(io.BytesIO(content))
    
    quality = check_image_quality(image)
    
    if not quality["is_clear"]:
        return {
            "status": "not ready",
            "message": "Image is blurry. Please retake.",
            "score": quality["score"]
        }
    
    return {
        "status": "ready", 
        "message": "Image quality is optimal for extraction.",
        "score": quality["score"]
    }