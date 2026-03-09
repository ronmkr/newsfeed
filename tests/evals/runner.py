import json
import os
import sys
from typing import List, Dict, Any

from src.agents.graph import create_pipeline
from src.utils.logger import project_logger as logger

def calculate_variance(agent_score: float, human_score: float) -> float:
    """Calculates the percentage variance between agent and human scores."""
    # Scores are between -2 and +2 (range of 4)
    # Variance is (diff / range) * 100
    diff = abs(agent_score - human_score)
    variance_pct = (diff / 4.0) * 100
    return variance_pct

def run_evaluations(gold_standard_path: str, threshold: float = 20.0):
    """Runs the Auditor Agent against gold standard data and compares results."""
    logger.info(f"Starting Auditor Evaluation Run (Threshold: {threshold}%)")
    
    if not os.path.exists(gold_standard_path):
        logger.error(f"Gold standard file not found: {gold_standard_path}")
        sys.exit(1)
        
    with open(gold_standard_path, 'r') as f:
        test_cases = json.load(f)
        
    pipeline = create_pipeline()
    failures = []
    
    for case in test_cases:
        logger.info(f"Evaluating Case: {case['description']} ({case['test_id']})")
        
        # Prepare state for the pipeline
        # (Injecting pre-clustered articles into the state for evaluation)
        initial_state = {
            "clusters": [],
            "current_cluster_index": 0,
            "raw_data": case["articles"],
            "errors": [],
            "next_step": ""
        }
        
        # Run the pipeline (Scout -> Auditor -> Editor)
        final_state = pipeline.invoke(initial_state)
        
        # Extract the Auditor's score from the first cluster
        if not final_state["clusters"]:
            logger.error(f"Fail: Agent produced no clusters for {case['test_id']}")
            failures.append(case['test_id'])
            continue
            
        agent_score = final_state["clusters"][0].overall_bias
        human_score = case["human_bias_score"]
        
        variance = calculate_variance(agent_score, human_score)
        
        logger.info(f"Agent Score: {agent_score} | Human Score: {human_score}")
        logger.info(f"Variance: {variance:.2f}%")
        
        if variance > threshold:
            logger.error(f"FAIL: Variance {variance:.2f}% exceeds threshold for {case['test_id']}")
            failures.append(case['test_id'])
        else:
            logger.success(f"PASS: {case['test_id']}")
            
    # Final Result
    if failures:
        logger.error(f"Evaluation Failed: {len(failures)} cases exceeded the {threshold}% variance threshold.")
        sys.exit(1)
    else:
        logger.success("All evaluation cases passed within the variance threshold!")
        sys.exit(0)

if __name__ == "__main__":
    GOLD_STANDARD = "tests/evals/gold_standard.json"
    run_evaluations(GOLD_STANDARD)
