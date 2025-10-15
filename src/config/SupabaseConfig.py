from supabase import create_client
from dotenv import get_key

url = get_key(".env", "SUPABASE_URL")
key = get_key(".env", "SUPABASE_API_KEY")

supabase = create_client(url, key)
