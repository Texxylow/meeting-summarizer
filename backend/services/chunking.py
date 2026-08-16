import re

def chunk_transcript(text: str, max_chunk_words: int = 800) -> list[str]:
    """
    Splits a transcript into chunks of roughly max_chunk_words each,
    without cutting sentences in half.
    """
    # Split into sentences (basic approach: split on . ! ? followed by a space)
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())

    chunks = []
    current_chunk = []
    current_word_count = 0

    for sentence in sentences:
        sentence_word_count = len(sentence.split())

        # If adding this sentence would exceed the limit, start a new chunk
        if current_word_count + sentence_word_count > max_chunk_words and current_chunk:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_word_count = 0

        current_chunk.append(sentence)
        current_word_count += sentence_word_count

    # Add the last chunk if anything remains
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks