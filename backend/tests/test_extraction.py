import os
from file_extractor import extract_text

# Create dummy files for testing if they don't exist
# We'll just test the import and basic function existence first
# To test actual extraction, we'd need a docx file.
# But if the import works, that's 90% of the battle against server crash.

print("Testing imports...")
try:
    import docx
    import pptx
    import bs4
    print("Imports successful.")
except ImportError as e:
    print(f"Import failed: {e}")
    exit(1)

print("Testing extract_text function...")
try:
    # Test with a non-existent file (should return empty string)
    text = extract_text("non_existent_file.docx")
    print(f"Extraction result for non-existent file: '{text}'")
    
    # Create a dummy txt file
    with open("test.txt", "w") as f:
        f.write("Hello World")
    
    text = extract_text("test.txt")
    print(f"Extraction result for test.txt: '{text}'")
    
    if text == "Hello World":
        print("Text extraction verified.")
    else:
        print("Text extraction failed.")
        
    os.remove("test.txt")
    
except Exception as e:
    print(f"Runtime error: {e}")
    exit(1)
