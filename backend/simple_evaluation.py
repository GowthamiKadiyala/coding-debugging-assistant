import sys
from agent import get_agent

# 1. Define the Exam Questions ("Golden Dataset")
test_cases = [
    {
        "question": "How do I fix the division by zero error in test_bug.py?",
        # We expect the AI to mention checking if the list is empty
        "required_keywords": ["empty", "if", "return", "0"] 
    },
    {
        "question": "Where is the index_codebase function defined?",
        # We expect the AI to find the correct file
        "required_keywords": ["indexer.py"]
    }
]

def run_tests():
    print("🚀 Starting Automated Agent Tests...\n")
    agent = get_agent()
    score = 0
    
    for i, case in enumerate(test_cases):
        print(f"--- Test Case {i+1} ---")
        print(f"❓ Input: {case['question']}")
        
        # Run the Agent
        try:
            response = agent.invoke({"input": case['question']})
            answer = response["output"]
            print(f"🤖 Output: {answer}\n")
            
            # Grade the Answer (Simple Keyword Match)
            # A Senior Engineer would use an LLM here, but keywords work for a smoke test
            missing_words = [word for word in case['required_keywords'] if word.lower() not in answer.lower()]
            
            if not missing_words:
                print("✅ PASSED")
                score += 1
            else:
                print(f"❌ FAILED - Missing keywords: {missing_words}")
                
        except Exception as e:
            print(f"❌ CRASHED: {e}")
            
    print(f"\n📊 Final Score: {score}/{len(test_cases)}")
    if score == len(test_cases):
        print("🎉 READY FOR PRODUCTION")
    else:
        print("⚠️  NEEDS IMPROVEMENT")

if __name__ == "__main__":
    run_tests()