# Basic chunking and can be definitely improved
def create_chunks_from(text: str, chunk_size=500, overlap=50) -> list[str]:
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i : i + chunk_size])
        chunks.append(chunk)

    return chunks
