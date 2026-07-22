import os
from imagekitio import ImageKit
from django.conf import settings
from imagekitio import ImageKit
import base64
import io


def get_imagekit_client():
    os.environ["IMAGEKIT_PRIVATE_KEY"] = settings.IMAGEKIT_PRIVATE_KEY
    os.environ["IMAGEKIT_PUBLIC_KEY"] = settings.IMAGEKIT_PUBLIC_KEY
    os.environ["IMAGEKIT_URL_ENDPOINT"] = settings.IMAGEKIT_URL_ENDPOINT

    return ImageKit()

def upload_video(file_data: bytes,file_name: str, folder: str = "videos") -> dict:
    # public_key = os.environ.get("IMAGEKIT_PUBLIC_KEY")
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

def get_optimized_video_url(base_url:str) -> str:
    if "?" in base_url:
        return f"{base_url}&tr=q-80,f-auto" # using imagekit quality parameter to optimize videos
    return f"{base_url}?tr=q-80,f-auto" # read the documentation for more transformations: https://docs.imagekit.io/features/video-transformations

def get_streaming_video_url(base_url:str) -> str:
    return f"{base_url}?ik-master.m3u8"

def get_thumbnail_url(base_url:str, width : int= 480, height : int = 270) -> str:
    return f"{base_url}/ik-thumbnail.jpg"



def upload_thumbnail(file_data: str, file_name: str, folder: str = "thumbnails") -> dict:
    client = get_imagekit_client()

    # public_key = os.environ.get("IMAGEKIT_PUBLIC_KEY")
    # Fixed typo (file_Date -> file_data) and added string validation

    if isinstance(file_data, str) and file_data.startswith("data:"):
        base64_payload = file_data.split(",")[1]
        thumbnail_bytes = base64.b64decode(base64_payload)
    else:
        thumbnail_bytes = base64.b64decode(file_data)

    # Wrap raw bytes in a BytesIO stream object so the SDK accepts it seamlessly
    file_stream = io.BytesIO(thumbnail_bytes)

    response = client.files.upload(
        file=file_stream,
        file_name=file_name,
        folder=folder,
    )

    return {
        "file_id": response.file_id,
        "url": response.url,
    }

# adding deleting file option

def delete_video(file_id: str) -> bool:
    client = get_imagekit_client()
    client.files.delete(file_id)
    return True