"""Hashtag combination generator module."""

from typing import List
from config import BLOCK_SIZE


def generate_combinations(roots: List[str], suffixes: List[str]) -> List[str]:
    """
    Generate all hashtag combinations from roots and suffixes.
    
    Args:
        roots: List of root words
        suffixes: List of suffix words
        
    Returns:
        List of unique hashtags with # prefix
    """
    hashtags = set()
    
    for root in roots:
        root = root.strip()
        if not root:
            continue
            
        for suffix in suffixes:
            suffix = suffix.strip()
            if not suffix:
                continue
                
            # Create hashtag: #root+suffix
            hashtag = f"#{root}{suffix}"
            hashtags.add(hashtag.lower())
    
    return list(hashtags)


def split_into_blocks(hashtags: List[str], size: int = BLOCK_SIZE) -> List[List[str]]:
    """
    Split hashtags into blocks of specified size.
    
    Args:
        hashtags: List of hashtags
        size: Number of hashtags per block (default: 30)
        
    Returns:
        List of hashtag blocks
    """
    blocks = []
    for i in range(0, len(hashtags), size):
        blocks.append(hashtags[i:i + size])
    return blocks


def format_block(block: List[str]) -> str:
    """
    Format a block of hashtags as a single string for copy-paste.
    
    Args:
        block: List of hashtags
        
    Returns:
        Space-separated string of hashtags
    """
    return " ".join(block)


def parse_input(text: str) -> tuple[List[str], List[str]]:
    """
    Parse user input to extract roots and suffixes.
    
    Supported formats:
        1. Multi-line:
           Корни: слово1, слово2
           Суффиксы: окончание1, окончание2
        
        2. Single-line:
           Корни: слово1, слово2 Суффиксы: окончание1, окончание2
    
    Args:
        text: User message text
        
    Returns:
        Tuple of (roots, suffixes) lists
    """
    import re
    
    roots = []
    suffixes = []
    
    # Normalize text - replace multiple spaces with single space
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Try to find roots pattern (case-insensitive)
    roots_match = re.search(
        r'(?:корни|roots)\s*:\s*([^:]+?)(?=\s*(?:суффиксы|suffixes)\s*:|$)',
        text,
        re.IGNORECASE
    )
    if roots_match:
        roots_text = roots_match.group(1).strip()
        roots = [r.strip() for r in roots_text.split(",") if r.strip()]
    
    # Try to find suffixes pattern (case-insensitive)
    suffixes_match = re.search(
        r'(?:суффиксы|suffixes)\s*:\s*(.+?)$',
        text,
        re.IGNORECASE
    )
    if suffixes_match:
        suffixes_text = suffixes_match.group(1).strip()
        suffixes = [s.strip() for s in suffixes_text.split(",") if s.strip()]
    
    return roots, suffixes
