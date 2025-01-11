import cloudinary.uploader
from fastapi import UploadFile, HTTPException, status
import uuid

async def upload_photo(file: UploadFile) -> str:
    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "image/jpg"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File type not allowed. Please upload JPEG or PNG images only."
        )
    
    try:
        # Read file content
        file_content = await file.read()
        if len(file_content) > 5 * 1024 * 1024:  # 5MB limit
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File size too large. Maximum size is 5MB."
            )

        # Upload to Cloudinary
        upload_result = cloudinary.uploader.upload(
            file_content,
            folder="hrms/profile_photos",
            allowed_formats=["jpg", "png", "jpeg"],
            resource_type="image"
        )
        
        return upload_result["secure_url"]
    except cloudinary.exceptions.Error as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Cloudinary upload failed: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Upload failed: {str(e)}"
        )
    finally:
        await file.seek(0)  # Reset file pointer
