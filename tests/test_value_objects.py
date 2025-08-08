"""Tests for domain value objects."""

import pytest
from src.domain.value_objects import (
    WordCount, WordLimit, ChunkInfo, FilePath, SessionId, ProcessingResult
)


class TestWordCount:
    """Test WordCount value object."""
    
    def test_valid_word_count(self):
        wc = WordCount(100)
        assert int(wc) == 100
        assert str(wc) == "100"
    
    def test_large_word_count_formatting(self):
        wc = WordCount(1500)
        assert str(wc) == "1,500"
    
    def test_negative_word_count_raises_error(self):
        with pytest.raises(ValueError, match="cannot be negative"):
            WordCount(-1)
    
    def test_exceeds_limit(self):
        wc = WordCount(2500)
        assert wc.exceeds_limit(2000) is True
        assert wc.exceeds_limit(3000) is False


class TestWordLimit:
    """Test WordLimit value object."""
    
    def test_valid_word_limit(self):
        wl = WordLimit(2000)
        assert int(wl) == 2000
    
    def test_word_limit_too_small(self):
        with pytest.raises(ValueError, match="must be between"):
            WordLimit(50)
    
    def test_word_limit_too_large(self):
        with pytest.raises(ValueError, match="must be between"):
            WordLimit(15000)


class TestChunkInfo:
    """Test ChunkInfo value object."""
    
    def test_valid_chunk_info(self):
        ci = ChunkInfo(2, 5)
        assert ci.current == 2
        assert ci.total == 5
        assert str(ci) == "2/5"
    
    def test_is_first(self):
        ci = ChunkInfo(1, 5)
        assert ci.is_first is True
        assert ci.is_last is False
    
    def test_is_last(self):
        ci = ChunkInfo(5, 5)
        assert ci.is_first is False
        assert ci.is_last is True
    
    def test_is_single(self):
        ci = ChunkInfo(1, 1)
        assert ci.is_single is True
        assert ci.is_first is True
        assert ci.is_last is True
    
    def test_invalid_chunk_info(self):
        with pytest.raises(ValueError):
            ChunkInfo(0, 5)  # Current < 1
        
        with pytest.raises(ValueError):
            ChunkInfo(6, 5)  # Current > total
        
        with pytest.raises(ValueError):
            ChunkInfo(1, 0)  # Total < 1


class TestFilePath:
    """Test FilePath value object."""
    
    def test_valid_file_path(self):
        fp = FilePath("test.txt")
        assert str(fp) == "test.txt"
        assert fp.name == "test.txt"
    
    def test_empty_path_raises_error(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            FilePath("")
    
    def test_must_exist_validation(self, tmp_path):
        # Create temp file
        test_file = tmp_path / "exists.txt"
        test_file.write_text("test")
        
        # Should succeed with existing file
        fp = FilePath(str(test_file), must_exist=True)
        assert fp.exists is True
        
        # Should fail with non-existing file
        with pytest.raises(ValueError, match="does not exist"):
            FilePath("nonexistent.txt", must_exist=True)


class TestSessionId:
    """Test SessionId value object."""
    
    def test_valid_session_id(self):
        sid = SessionId("12345678-abcd-efgh-ijkl")
        assert str(sid) == "12345678-abcd-efgh-ijkl"
        assert sid.short == "12345678..."
    
    def test_empty_session_id_raises_error(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            SessionId("")
    
    def test_short_session_id_raises_error(self):
        with pytest.raises(ValueError, match="too short"):
            SessionId("123")


class TestProcessingResult:
    """Test ProcessingResult value object."""
    
    def test_success_result(self):
        result = ProcessingResult.success_result("Operation completed", "Preview text")
        assert result.success is True
        assert result.message == "Operation completed"
        assert result.preview == "Preview text"
        assert result.error is None
    
    def test_error_result(self):
        result = ProcessingResult.error_result("Something went wrong")
        assert result.success is False
        assert result.message == "Processing failed"
        assert result.error == "Something went wrong"
        assert result.preview is None