import cloudinary
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def init_cloudinary():
    # Configure Cloudinary
    cloudinary.config(
        cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
        api_key=os.getenv('CLOUDINARY_API_KEY'),
        api_secret=os.getenv('CLOUDINARY_API_SECRET'),
        secure=True
    )

    # Verify configuration
    if not all([os.getenv('CLOUDINARY_CLOUD_NAME'), 
                os.getenv('CLOUDINARY_API_KEY'), 
                os.getenv('CLOUDINARY_API_SECRET')]):
        raise ValueError("Cloudinary configuration is missing. Please check your environment variables.")
