"""Formatting context entity for managing processing history."""

from dataclasses import dataclass, field
from typing import List

from ..value_objects import WordCount
from ..constants import MAX_SESSION_HISTORY, MAX_RECENT_SESSIONS
from .processing_session import ProcessingSession


@dataclass
class FormattingContext:
    """Context for formatting operations with history management."""
    session_history: List[ProcessingSession] = field(default_factory=list)
    custom_instructions: str = ""
    conversation_summary: str = ""
    max_history_size: int = MAX_SESSION_HISTORY
    
    def add_session(self, session: ProcessingSession) -> None:
        """Add session to history with size management."""
        self.session_history.append(session)
        self._trim_history()
    
    def _trim_history(self) -> None:
        """Keep history within size limit."""
        if len(self.session_history) > self.max_history_size:
            self.session_history = self.session_history[-self.max_history_size:]
    
    def get_recent_sessions(self, limit: int = MAX_RECENT_SESSIONS) -> List[ProcessingSession]:
        """Get most recent sessions."""
        return self.session_history[-limit:] if self.session_history else []
    
    def has_custom_instructions(self) -> bool:
        """Check if custom instructions are set."""
        return bool(self.custom_instructions)
    
    def has_conversation_summary(self) -> bool:
        """Check if conversation summary exists."""
        return bool(self.conversation_summary)
    
    def get_total_words_processed(self) -> WordCount:
        """Get total words processed across all sessions."""
        total = sum(
            int(session.total_words_processed) 
            for session in self.session_history
        )
        return WordCount(total)
    
    def get_total_chunks_processed(self) -> int:
        """Get total chunks processed across all sessions."""
        return sum(session.total_chunks for session in self.session_history)
    
    def clear_history(self) -> None:
        """Clear session history."""
        self.session_history.clear()
    
    def __str__(self) -> str:
        return f"Context({len(self.session_history)} sessions)"