import requests
import time

BASE = "http://localhost:8000"

# Login first
login = requests.post(f"{BASE}/users/login", json={
    "username": "anan",
    "password": "password123"
})
token   = login.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}
print(f"✅ Logged in")

# Upload PDF — requests handles binary correctly
pdf_path = r"D:\LLM_RAG_learning\documind-ai\test.pdf"

with open(pdf_path, "rb") as f:
    upload = requests.post(
        f"{BASE}/documents/upload",
        headers=headers,
        files={"file": ("test.pdf", f, "application/pdf")}
    )

print(f"Upload: {upload.json()}")
doc_id = upload.json()["document_id"]

# Wait for processing
print("⏳ Waiting 20s...")
time.sleep(20)

# Check status
status = requests.get(f"{BASE}/documents/{doc_id}", headers=headers)
print(f"Status: {status.json()}")

if status.json()["status"] == "ready":
    # Ask question
    chat = requests.post(
        f"{BASE}/chat/{doc_id}",
        headers=headers,
        json={"question": "What is this document about?"}
    )
    print(f"\n✅ Answer: {chat.json()['answer']}")
    print(f"Score: {chat.json()['retrieval_score']}")
    print(f"Sources: {len(chat.json()['sources'])}")

    # History
    history = requests.get(f"{BASE}/chat/{doc_id}/history", headers=headers)
    print(f"\n✅ Chat history: {len(history.json())} entries saved")