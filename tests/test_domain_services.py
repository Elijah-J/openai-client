"""Tests for domain services."""

import pytest
from src.domain.services import (
    TextChunkingService, EvenDistributionChunking, 
    PromptBuilder, ContextBuilder
)
from src.domain.entities import Document
from src.domain.value_objects import WordLimit, ChunkInfo


class TestTextChunkingService:
    """Test text chunking service."""
    
    def test_even_distribution_chunking(self):
        """Test even distribution chunking strategy."""
        service = TextChunkingService()
        doc = Document.from_content("word " * 500)  # 500 words
        word_limit = WordLimit(200)  # Valid word limit
        
        chunks = service.chunk_document(doc, word_limit)
        
        # Should create 3 chunks (500/200 = 2.5, rounded up to 3)
        assert len(chunks) == 3
        
        # Each chunk should have roughly 167 words
        for chunk in chunks:
            word_count = len(chunk.split())
            assert 150 <= word_count <= 200
    
    def test_no_chunking_needed(self):
        """Test when document doesn't need chunking."""
        service = TextChunkingService()
        content = "word " * 50  # 50 words
        doc = Document.from_content(content)
        word_limit = WordLimit(100)
        
        chunks = service.chunk_document(doc, word_limit)
        
        assert len(chunks) == 1
        assert chunks[0] == content
    
    def test_calculate_chunks_needed(self):
        """Test chunk calculation."""
        service = TextChunkingService()
        doc = Document.from_content("word " * 500)  # 500 words
        word_limit = WordLimit(100)
        
        chunks_needed = service.calculate_chunks_needed(doc, word_limit)
        assert chunks_needed == 5


class TestPromptBuilder:
    """Test prompt builder service."""
    
    def test_build_simple_prompt(self):
        """Test building simple prompt."""
        builder = PromptBuilder()
        
        prompt = builder.build_formatting_prompt(
            instructions="Format this",
            content="Test content"
        )
        
        assert "Format this" in prompt
        assert "Test content" in prompt
        assert "# Text to Format:" in prompt
    
    def test_build_prompt_with_context(self):
        """Test building prompt with context."""
        builder = PromptBuilder()
        
        prompt = builder.build_formatting_prompt(
            instructions="Format this",
            content="Test content",
            context="Previous context"
        )
        
        assert "Previous context" in prompt
        assert prompt.startswith("## Context")
    
    def test_build_prompt_with_chunk_info(self):
        """Test building prompt with chunk information."""
        builder = PromptBuilder()
        chunk_info = ChunkInfo(2, 5)
        
        prompt = builder.build_formatting_prompt(
            instructions="Format this",
            content="Chunk content",
            chunk_info=chunk_info
        )
        
        assert "Part 2 of 5" in prompt
    
    def test_build_continuation_header(self):
        """Test building continuation header."""
        builder = PromptBuilder()
        chunk_info = ChunkInfo(3, 5)
        
        header = builder.build_continuation_header(chunk_info)
        
        assert "CONTINUATION" in header
        assert "Part 3 of 5" in header
        assert "=" * 60 in header


class TestContextBuilder:
    """Test context builder service."""
    
    def test_build_empty_context(self):
        """Test building empty context."""
        builder = ContextBuilder()
        
        context = builder.build_context_prompt()
        assert context == ""
    
    def test_build_context_with_summary(self):
        """Test building context with conversation summary."""
        builder = ContextBuilder()
        
        context = builder.build_context_prompt(
            conversation_summary="Previous discussion about formatting"
        )
        
        assert "Previous conversation: Previous discussion about formatting" in context
    
    def test_build_context_with_instructions(self):
        """Test building context with custom instructions."""
        builder = ContextBuilder()
        
        context = builder.build_context_prompt(
            custom_instructions="Use British spelling"
        )
        
        assert "Custom instructions: Use British spelling" in context
    
    def test_build_full_context(self):
        """Test building complete context."""
        builder = ContextBuilder()
        
        # Create mock sessions
        class MockSession:
            def get_summary(self):
                return "test.md: 100 words"
        
        sessions = [MockSession(), MockSession()]
        
        context = builder.build_context_prompt(
            conversation_summary="Previous work",
            custom_instructions="Be formal",
            recent_sessions=sessions
        )
        
        assert "Previous conversation: Previous work" in context
        assert "Custom instructions: Be formal" in context
        assert "Recent processing:" in context
        assert "test.md: 100 words" in context