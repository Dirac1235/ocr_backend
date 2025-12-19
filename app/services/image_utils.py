import cv2
import numpy as np
from PIL import Image

def check_image_quality(image: Image.Image, threshold: float = 110.0) -> dict:
    """
    Checks if an image is too blurry for OCR.
    
    Args:
        image (PIL.Image): The loaded image object.
        threshold (float): The score below which an image is considered blurry. 
                           100-120 is standard for text documents.
    Returns:
        dict: Contains 'is_clear' (bool) and 'score' (float).
    """
    try:
        # 1. Convert PIL Image to OpenCV format (numpy array)
        # Note: PIL images are RGB, OpenCV uses BGR, but for grayscale it doesn't matter much.
        # We explicitly convert to grayscale first.
        open_cv_image = np.array(image.convert('L'))

        # 2. Calculate Variance of the Laplacian
        # This gives a score. High score = Sharp. Low score = Blurry.
        blur_score = cv2.Laplacian(open_cv_image, cv2.CV_64F).var()

        # 3. Determine if it passes
        is_clear = blur_score > threshold

        return {
            "is_clear": is_clear,
            "score": round(blur_score, 2),
            "threshold": threshold
        }

    except Exception as e:
        # Fallback in case of conversion error
        print(f"Error checking blur: {e}")
        return {"is_clear": False, "score": 0.0, "error": str(e)}