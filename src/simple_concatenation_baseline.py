"""
As a simple baseline, we want to simply concatenate all highlights
"""

import logging
from datasets import load_metric

import pandas as pd
from src.compute_metrics import compute_rouge_metrics
from src.concatenate_highlights import concatenate_highlights
from src.predictions_analyzer import PredictionsAnalyzer


def main(config: dict, summaries_to_test_key: str):
    # Setup logging
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        level=logging.INFO
    )

    df = pd.read_csv(config['test_file'])
    inputs = list(df['doc_text'])
    summaries = list(df['summary_text'])

    logging.info("Creating summaries...")

    if summaries_to_test_key == "gold_summaries":
        summaries_to_test = summaries
    elif summaries_to_test_key == "simple_concatenation":
        summaries_to_test = concatenate_highlights(df)
    else:
        raise ValueError(f"Unexpeceted key for summaries_to_text ; {summaries_to_test_key}")

    logging.info("Evaluating...")
    # Calc rouge
    metric = load_metric("rouge")
    result = compute_rouge_metrics(summaries_to_test, summaries, metric, prefix="gold")
    logging.info(result)
    logging.info("Analyzing predictions...")

    # Extract predictions file
    PredictionsAnalyzer(None, None, False, config['output_dir'], metric).write_predictions_to_file(summaries_to_test, inputs, df, is_tokenized=False)
