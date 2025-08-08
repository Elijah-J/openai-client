"""Tests for prompt continuity functionality."""

import pytest
from src.domain.prompt_continuity import ContinuityInstructions, ContinuousPromptBuilder
from src.domain.services import PromptBuilder
from src.domain.value_objects import ChunkInfo


class TestContinuityInstructions:
    """Test continuity instruction generation."""
    
    def test_single_chunk_no_instructions(self):
        """Test that single chunks get no continuity instructions."""
        chunk_info = ChunkInfo(1, 1)
        instructions = ContinuityInstructions.get_chunk_instructions(chunk_info)
        
        assert instructions == ""
    
    def test_first_chunk_instructions(self):
        """Test instructions for first chunk."""
        chunk_info = ChunkInfo(1, 3)
        instructions = ContinuityInstructions.get_chunk_instructions(chunk_info)
        
        assert "part 1 of 3" in instructions
        assert "Begin formatting from the very first word" in instructions
        assert "Establish a consistent style" in instructions
        assert "NOT add conclusions" in instructions
        assert "concatenated with the next parts" in instructions
    
    def test_middle_chunk_instructions(self):
        """Test instructions for middle chunks."""
        chunk_info = ChunkInfo(2, 4)
        instructions = ContinuityInstructions.get_chunk_instructions(chunk_info)
        
        assert "part 2 of 4" in instructions
        assert "Continue EXACTLY where the previous part left off" in instructions
        assert "Start mid-sentence if that's where the text begins" in instructions
        assert "SAME style, tone, and formatting" in instructions
        assert "directly appended to the previous part" in instructions
    
    def test_last_chunk_instructions(self):
        """Test instructions for last chunk."""
        chunk_info = ChunkInfo(3, 3)
        instructions = ContinuityInstructions.get_chunk_instructions(chunk_info)
        
        assert "final part (3 of 3)" in instructions
        assert "Continue EXACTLY where the previous part left off" in instructions
        assert "Complete the document naturally" in instructions
        assert "NOT reference that this was a multi-part" in instructions


class TestContinuousPromptBuilder:
    """Test continuous prompt builder."""
    
    def test_single_chunk_uses_base_builder(self):
        """Test that single chunks use base builder without modifications."""
        base_builder = PromptBuilder()
        continuous_builder = ContinuousPromptBuilder(base_builder)
        
        chunk_info = ChunkInfo(1, 1)
        prompt = continuous_builder.build_formatting_prompt(
            instructions="Format this",
            content="Test content",
            chunk_info=chunk_info
        )
        
        # Should not contain continuity instructions
        assert "Important Continuity Instructions" not in prompt
        assert "Format this" in prompt
        assert "Test content" in prompt
    
    def test_multi_chunk_adds_continuity(self):
        """Test that multi-chunk processing adds continuity instructions."""
        base_builder = PromptBuilder()
        continuous_builder = ContinuousPromptBuilder(base_builder)
        
        # Test first chunk
        chunk_info = ChunkInfo(1, 3)
        prompt = continuous_builder.build_formatting_prompt(
            instructions="Original formatting instructions",
            content="First chunk content",
            chunk_info=chunk_info
        )
        
        assert "Original formatting instructions" in prompt
        assert "Important Continuity Instructions" in prompt
        assert "part 1 of 3" in prompt
        assert "First chunk content" in prompt
    
    def test_preserves_context_and_formatting(self):
        """Test that context and other formatting is preserved."""
        base_builder = PromptBuilder()
        continuous_builder = ContinuousPromptBuilder(base_builder)
        
        chunk_info = ChunkInfo(2, 3)
        prompt = continuous_builder.build_formatting_prompt(
            instructions="Format instructions",
            content="Middle chunk",
            context="Previous context info",
            chunk_info=chunk_info
        )
        
        # Should have all components
        assert "Previous context info" in prompt
        assert "Format instructions" in prompt
        assert "Important Continuity Instructions" in prompt
        assert "Middle chunk" in prompt
        assert "Part 2 of 3" in prompt
    
    def test_continuation_header_delegation(self):
        """Test that continuation header is delegated to base builder."""
        base_builder = PromptBuilder()
        continuous_builder = ContinuousPromptBuilder(base_builder)
        
        chunk_info = ChunkInfo(2, 3)
        header = continuous_builder.build_continuation_header(chunk_info)
        
        assert "CONTINUATION" in header
        assert "Part 2 of 3" in header
        assert "=" * 60 in header