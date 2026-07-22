import os
from io import BytesIO
from django.core.files.storage import Storage
from django.core.files.base import ContentFile
from django.utils.deconstruct import deconstructible
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url: str = os.getenv("SUPABASE_URL", "")
key: str = os.getenv("SUPABASE_KEY", "")
supabase: Client = create_client(url, key)

@deconstructible
class SupabaseStorage(Storage):
    def __init__(self, bucket_name='homework_submissions'):
        self.bucket_name = bucket_name

    def _open(self, name, mode='rb'):
        res = supabase.storage.from_(self.bucket_name).download(name)
        return ContentFile(res)

    def _save(self, name, content):
        content_bytes = content.read()
        # Ensure we are at the start of the file if it's already been read
        if hasattr(content, 'seek'):
            content.seek(0)
            
        try:
            supabase.storage.from_(self.bucket_name).upload(
                path=name,
                file=content_bytes,
                file_options={"content-type": getattr(content, 'content_type', 'application/octet-stream')}
            )
        except Exception as e:
            # If the file already exists, it might throw an error. 
            # In a production app, we would handle naming collisions (like django does).
            print("Error uploading to supabase:", e)
            
        return name

    def exists(self, name):
        # We can list files to see if it exists, or just return False to always upload
        return False 

    def url(self, name):
        return supabase.storage.from_(self.bucket_name).get_public_url(name)

    def get_available_name(self, name, max_length=None):
        return name
