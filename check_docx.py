try:
    import docx
    from docx import Document
    print("docx imported successfully")
    print(f"docx location: {docx.__file__}")
except ImportError as e:
    print(f"Error importing docx: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
