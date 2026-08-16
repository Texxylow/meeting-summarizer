from services.chunking import chunk_transcript

sample_text = "This is sentence one. This is sentence two! Is this sentence three? Yes it is, and here's sentence four."

chunks = chunk_transcript(sample_text, max_chunk_words=5)

for i, chunk in enumerate(chunks):
    print(f"--- Chunk {i+1} ---")
    print(chunk)
    print()