from src.pipeline import UnbiasedIndiaNewsPipeline

if __name__ == "__main__":
    pipeline = UnbiasedIndiaNewsPipeline()
    pipeline.run_daily_batch()
