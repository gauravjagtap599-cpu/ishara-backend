from supabase import create_client

# 🔥 TEMP HARDCODE (to fix crash)
SUPABASE_URL = "https://ezmkkpicphlzkkyopzym.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV6bWtrcGljcGhsemtreW9wenltIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzMwNTgyOTcsImV4cCI6MjA4ODYzNDI5N30.G8qImEgBIkDy5adPFIAtzUec721CygbjtkQwzyONnIw"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def save_purchase(payment_id, subject_code):
    supabase.table("purchases").insert({
        "payment_id": payment_id,
        "subject_code": subject_code
    }).execute()

def get_signed_url(file_name):
    base_url = "https://ezmkkpicphlzkkyopzym.supabase.co/storage/v1/object/public/notes"
    
    url = f"{base_url}/{file_name}"
    
    print("PUBLIC URL:", url)
    
    return url