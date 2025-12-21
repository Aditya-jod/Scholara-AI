#!/usr/bin/env python3
"""
Test script to verify mock mode functionality without requiring API dependencies.
"""

import json
import sys
import os

# Add src to path for imports
sys.path.insert(0, 'src')

def test_mock_data_files():
    """Test that all required mock data files exist and are valid JSON."""
    mock_files = [
        'mock_data/concepts.json',
        'mock_data/concept_map.json', 
        'mock_data/quiz.json',
        'mock_data/validation.json'
    ]
    
    print("Testing mock data files...")
    for file_path in mock_files:
        if not os.path.exists(file_path):
            print(f"❌ Missing file: {file_path}")
            return False
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            print(f"✅ Valid JSON: {file_path}")
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in {file_path}: {e}")
            return False
    
    return True

def test_mock_mode_logic():
    """Test the mock mode logic without importing LLM dependencies."""
    print("\nTesting mock mode logic...")
    
    # Test load_mock_data function
    def load_mock_data(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    
    try:
        # Test loading each mock file
        concepts = load_mock_data("mock_data/concepts.json")
        concept_map = load_mock_data("mock_data/concept_map.json")
        quiz = load_mock_data("mock_data/quiz.json")
        validation = load_mock_data("mock_data/validation.json")
        
        # Validate structure
        assert isinstance(concepts, dict), "Concepts should be a dict"
        assert "concept_map" in concept_map, "Concept map should have 'concept_map' key"
        assert isinstance(quiz, list), "Quiz should be a list"
        assert isinstance(validation, list), "Validation should be a list"
        
        print("✅ Mock data structure validation passed")
        return True
        
    except Exception as e:
        print(f"❌ Mock mode logic test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Scholara AI Mock Mode\n")
    
    success = True
    success &= test_mock_data_files()
    success &= test_mock_mode_logic()
    
    if success:
        print("\n🎉 All tests passed! Mock mode should work correctly.")
        print("\nTo run the application:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Set MODE='mock' in src/run_pipeline.py (currently set)")
        print("3. Run: streamlit run streamlit_app.py")
    else:
        print("\n❌ Some tests failed. Please fix the issues above.")
        sys.exit(1)