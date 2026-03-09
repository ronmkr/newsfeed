import json
import re
from typing import Dict, Any, Optional
from src.utils.logger import project_logger as logger

class RobustJSONParser:
    """Provides resilient JSON extraction from unstructured AI responses."""

    @staticmethod
    def extract_json(raw_text: str) -> Optional[Dict[str, Any]]:
        """
        Extracts and parses JSON from text, handling markdown blocks and loose text.
        
        Args:
            raw_text: The raw string response from an LLM.
        Returns:
            A dictionary if extraction is successful, else None.
        """
        if not raw_text or not isinstance(raw_text, str):
            return None

        # Clean potential whitespace/newlines
        text = raw_text.strip()

        # Pattern 1: Markdown code blocks
        md_match = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
        if md_match:
            result = RobustJSONParser._parse_string(md_match.group(1))
            if result: return result

        # Pattern 2: First '{' to last '}'
        brace_match = re.search(r"(\{.*\})", text, re.DOTALL)
        if brace_match:
            result = RobustJSONParser._parse_string(brace_match.group(1))
            if result: return result

        # Fallback: Direct parse
        return RobustJSONParser._parse_string(text)

    @staticmethod
    def _parse_string(json_str: str) -> Optional[Dict[str, Any]]:
        """Internal helper for json.loads with logging."""
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            logger.debug(f"JSON Decode Error: {e} | Text fragment: {json_str[:50]}...")
            return None
