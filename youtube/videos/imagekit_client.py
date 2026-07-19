import os
from imagekitio import ImageKit
from django.conf import settings
from imagekitio import ImageKit


def get_imagekit_client():
    os.environ["IMAGEKIT_PRIVATE_KEY"] = settings.IMAGEKIT_PRIVATE_KEY
    os.environ["IMAGEKIT_PUBLIC_KEY"] = settings.IMAGEKIT_PUBLIC_KEY
    os.environ["IMAGEKIT_URL_ENDPOINT"] = settings.IMAGEKIT_URL_ENDPOINT

    return ImageKit()

def upload_video(file_data: bytes,file_name: str, folder: str = "videos") -> dict:
    public_key = os.environ.get("IMAGEKIT_PUBLIC_KEY")

    client = get_imagekit_client()

    response = client.files.upload(
        file=file_data,
        file_name=file_name,
        folder=folder,
    )


    return {
        "file_id": response.file_id,
        "url": response.url,
    }


def upload_thumbnail(file_data: str, file_name: str, folder: str = "thumbnails") -> dict:
    import base64

    # public_key = os.environ.get("IMAGEKIT_PUBLIC_KEY")

    # Fixed typo (file_Date -> file_data) and added string validation

    if isinstance(file_data, str) and file_data.startswith("data:"):
        base64_data = file_data.split(",", 1)[1]
        image_bytes = base64.b64decode(base64_data)
    else:
        image_bytes = file_data

    client = get_imagekit_client()

    response = client.files.upload(
        file=image_bytes,
        file_name=file_name,
        folder=folder,
    )

    return {
        "file_id": response.file_id,
        "url": response.url,
    }

