import cv2
import os
import pytesseract
import re
from PIL import Image
import platform


def get_tesseract_cmd():
    if platform.system() == "Windows":
        default_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        ]
    else:  # Linux macOS
        default_paths = ["/usr/bin/tesseract", "/usr/local/bin/tesseract"]

    # Check if tesseract is in PATH
    try:
        pytesseract.pytesseract.tesseract_cmd = "tesseract"  # Try the default PATH
        pytesseract.image_to_string(Image.new("RGB", (10, 10)))  # Test image
        return "tesseract"  # Success
    except (pytesseract.TesseractNotFoundError, FileNotFoundError):
        pass

    # Install locations
    for path in default_paths:
        if os.path.exists(path):
            return path

    raise pytesseract.TesseractNotFoundError(
        "Tesseract not found. Please install it and ensure it's in your PATH."
    )


# Set Tesseract path automatically
pytesseract.pytesseract.tesseract_cmd = get_tesseract_cmd()


# Upscale image
def upscale_opencv_new(image_path, output_path, model_path, set_model="fsrcnn"):
    if not all(os.path.exists(p) for p in [image_path, model_path]):
        raise FileNotFoundError("Input image or model file not found.")

    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Failed to read the image.")

    sr = cv2.dnn_superres.DnnSuperResImpl_create()
    sr.readModel(model_path)
    sr.setModel(set_model.lower(), 4)  # x4 upscaling
    result = sr.upsample(img)
    cv2.imwrite(output_path, result)


def extract_passport_info(image_path="passport_upscaled_sharp.png"):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)

    print("\n--- OCR Raw Output ---")
    print(text)

    info = {}
    patterns = {
        "Passport Number": r"\b[A-Z]{2}[0-9]{7}\b",
        "Nationality": r"\b[A-Z]{3}\b",
        "Name (P< format)": r"P<[A-Z]{3}([A-Z]+)<<([A-Z<]+)",
        "Sex": r"\b[MFO]\b",
        "Dates": r"\b[0-9]{2}-[A-Za-z]{3}-[0-9]{4}\b",
    }

    # Extract fields
    info["Passport Number"] = re.search(patterns["Passport Number"], text)
    info["Nationality"] = re.search(patterns["Nationality"], text)

    if name_match := re.search(patterns["Name (P< format)"], text):
        info["Last Name"] = name_match.group(1).replace("<", " ").strip()
        info["First Name"] = name_match.group(2).replace("<", " ").strip()

    if dates := re.findall(patterns["Dates"], text):
        info.update(zip(["DOB", "Issue Date", "Expiry Date"], dates[:3]))

    print("\n--- Extracted Data ---")
    for k, v in info.items():
        if v:
            print(f"{k}: {v.group() if hasattr(v, 'group') else v}")


# Example
if __name__ == "__main__":
    try:
        upscale_opencv_new(
            "passport.png",
            "passport_upscaled_sharp.png",
            "FSRCNN_x4.pb",  # Ensure this model file exists
        )
        extract_passport_info()
    except Exception as e:
        print(f"Error: {e}")
