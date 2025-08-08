"""Service for building context prompts."""

from typing import List, Optional

from ..constants import SECTION_DIVIDER


class ContextBuilder:
    """Service for building context prompts."""
    
    def build_context_prompt(
        self,
        conversation_summary: Optional[str] = None,
        custom_instructions: Optional[str] = None,
        recent_sessions: Optional[List] = None
    ) -> str:
        """Build a well-structured context prompt."""
        sections = []
        
        if conversation_summary:
            sections.append(f"Previous conversation: {conversation_summary}")
        
        if custom_instructions:
            sections.append(f"Custom instructions: {custom_instructions}")
        
        if recent_sessions:
            history = self._format_session_history(recent_sessions)
            sections.append(history)
        
        if sections:
            return "\n\n".join(sections) + f"\n\n{SECTION_DIVIDER}\n\n"
        
        return ""
    
    def _format_session_history(self, sessions: List) -> str:
        """Format session history for context."""
        lines = ["Recent processing:"]
        for session in sessions:
            lines.append(f"  • {session.get_summary()}")
        return "\n".join(lines)