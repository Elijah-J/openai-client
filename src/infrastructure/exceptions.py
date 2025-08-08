"""Enhanced exception handling with specific error types and user-friendly messages."""

from typing import Optional, Dict, Any
from enum import Enum


class ErrorCode(Enum):
    """Error codes for categorizing exceptions."""
    # Configuration errors (1xxx)
    CONFIG_MISSING = 1001
    CONFIG_INVALID = 1002
    CONFIG_FILE_NOT_FOUND = 1003
    
    # File operation errors (2xxx)
    FILE_NOT_FOUND = 2001
    FILE_READ_ERROR = 2002
    FILE_WRITE_ERROR = 2003
    FILE_PERMISSION_DENIED = 2004
    
    # API errors (3xxx)
    API_CONNECTION_ERROR = 3001
    API_AUTHENTICATION_ERROR = 3002
    API_RATE_LIMIT = 3003
    API_INVALID_RESPONSE = 3004
    API_TIMEOUT = 3005
    
    # Validation errors (4xxx)
    VALIDATION_EMPTY_CONTENT = 4001
    VALIDATION_INVALID_WORD_LIMIT = 4002
    VALIDATION_INVALID_PATH = 4003
    VALIDATION_INVALID_FORMAT = 4004
    
    # Processing errors (5xxx)
    PROCESSING_FAILED = 5001
    PROCESSING_INTERRUPTED = 5002
    CONTEXT_LOAD_ERROR = 5003
    CONTEXT_SAVE_ERROR = 5004


class ApplicationError(Exception):
    """Enhanced base application error with error codes and context."""
    
    def __init__(
        self,
        message: str,
        error_code: ErrorCode,
        details: Optional[Dict[str, Any]] = None,
        cause: Optional[Exception] = None
    ):
        """Initialize with detailed error information."""
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        self.cause = cause
    
    def get_user_message(self) -> str:
        """Get user-friendly error message."""
        return f"Error {self.error_code.value}: {self.message}"
    
    def get_detailed_message(self) -> str:
        """Get detailed error message for logging."""
        parts = [self.get_user_message()]
        
        if self.details:
            details_str = ", ".join(f"{k}={v}" for k, v in self.details.items())
            parts.append(f"Details: {details_str}")
        
        if self.cause:
            parts.append(f"Caused by: {str(self.cause)}")
        
        return " | ".join(parts)
    
    def __str__(self) -> str:
        return self.get_user_message()


class ConfigurationError(ApplicationError):
    """Configuration-related errors."""
    
    @classmethod
    def missing_config(cls, config_name: str) -> 'ConfigurationError':
        """Factory method for missing configuration."""
        return cls(
            message=f"Required configuration '{config_name}' is missing",
            error_code=ErrorCode.CONFIG_MISSING,
            details={"config_name": config_name}
        )
    
    @classmethod
    def invalid_config(cls, config_name: str, reason: str) -> 'ConfigurationError':
        """Factory method for invalid configuration."""
        return cls(
            message=f"Configuration '{config_name}' is invalid: {reason}",
            error_code=ErrorCode.CONFIG_INVALID,
            details={"config_name": config_name, "reason": reason}
        )
    
    @classmethod
    def config_file_not_found(cls, file_path: str) -> 'ConfigurationError':
        """Factory method for missing config file."""
        return cls(
            message=f"Configuration file not found: {file_path}",
            error_code=ErrorCode.CONFIG_FILE_NOT_FOUND,
            details={"file_path": file_path}
        )


class FileOperationError(ApplicationError):
    """File operation errors."""
    
    @classmethod
    def file_not_found(cls, file_path: str) -> 'FileOperationError':
        """Factory method for file not found."""
        return cls(
            message=f"File not found: {file_path}",
            error_code=ErrorCode.FILE_NOT_FOUND,
            details={"file_path": file_path}
        )
    
    @classmethod
    def read_error(cls, file_path: str, cause: Exception) -> 'FileOperationError':
        """Factory method for file read error."""
        return cls(
            message=f"Failed to read file: {file_path}",
            error_code=ErrorCode.FILE_READ_ERROR,
            details={"file_path": file_path},
            cause=cause
        )
    
    @classmethod
    def write_error(cls, file_path: str, cause: Exception) -> 'FileOperationError':
        """Factory method for file write error."""
        return cls(
            message=f"Failed to write to file: {file_path}",
            error_code=ErrorCode.FILE_WRITE_ERROR,
            details={"file_path": file_path},
            cause=cause
        )
    
    @classmethod
    def permission_denied(cls, file_path: str) -> 'FileOperationError':
        """Factory method for permission denied."""
        return cls(
            message=f"Permission denied accessing file: {file_path}",
            error_code=ErrorCode.FILE_PERMISSION_DENIED,
            details={"file_path": file_path}
        )


