import io
import uuid
from supabase import create_client

url = "https://zrxeteoauwceolemurjd.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpyeGV0ZW9hdXdjZW9sZW11cmpkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA1MjkzODAsImV4cCI6MjA2NjEwNTM4MH0.nX_K0VkdzjZB9GymyvUvQeIxNjs0ccRjZuiIW5c5D0U"

supabase = create_client(url, key)


