from typing import List, Dict
from pypdf import PdfReader
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter

def extract_text_from_pdf(pdf_path: str) -> List[Dict[str, str]]:
    """
    Extracts text from each page of a PDF document.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        List[Dict[str, str]]: A list of dictionaries, where each dictionary
                              represents a page with its text content and page number.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found at: {pdf_path}")

    reader = PdfReader(pdf_path)
    extracted_pages = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        extracted_pages.append({
            "page_content": text if text else "", # Ensure text is not None
            "page_number": i + 1,
            "source": pdf_path
        })
    return extracted_pages

def chunk_text(pages: List[Dict[str, str]], chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Dict[str, Any]]:
    """
    Chunks extracted text from PDF pages into smaller pieces suitable for embedding.

    Args:
        pages (List[Dict[str, str]]): List of dictionaries, each containing 'page_content', 'page_number', 'source'.
        chunk_size (int): The maximum number of characters in each chunk.
        chunk_overlap (int): The number of characters to overlap between chunks.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, where each dictionary represents a chunk
                              with its content and metadata (page_number, source).
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        add_start_index=True,
    )
    chunks = []
    for page_data in pages:
        page_content = page_data['page_content']
        page_number = page_data['page_number']
        source = page_data['source']

        # Ensure we have content to chunk
        if not page_content.strip():
            continue

        split_chunks = text_splitter.create_documents(
            texts=[page_content],
            metadatas=[{"page_number": page_number, "source": source}]
        )
        for chunk in split_chunks:
            chunks.append({
                "document": chunk.page_content,
                "metadata": chunk.metadata,
                "id": f"{os.path.basename(source)}-p{page_number}-c{chunk.metadata['start_index']}"
            })
    return chunks

if __name__ == "__main__":
    # Example usage: Requires a PDF file to exist in data/
    data_dir = "labs/chroma-agent-integration/data"
    sample_pdf_path = os.path.join(data_dir, "sample_large_document.pdf")

    # Generate a dummy PDF if it doesn't exist for testing
    if not os.path.exists(sample_pdf_path):
        from generate_large_pdf import generate_large_pdf
        print(f"Generating dummy PDF for testing: {sample_pdf_path}")
        generate_large_pdf(sample_pdf_path, num_pages=2, text_per_page="This is sample text for the large PDF document. ")
    else:
        print(f"Using existing PDF: {sample_pdf_path}")


    try:
        pages = extract_text_from_pdf(sample_pdf_path)
        print(f"\nExtracted {len(pages)} pages from {sample_pdf_path}")
        # Note: Dummy PDF has empty pages, so text content will be empty
        if any(page['page_content'].strip() for page in pages):
            chunks = chunk_text(pages)
            print(f"Generated {len(chunks)} chunks.")
            if chunks:
                print("\n--- First Chunk ---")
                print(f"Content: {chunks[0]['document'][:200]}...")
                print(f"Metadata: {chunks[0]['metadata']}")
        else:
            print("No text content extracted from PDF, cannot chunk.")

    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred: {e}")