class APIError(ApplicationError):
    """External API errors."""
    
    @classmethod
    def connection_error(cls, service: str, cause: Exception) -> 'APIError':
        """Factory method for connection error."""
        return cls(
            message=f"Failed to connect to {service}",
            error_code=ErrorCode.API_CONNECTION_ERROR,
            details={"service": service},
            cause=cause
        )
    
    @classmethod
    def authentication_error(cls, service: str) -> 'APIError':
        """Factory method for authentication error."""
        return cls(
            message=f"Authentication failed for {service}. Check your API key.",
            error_code=ErrorCode.API_AUTHENTICATION_ERROR,
            details={"service": service}
        )
    
    @classmethod
    def rate_limit_error(cls, service: str, retry_after: Optional[int] = None) -> 'APIError':
        """Factory method for rate limit error."""
        message = f"Rate limit exceeded for {service}"
        if retry_after:
            message += f". Retry after {retry_after} seconds."
        
        return cls(
            message=message,
            error_code=ErrorCode.API_RATE_LIMIT,
            details={"service": service, "retry_after": retry_after}
        )
    
    @classmethod
    def invalid_response(cls, service: str, reason: str) -> 'APIError':
        """Factory method for invalid API response."""
        return cls(
            message=f"Invalid response from {service}: {reason}",
            error_code=ErrorCode.API_INVALID_RESPONSE,
            details={"service": service, "reason": reason}
        )
    
    @classmethod
    def timeout_error(cls, service: str, timeout_seconds: int) -> 'APIError':
        """Factory method for timeout error."""
        return cls(
            message=f"Request to {service} timed out after {timeout_seconds} seconds",
            error_code=ErrorCode.API_TIMEOUT,
            details={"service": service, "timeout_seconds": timeout_seconds}
        )


class ValidationError(ApplicationError):
    """Validation errors."""
    
    @classmethod
    def empty_content(cls, field_name: str) -> 'ValidationError':
        """Factory method for empty content validation."""
        return cls(
            message=f"{field_name} cannot be empty",
            error_code=ErrorCode.VALIDATION_EMPTY_CONTENT,
            details={"field_name": field_name}
        )
    
    @classmethod
    def invalid_word_limit(cls, value: int, min_limit: int, max_limit: int) -> 'ValidationError':
        """Factory method for invalid word limit."""
        return cls(
            message=f"Word limit {value} is invalid. Must be between {min_limit} and {max_limit}",
            error_code=ErrorCode.VALIDATION_INVALID_WORD_LIMIT,
            details={"value": value, "min": min_limit, "max": max_limit}
        )
    
    @classmethod
    def invalid_path(cls, path: str, reason: str) -> 'ValidationError':
        """Factory method for invalid path."""
        return cls(
            message=f"Path '{path}' is invalid: {reason}",
            error_code=ErrorCode.VALIDATION_INVALID_PATH,
            details={"path": path, "reason": reason}
        )
    
    @classmethod
    def invalid_format(cls, field_name: str, expected_format: str) -> 'ValidationError':
        """Factory method for invalid format."""
        return cls(
            message=f"{field_name} has invalid format. Expected: {expected_format}",
            error_code=ErrorCode.VALIDATION_INVALID_FORMAT,
            details={"field_name": field_name, "expected_format": expected_format}
        )


class ProcessingError(ApplicationError):
    """Processing-related errors."""
    
    @classmethod
    def processing_failed(cls, step: str, reason: str) -> 'ProcessingError':
        """Factory method for processing failure."""
        return cls(
            message=f"Processing failed at step '{step}': {reason}",
            error_code=ErrorCode.PROCESSING_FAILED,
            details={"step": step, "reason": reason}
        )
    
    @classmethod
    def processing_interrupted(cls, step: str) -> 'ProcessingError':
        """Factory method for interrupted processing."""
        return cls(
            message=f"Processing was interrupted at step '{step}'",
            error_code=ErrorCode.PROCESSING_INTERRUPTED,
            details={"step": step}
        )
    
    @classmethod
    def context_load_error(cls, cause: Exception) -> 'ProcessingError':
        """Factory method for context load error."""
        return cls(
            message="Failed to load processing context",
            error_code=ErrorCode.CONTEXT_LOAD_ERROR,
            cause=cause
        )
    
    @classmethod
    def context_save_error(cls, cause: Exception) -> 'ProcessingError':
        """Factory method for context save error."""
        return cls(
            message="Failed to save processing context",
            error_code=ErrorCode.CONTEXT_SAVE_ERROR,
            cause=cause
        )