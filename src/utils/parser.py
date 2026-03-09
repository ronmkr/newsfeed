import json
import re
from typing import Dict, Any, Optional
from src.utils.logger import project_logger as logger

class RobustJSONParser:
    """Utility to reliably extract and parse JSON from LLM responses."""

    @staticmethod
    def extract_json(raw_text: str) -> Optional[Dict[str, Any]]:
        """
        Attempts to find a JSON block in the text and parse it.
        Handles markdown blocks (```json ... ```) and raw strings.
        """
        if not raw_text:
            return None

        # 1. Try to find content within markdown code blocks
        json_match = re.search(r"```json\s*(\{.*?\})\s*```", raw_text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                logger.warning("Failed to parse JSON inside markdown block.")

        # 2. Try to find the first '{' and last '}'
        start_idx = raw_text.find('{')
        end_idx = raw_text.rfind('}')
        if start_idx != -1 and end_idx != -1:
            try:
                potential_json = raw_text[start_idx : end_idx + 1]
                return json.loads(potential_json)
            except json.JSONDecodeError:
                logger.warning("Failed to parse extracted curly-brace block.")

        # 3. Last ditch: try raw parsing
        try:
            return json.loads(raw_text)
        except json.JSONDecodeError:
            logger.error(f"Could not extract valid JSON from text: {raw_text[:100]}...")
            return None
