import os
from io import BytesIO
from django.core.files.storage import Storage, FileSystemStorage
from django.core.files.base import ContentFile
from django.utils.deconstruct import deconstructible
from dotenv import load_dotenv

load_dotenv()

@deconstructible
class SupabaseStorage(Storage):
    def __init__(self, bucket_name='homework_submissions'):
        self.bucket_name = bucket_name
        self._client = None

    @property
    def client(self):
        if self._client is None:
            url: str = os.getenv("SUPABASE_URL", "")
            key: str = os.getenv("SUPABASE_KEY", "")
            if url and key:
                try:
                    from supabase import create_client
                    self._client = create_client(url, key)
                except Exception as e:
                    print("Error initializing Supabase client:", e)
        return self._client

    def _open(self, name, mode='rb'):
        if self.client:
            try:
                res = self.client.storage.from_(self.bucket_name).download(name)
                return ContentFile(res)
            except Exception as e:
                print("Error downloading from Supabase:", e)
        return FileSystemStorage()._open(name, mode)

    def _save(self, name, content):
        content_bytes = content.read()
        if hasattr(content, 'seek'):
            content.seek(0)
            
        if self.client:
            try:
                self.client.storage.from_(self.bucket_name).upload(
                    path=name,
                    file=content_bytes,
                    file_options={"content-type": getattr(content, 'content_type', 'application/octet-stream')}
                )
                return name
            except Exception as e:
                print("Error uploading to Supabase:", e)

        return FileSystemStorage()._save(name, content)

    def exists(self, name):
        return False 

    def url(self, name):
        if self.client:
            try:
                return self.client.storage.from_(self.bucket_name).get_public_url(name)
            except Exception as e:
                print("Error getting Supabase URL:", e)
        return FileSystemStorage().url(name)

    def get_available_name(self, name, max_length=None):
        return name
