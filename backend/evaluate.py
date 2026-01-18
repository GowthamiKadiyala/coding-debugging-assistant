import pytest
import os
from deepeval import assert_test
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric
from deepeval.test_case import LLMTestCase
from agent import get_agent

# 1. Define the Metrics (The "Rubric")
# Faithfulness: Did the AI hallucinate? (We want this high)
# Answer Relevancy: Did it actually answer the user's question?
faithfulness = FaithfulnessMetric(threshold=0.7, model="gpt-4o", include_reason=True)
relevancy = AnswerRelevancyMetric(threshold=0.7, model="gpt-4o", include_reason=True)

# 2. Define "Golden Data" (Questions with Known Correct Answers)
test_cases = [
    {
        "input": "How do I fix the division by zero error in test_bug.py?",
        "expected_output": "Check if the list is empty using 'if not numbers' before dividing.",
        "context": ["def calculate_average(numbers):\n    return total / len(numbers)"] 
    },
    {
        "input": "What library is used for vector storage in this project?",
        "expected_output": "ChromaDB is used for vector storage.",
        "context": ["import chromadb", "db = Chroma.from_documents(...)"]
    }
]

@pytest.mark.parametrize("case", test_cases)
def test_agent_logic(case):
    print(f"\n🧪 Testing Question: {case['input']}")
    
    # Run your actual Agent
    agent = get_agent()
    response = agent.invoke({"input": case["input"]})
    actual_output = response["output"]

    print(f"🤖 Agent Answer: {actual_output}")

    # Create a DeepEval Test Case
    test_case = LLMTestCase(
        input=case["input"],
        actual_output=actual_output,
        expected_output=case["expected_output"],
        retrieval_context=case["context"]
    )

    # Assert (Pass if metrics > 0.7)
    assert_test(test_case, [faithfulness, relevancy])