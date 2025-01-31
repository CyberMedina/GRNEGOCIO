import cloudinary
import cloudinary.uploader
import cloudinary.api
from cloudinary.utils import private_download_url
import os
from dotenv import load_dotenv

load_dotenv()
# Configure Cloudinary credentials
# (You can also store these in environment variables for security)
cloudinary.config(
    cloud_name= os.getenv('CLOUD_NAME'),
    api_key= os.getenv('API_KEY'),
    api_secret= os.getenv('API_SECRET'),
    secure=True
)






def get_authenticated_url(public_id, file_format='jpg'):
    """
    Generate a time-limited, signed URL for an authenticated resource in Cloudinary.
    
    :param public_id: The public ID of the uploaded asset.
    :param file_format: The file format/extension for the output (e.g., jpg, png).
    :return: A signed URL that can be used to access the authenticated asset.
    """
    # resource_type defaults to 'image', but can be adjusted (e.g., 'video') if needed.
    resource_type = 'image'
    url = private_download_url(
        public_id=public_id,
        format=file_format,
        resource_type=resource_type,
        type='authenticated',
        # sign_url is True by default in private_download_url, but we can explicitly set it:
        sign_url=True
    )
    return url

print(get_authenticated_url('my_private_folder/ebykdteoltflbdncqyks'))