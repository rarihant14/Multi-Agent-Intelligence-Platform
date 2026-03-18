import os
from pathlib import Path

class PDFParser:
    @staticmethod
    def parse_pdf(file_path: str):
        try:
            import PyPDF2
            
            if not os.path.exists(file_path):
                return {"success": False, "error": "File not found"}
            
            full_text = ""
            num_pages = 0
            
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                num_pages = len(reader.pages)
                
                for page_num, page in enumerate(reader.pages):
                    text = page.extract_text()
                    full_text += f"\n--- Page {page_num + 1} ---\n{text}"
            
            return {
                "success": True,
                "full_text": full_text,
                "num_pages": num_pages,
                "pages": list(range(1, num_pages + 1)),
                "metadata": {"filename": Path(file_path).name}
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def search_in_pdf(file_path: str, query: str):
        parsed = PDFParser.parse_pdf(file_path)
        if not parsed["success"]:
            return []
        
        text = parsed["full_text"].lower()
        query_lower = query.lower()
        
        if query_lower in text:
            start = max(0, text.find(query_lower) - 100)
            end = min(len(text), text.find(query_lower) + 200)
            return [text[start:end]]
        
        return []

pdf_parser = PDFParser()
