# test_rag.py — test RAG pipeline before connecting to API
from rag_pipeline import (
    extract_text_from_pdf,
    chunk_text,
    create_embeddings,
    store_in_chromadb,
    retrieve_relevant_chunks,
    generate_answer,
    answer_question
)

# Use any PDF you have — copy one into documind-ai folder
PDF_PATH = "test.pdf"   # ← put any PDF here

print("=" * 50)
print("TEST 1: PDF Extraction")
print("=" * 50)
text, pages = extract_text_from_pdf(PDF_PATH)
print(f"✅ Extracted {len(text)} chars from {pages} pages")
print(f"   Preview: {text[:200].strip()}")

print("\n" + "=" * 50)
print("TEST 2: Chunking")
print("=" * 50)
chunks = chunk_text(text)
print(f"✅ Created {len(chunks)} chunks")
print(f"   Avg size: {sum(len(c) for c in chunks)//len(chunks)} chars")
print(f"   Sample: {chunks[0][:150]}")

print("\n" + "=" * 50)
print("TEST 3: Embeddings")
print("=" * 50)
# Test with first 5 chunks only
sample_chunks  = chunks[:5]
sample_embeds  = create_embeddings(sample_chunks)
print(f"✅ Created {len(sample_embeds)} embeddings")
print(f"   Dimensions: {len(sample_embeds[0])}")

print("\n" + "=" * 50)
print("TEST 4: ChromaDB Storage")
print("=" * 50)
store_in_chromadb(
    document_id=999,
    chunks=sample_chunks,
    embeddings=sample_embeds,
    username="testuser"
)
print(f"✅ Stored {len(sample_chunks)} chunks")

print("\n" + "=" * 50)
print("TEST 5: Retrieval")
print("=" * 50)
retrieved, distances = retrieve_relevant_chunks(
    document_id=999,
    question="What is this document about?",
    username="testuser",
    n_results=2
)
print(f"✅ Retrieved {len(retrieved)} chunks")
for i, (chunk, dist) in enumerate(zip(retrieved, distances)):
    print(f"   #{i+1} (dist={dist:.3f}): {chunk[:100].strip()}")

print("\n" + "=" * 50)
print("TEST 6: Full Answer Generation")
print("=" * 50)
result = answer_question(
    document_id=999,
    question="What is this document about?",
    username="testuser",
    document_name="Test Document"
)
print(f"✅ Answer generated")
print(f"   Answer: {result['answer'][:300]}")
print(f"   Retrieval score: {result['retrieval_score']}")
print(f"   Sources: {len(result['sources'])}")

print("\n✅ All RAG tests passed!")