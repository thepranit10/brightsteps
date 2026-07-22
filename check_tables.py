import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brightsteps_admin.settings')
django.setup()
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema';")
    print("Tables:", cursor.fetchall())
    
    cursor.execute("SELECT * FROM event_photo;")
    print("Photos:", cursor.fetchall())
