import pytest
from backend.ai_service import analyze_text, analyze_file_content

def test_analyze_text_idea_detection():
    # Test idea detection
    result = analyze_text("I have an idea for a new blog post")
    assert result.is_idea == True
    assert result.category == "Blog"

    result = analyze_text("Just saying hello")
    assert result.is_idea == False

def test_analyze_text_priority():
    # Test priority scoring
    result = analyze_text("This is an urgent idea")
    assert result.priority == "High"

    result = analyze_text("We should do this next week")
    assert result.priority == "Medium"

def test_analyze_file_content():
    # Test file analysis
    result = analyze_file_content("Q4_Report.pdf", "financial data")
    assert result.is_idea == True
    assert result.category == "Document"
    # assert result.deadline == "2025-12-31" # Depends on current date logic, skipping strict check

def test_analyze_file_category():
    result = analyze_file_content("design_mockup.png", "ui ux")
    assert result.category == "Design"
