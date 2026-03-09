import asyncio
from src.pipeline import UnbiasedIndiaNewsPipeline

if __name__ == "__main__":
    pipeline = UnbiasedIndiaNewsPipeline()
    asyncio.run(pipeline.run_daily_batch())
