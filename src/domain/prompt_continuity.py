"""Enhanced prompt building with continuity instructions."""

from typing import Optional
from .value_objects import ChunkInfo


class ContinuityInstructions:
    """Generate continuity instructions for multi-chunk processing."""
    
    @staticmethod
    def get_chunk_instructions(chunk_info: ChunkInfo) -> str:
        """Get specific instructions based on chunk position."""
        if chunk_info.is_single:
            return ""
        
        if chunk_info.is_first:
            return ContinuityInstructions._get_first_chunk_instructions(chunk_info)
        elif chunk_info.is_last:
            return ContinuityInstructions._get_last_chunk_instructions(chunk_info)
        else:
            return ContinuityInstructions._get_middle_chunk_instructions(chunk_info)
    
    @staticmethod
    def _get_first_chunk_instructions(chunk_info: ChunkInfo) -> str:
        """Instructions for the first chunk."""
        return f"""
## Important Continuity Instructions

This is part 1 of {chunk_info.total} of a larger document that has been split for processing.

**Your response MUST:**
1. Begin formatting from the very first word without any preamble
2. Establish a consistent style and tone that will be maintained throughout
3. End naturally where the text cuts off - do NOT add conclusions or summaries
4. Do NOT indicate that the text is incomplete or will continue
5. Maintain the exact same formatting patterns throughout

**Remember:** Your output will be directly concatenated with the next parts, so ensure it flows seamlessly.
"""

    @staticmethod
    def _get_middle_chunk_instructions(chunk_info: ChunkInfo) -> str:
        """Instructions for middle chunks."""
        return f"""
## Important Continuity Instructions  

This is part {chunk_info.current} of {chunk_info.total} of a larger document.

**Your response MUST:**
1. Continue EXACTLY where the previous part left off
2. Start mid-sentence if that's where the text begins - do NOT add introductions
3. Maintain the EXACT SAME style, tone, and formatting as established in part 1
4. End naturally where the text cuts off - do NOT add conclusions
5. Do NOT reference that this is a continuation or partial text
6. Preserve the flow as if this is one continuous document

**Critical:** Your output will be directly appended to the previous part, so ensure perfect continuity.
"""

    @staticmethod
    def _get_last_chunk_instructions(chunk_info: ChunkInfo) -> str:
        """Instructions for the last chunk."""
        return f"""
## Important Continuity Instructions

This is the final part ({chunk_info.current} of {chunk_info.total}) of a larger document.

**Your response MUST:**
1. Continue EXACTLY where the previous part left off
2. Start mid-sentence if that's where the text begins
3. Maintain the EXACT SAME style, tone, and formatting as all previous parts
4. Complete the document naturally based on the content provided
5. Do NOT reference that this was a multi-part document
6. Ensure the ending flows naturally from everything that came before

**Note:** This completes the document. Format it to its natural conclusion.
"""


class ContinuousPromptBuilder:
    """Enhanced prompt builder that ensures output continuity across chunks."""
    
    def __init__(self, base_builder):
        """Initialize with a base prompt builder."""
        self.base_builder = base_builder
        self.continuity = ContinuityInstructions()
    
    def build_formatting_prompt(
        self,
        instructions: str,
        content: str,
        context: Optional[str] = None,
        chunk_info: Optional[ChunkInfo] = None
    ) -> str:
        """Build prompt with continuity instructions."""
        # Get continuity instructions if processing chunks
        continuity_instructions = ""
        if chunk_info and not chunk_info.is_single:
            continuity_instructions = self.continuity.get_chunk_instructions(chunk_info)
        
        # Enhance the original instructions with continuity guidance
        enhanced_instructions = instructions
        if continuity_instructions:
            enhanced_instructions = f"{instructions}\n{continuity_instructions}"
        
        # Use the base builder with enhanced instructions
        return self.base_builder.build_formatting_prompt(
            instructions=enhanced_instructions,
            content=content,
            context=context,
            chunk_info=chunk_info
        )
    
    def build_continuation_header(self, chunk_info: ChunkInfo) -> str:
        """Build continuation header (delegates to base builder)."""
        return self.base_builder.build_continuation_header(chunk_info)