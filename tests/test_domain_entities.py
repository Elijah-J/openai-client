"""Tests for domain entities."""

import pytest
from datetime import datetime
from src.domain.entities import Document, ProcessedChunk, ProcessingSession, FormattingContext
from src.domain.value_objects import WordCount, SessionId, ChunkInfo


class TestDocument:
    """Test Document entity."""
    
    def test_create_from_content(self):
        """Test creating document from content."""
        content = "This is test content with several words"
        doc = Document.from_content(content)
        
        assert doc.content == content
        assert int(doc.word_count) == 7
        assert doc.source_file is None
    
    def test_create_with_source_file(self):
        """Test creating document with source file."""
        doc = Document.from_content("Test content", "test.txt")
        
        assert str(doc.source_file) == "test.txt"
    
    def test_empty_content_raises_error(self):
        """Test that empty content raises error."""
        with pytest.raises(ValueError, match="cannot be empty"):
            Document.from_content("")
    
    def test_requires_chunking(self):
        """Test chunking requirement check."""
        doc = Document.from_content("word " * 100)  # 100 words
        
        assert doc.requires_chunking(50) is True
        assert doc.requires_chunking(200) is False


class TestProcessedChunk:
    """Test ProcessedChunk entity."""
    
    def test_create_chunk(self):
        """Test creating processed chunk."""
        chunk = ProcessedChunk.create("Chunk content", 2, 5)
        
        assert chunk.content == "Chunk content"
        assert chunk.chunk_info.current == 2
        assert chunk.chunk_info.total == 5
        assert int(chunk.word_count) == 2
    
    def test_needs_continuation_header(self):
        """Test continuation header requirement."""
        chunk1 = ProcessedChunk.create("First", 1, 3)
        chunk2 = ProcessedChunk.create("Second", 2, 3)
        
        assert chunk1.needs_continuation_header is False
        assert chunk2.needs_continuation_header is True


class TestProcessingSession:
    """Test ProcessingSession entity."""
    
    def test_create_new_session(self):
        """Test creating new session."""
        doc = Document.from_content("Test content")
        session = ProcessingSession.create_new(doc, "Format this")
        
        assert session.document == doc
        assert session.formatting_prompt == "Format this"
        assert session.is_completed is False
        assert len(session.chunks) == 0
    
    def test_add_chunks(self):
        """Test adding chunks to session."""
        doc = Document.from_content("Test content")
        session = ProcessingSession.create_new(doc, "Format")
        
        chunk1 = ProcessedChunk.create("Chunk 1", 1, 2)
        chunk2 = ProcessedChunk.create("Chunk 2", 2, 2)
        
        session.add_chunk(chunk1)
        session.add_chunk(chunk2)
        
        assert session.total_chunks == 2
        assert session.is_chunked is True
    
    def test_complete_session(self):
        """Test completing session."""
        doc = Document.from_content("Test")
        session = ProcessingSession.create_new(doc, "Format")
        
        assert session.is_completed is False
        
        session.complete()
        
        assert session.is_completed is True
        assert session.completed_at is not None
        assert session.processing_duration is not None
    
    def test_session_summary(self):
        """Test getting session summary."""
        doc = Document.from_content("word " * 100, "test.md")
        session = ProcessingSession.create_new(doc, "Format")
        
        chunk = ProcessedChunk.create("Formatted", 1, 1)
        session.add_chunk(chunk)
        
        summary = session.get_summary()
        assert "test.md" in summary
        assert "100 words" in summary


class TestFormattingContext:
    """Test FormattingContext entity."""
    
    def test_create_context(self):
        """Test creating formatting context."""
        context = FormattingContext()
        
        assert len(context.session_history) == 0
        assert context.custom_instructions == ""
        assert context.conversation_summary == ""
    
    def test_add_session(self):
        """Test adding session to context."""
        context = FormattingContext()
        doc = Document.from_content("Test")
        session = ProcessingSession.create_new(doc, "Format")
        
        context.add_session(session)
        
        assert len(context.session_history) == 1
        assert context.session_history[0] == session
    
    def test_history_size_limit(self):
        """Test that history is trimmed to max size."""
        context = FormattingContext(max_history_size=3)
        
        # Add 5 sessions
        for i in range(5):
            doc = Document.from_content(f"Test {i}")
            session = ProcessingSession.create_new(doc, "Format")
            context.add_session(session)
        
        # Should only keep last 3
        assert len(context.session_history) == 3
        # Should have sessions 2, 3, 4 (0 and 1 were trimmed)
        assert "Test 2" in context.session_history[0].document.content
    
    def test_get_recent_sessions(self):
        """Test getting recent sessions."""
        context = FormattingContext()
        
        # Add 5 sessions
        for i in range(5):
            doc = Document.from_content(f"Test {i}")
            session = ProcessingSession.create_new(doc, "Format")
            context.add_session(session)
        
        recent = context.get_recent_sessions(2)
        assert len(recent) == 2
        assert "Test 4" in recent[-1].document.content
    
    def test_total_statistics(self):
        """Test getting total statistics."""
        context = FormattingContext()
        
        # Add sessions with chunks
        for i in range(3):
            doc = Document.from_content("word " * 50)
            session = ProcessingSession.create_new(doc, "Format")
            chunk = ProcessedChunk.create("Formatted", 1, 1)
            session.add_chunk(chunk)
            context.add_session(session)
        
        total_words = context.get_total_words_processed()
        total_chunks = context.get_total_chunks_processed()
        
        assert int(total_words) == 3  # 3 sessions, 1 word each in formatted chunk
        assert total_chunks == 3  # 3 sessions, 1 chunk each