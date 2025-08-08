"""Service for building well-formatted prompts."""

from typing import List, Optional

from ..value_objects import ChunkInfo
from ..constants import (
    CHUNK_HEADER_FORMAT,
    SINGLE_HEADER_FORMAT,
    CONTINUATION_HEADER_FORMAT,
    SECTION_DIVIDER,
    SEPARATOR_WIDTH
)


class PromptBuilder:
    """Service for building well-formatted prompts."""
    
    def __init__(self, separator_width: int = SEPARATOR_WIDTH):
        """Initialize with configuration."""
        self.separator_width = separator_width
    
    def build_formatting_prompt(
        self,
        instructions: str,
        content: str,
        context: Optional[str] = None,
        chunk_info: Optional[ChunkInfo] = None
    ) -> str:
        """Build a complete, well-structured formatting prompt."""
        sections = []
        
        # Add context section if provided
        if context:
            sections.append(self._format_section("Context", context))
        
        # Add instructions section
        if instructions:
            sections.append(self._format_section("Instructions", instructions))
        
        # Add content section with appropriate header
        if content:
            header = self._get_content_header(chunk_info)
            sections.append(self._format_content_section(header, content))
        
        return self._join_sections(sections)
    
    def build_continuation_header(self, chunk_info: ChunkInfo) -> str:
        """Build header for continuation chunks."""
        separator = "=" * self.separator_width
        header = CONTINUATION_HEADER_FORMAT.format(
            chunk_num=chunk_info.current,
            total_chunks=chunk_info.total
        )
        return f"\n\n{separator}\n{header}\n{separator}\n\n"
    
    def _format_section(self, title: str, content: str) -> str:
        """Format a section with title."""
        return f"## {title}\n\n{content}"
    
    def _format_content_section(self, header: str, content: str) -> str:
        """Format the main content section."""
        return f"{SECTION_DIVIDER}\n\n{header}\n\n{content}"
    
    def _get_content_header(self, chunk_info: Optional[ChunkInfo]) -> str:
        """Get appropriate header for content."""
        if chunk_info and not chunk_info.is_single:
            return CHUNK_HEADER_FORMAT.format(
                chunk_num=chunk_info.current,
                total_chunks=chunk_info.total
            )
        return SINGLE_HEADER_FORMAT
    
    def _join_sections(self, sections: List[str]) -> str:
        """Join sections with appropriate spacing."""
        return "\n\n".join(filter(None, sections))