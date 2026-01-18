import os
from dotenv import load_dotenv

# 1. Try to load the environment
print("--- DIAGNOSTIC START ---")
print(f"Current Working Directory: {os.getcwd()}")

# Check if .env file actually exists here
if os.path.exists(".env"):
    print("✅ Found .env file.")
else:
    print("❌ .env file NOT found in this folder.")
    print("   Please check if it's named '.env.txt' or located in the parent folder.")

# Load it
load_dotenv()

# 2. Check the Key
api_key = os.getenv("OPENAI_API_KEY")

if api_key:
    print(f"✅ API Key found: {api_key[:8]}... (hidden)")
    if api_key.startswith("sk-"):
        print("✅ Key format looks correct (starts with sk-).")
    else:
        print("⚠️  Key format looks weird. It should usually start with 'sk-'.")
else:
    print("❌ API Key is NONE. The .env file is likely empty or formatted wrong.")

print("--- DIAGNOSTIC END ---")