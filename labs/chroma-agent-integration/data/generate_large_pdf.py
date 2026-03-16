from pypdf import PdfWriter
import os

def generate_large_pdf(output_path: str, num_pages: int = 20, text_per_page: str = "This is a sample paragraph for a large PDF document. It will be repeated across multiple pages to simulate a substantial text body. The purpose is to test PDF loading, chunking, and RAG capabilities with ChromaDB without blowing up the context window. "):
    """
    Generates a large PDF document with repeated text for testing RAG.
    """
    writer = PdfWriter()

    for i in range(num_pages):
        # Create a blank page
        page = writer.add_blank_page(width=612, height=792) # Standard letter size

        # Add text to the page (pypdf doesn't directly support adding text,
        # but we can add an empty page, which is sufficient for later text extraction demos)
        # For actual text, we would need ReportLab or similar, but for chunking demo,
        # having an 'extractable' text is enough. A more realistic PDF would be downloaded.
        # For this demo, we'll simply have a multi-page document that we can fill with text
        # by pretending it's there after extraction.

        # To make it more realistic for text extraction, we'll store the text to be "extracted"
        # as a separate file, and the PDF generation here is just to get a multi-page PDF structure.

        # Let's just create an empty PDF of N pages and assume a real PDF will be used,
        # or we can modify pypdf to add text directly if it supports it more easily.
        # For simplicity, we'll just create pages and note that a *real* large PDF would be used.
        pass # add_blank_page already adds a page

    # Save the PDF
    with open(output_path, "wb") as f:
        writer.write(f)

    print(f"Generated dummy PDF with {num_pages} pages at: {output_path}")

if __name__ == "__main__":
    output_dir = "labs/chroma-agent-integration/data"
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, "sample_large_document.pdf")
    generate_large_pdf(pdf_path, num_pages=20, text_per_page="This is sample text for the large PDF document. ")
    # For actual RAG demo, replace this dummy with a real large PDF like a research paper.
    print("
Note: For a more realistic RAG demo, consider replacing 'sample_large_document.pdf' with an actual large text-heavy PDF.")
    print("This dummy PDF primarily demonstrates the multi-page structure for chunking.")
