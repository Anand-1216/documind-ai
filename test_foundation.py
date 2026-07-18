# test_foundation.py — verify foundation before building RAG
from database import engine, Base
from models import User, Document, ChatHistory
from auth import hash_password, verify_password, create_access_token, verify_token
from config import settings

print("Testing foundation...\n")

# Test 1: DB creation
print("1. Creating database tables...")
Base.metadata.create_all(bind=engine)
print("   ✅ Tables created")

# Test 2: Password hashing
print("\n2. Testing password hashing...")
hashed = hash_password("mypassword123")
assert verify_password("mypassword123", hashed) == True
assert verify_password("wrongpassword", hashed) == False
print("   ✅ Password hashing works")

# Test 3: JWT tokens
print("\n3. Testing JWT tokens...")
token    = create_access_token({"sub": "testuser"})
username = verify_token(token)
assert username == "testuser"
print(f"   ✅ Token created and verified for: {username}")

# Test 4: Settings loaded
print("\n4. Testing config...")
assert settings.GEMINI_API_KEY != ""
assert settings.SECRET_KEY != ""
print(f"   ✅ Config loaded")
print(f"   Gemini key: {settings.GEMINI_API_KEY[:10]}...")
print(f"   DB URL: {settings.DATABASE_URL}")

print("\n✅ All foundation tests passed!")
print("   Ready to build RAG pipeline")