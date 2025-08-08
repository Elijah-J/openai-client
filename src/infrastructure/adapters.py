"""Refactored infrastructure adapters with better error handling and type safety."""

import json
import sys
import os
import time
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

from openai import OpenAI

from ..application.ports import (
    TextFormatterPort, FileSystemPort, ContextPersistencePort,
    UserInterfacePort, ConfigurationPort
)
from ..domain.entities import FormattingContext, ProcessingSession
from ..domain.value_objects import FilePath, WordLimit
from ..domain.constants import (
    DEFAULT_MODEL, API_TIMEOUT_SECONDS, MAX_RETRY_ATTEMPTS,
    HEADER_SEPARATOR, SECTION_SEPARATOR,
    DEFAULT_WORD_LIMIT, DEFAULT_PROMPT_FILE,
    DEFAULT_MESSAGE_FILE, DEFAULT_OUTPUT_FILE
)
from .exceptions import (
    APIError, FileOperationError, ProcessingError
)


class OpenAIAdapter(TextFormatterPort):
    """OpenAI API adapter with enhanced error handling."""
    
    def __init__(self, model: str = DEFAULT_MODEL, timeout: int = API_TIMEOUT_SECONDS, max_retries: int = MAX_RETRY_ATTEMPTS):
        """Initialize with model and timeout configuration."""
        self.model = model
        self.timeout = timeout
        self.max_retries = max_retries
        self.client = self._initialize_client()
    
    def _initialize_client(self) -> OpenAI:
        """Initialize OpenAI client with validation and increased timeout."""
        if not os.getenv('OPENAI_API_KEY'):
            raise APIError.authentication_error("OpenAI")
        
        return OpenAI(
            timeout=self.timeout,
            max_retries=0  # We handle retries ourselves
        )
    
    def format_text(self, prompt: str) -> str:
        """Format text using OpenAI API with retry logic and comprehensive error handling."""
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                response = self._make_api_call_with_backoff(prompt, attempt)
                return self._extract_response(response)
                
            except Exception as e:
                last_error = e
                error_str = str(e).lower()
                
                # Don't retry on authentication errors
                if "authentication" in error_str or "api key" in error_str:
                    raise APIError.authentication_error("OpenAI")
                
                # Don't retry on invalid request errors
                if "invalid" in error_str and "request" in error_str:
                    raise APIError.invalid_response("OpenAI", str(e))
                
                # Check for specific error types
                if "timeout" in error_str or "timed out" in error_str:
                    if attempt < self.max_retries - 1:
                        wait_time = self._calculate_backoff(attempt)
                        print(f"[INFO] Request timed out. Retrying in {wait_time:.1f} seconds... (Attempt {attempt + 2}/{self.max_retries})")
                        time.sleep(wait_time)
                        continue
                    else:
                        raise APIError.timeout_error("OpenAI", self.timeout)
                
                if "rate_limit" in error_str or "rate limit" in error_str:
                    if attempt < self.max_retries - 1:
                        wait_time = self._calculate_backoff(attempt, is_rate_limit=True)
                        print(f"[INFO] Rate limited. Waiting {wait_time:.1f} seconds before retry... (Attempt {attempt + 2}/{self.max_retries})")
                        time.sleep(wait_time)
                        continue
                    else:
                        raise APIError.rate_limit_error("OpenAI")
                
                if "connection" in error_str or "network" in error_str:
                    if attempt < self.max_retries - 1:
                        wait_time = self._calculate_backoff(attempt)
                        print(f"[INFO] Connection error. Retrying in {wait_time:.1f} seconds... (Attempt {attempt + 2}/{self.max_retries})")
                        time.sleep(wait_time)
                        continue
                    else:
                        raise APIError.connection_error("OpenAI", e)
                
                # For other errors, retry with backoff
                if attempt < self.max_retries - 1:
                    wait_time = self._calculate_backoff(attempt)
                    print(f"[INFO] API error occurred. Retrying in {wait_time:.1f} seconds... (Attempt {attempt + 2}/{self.max_retries})")
                    time.sleep(wait_time)
                    continue
        
        # If all retries failed, raise the last error
        if last_error:
            raise APIError.invalid_response("OpenAI", str(last_error))
        else:
            raise APIError.invalid_response("OpenAI", "Failed after all retry attempts")
    
    def _make_api_call_with_backoff(self, prompt: str, attempt: int) -> Any:
        """Make API call with dynamic timeout based on attempt number."""
        # Increase timeout with each retry
        from ..domain.constants import RETRY_TIMEOUT_MULTIPLIER
        adjusted_timeout = self.timeout * (1 + attempt * RETRY_TIMEOUT_MULTIPLIER)
        
        # No truncation - send full prompt to GPT-5
        
        # Use chat completions API with optimized settings
        # Note: GPT-5 may have different requirements
        try:
            # Try without system message and max_completion_tokens for GPT-5
            return self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                timeout=adjusted_timeout
            )
        except Exception as e:
            # If that fails, try with minimal parameters
            if "max_completion_tokens" in str(e) or "system" in str(e):
                return self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    timeout=adjusted_timeout
                )
            raise e
    
    def _calculate_backoff(self, attempt: int, is_rate_limit: bool = False) -> float:
        """Calculate exponential backoff with jitter."""
        from ..domain.constants import (
            RETRY_BASE_WAIT, RETRY_BASE_WAIT_RATE_LIMIT,
            RETRY_MAX_WAIT, RETRY_MAX_WAIT_RATE_LIMIT,
            RETRY_BACKOFF_MULTIPLIER, RETRY_JITTER_FACTOR
        )
        
        base_wait = RETRY_BASE_WAIT_RATE_LIMIT if is_rate_limit else RETRY_BASE_WAIT
        max_wait = RETRY_MAX_WAIT_RATE_LIMIT if is_rate_limit else RETRY_MAX_WAIT
        
        # Exponential backoff: multiplier^attempt * base_wait
        wait_time = min(base_wait * (RETRY_BACKOFF_MULTIPLIER ** attempt), max_wait)
        
        # Add jitter to prevent thundering herd
        import random
        jitter = random.uniform(0, wait_time * RETRY_JITTER_FACTOR)
        
        return wait_time + jitter
    
    def _extract_response(self, response: Any) -> str:
        """Extract text from API response with multiple strategies."""
        # Strategy 1: Chat completion response (most common)
        if hasattr(response, 'choices') and response.choices:
            for choice in response.choices:
                if hasattr(choice, 'message') and hasattr(choice.message, 'content'):
                    content = choice.message.content
                    if content:
                        return content.strip()
        
        # Strategy 2: Direct attribute
        if hasattr(response, 'output_text') and response.output_text:
            return response.output_text
        
        # Strategy 3: Output array
        if hasattr(response, 'output') and response.output:
            text_parts = self._extract_from_output_array(response.output)
            if text_parts:
                return ''.join(text_parts)
        
        # Strategy 4: String conversion
        result = str(response)
        if not result or result == str(type(response)):
            raise APIError.invalid_response(
                "OpenAI",
                "Could not extract text from response"
            )
        
        return result
    
    def _extract_from_output_array(self, output_items: list) -> list:
        """Extract text parts from output array."""
        return [
            getattr(item, 'content', '')
            for item in output_items
            if getattr(item, 'type', '') == 'output_text'
        ]


class FileSystemAdapter(FileSystemPort):
    """File system adapter with enhanced error handling."""
    
    def read_file(self, path: str) -> Optional[str]:
        """Read file with comprehensive error handling."""
        file_path = Path(path)
        
        if not file_path.exists():
            return None
        
        if not file_path.is_file():
            raise FileOperationError.invalid_path(
                str(path),
                "Path exists but is not a file"
            )
        
        try:
            return file_path.read_text(encoding='utf-8')
        except PermissionError:
            raise FileOperationError.permission_denied(str(path))
        except Exception as e:
            raise FileOperationError.read_error(str(path), e)
    
    def write_file(self, path: str, content: str, append: bool = False) -> None:
        """Write file with proper append handling."""
        file_path = Path(path)
        
        # Create parent directory if needed
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            if append and file_path.exists():
                existing = file_path.read_text(encoding='utf-8')
                if existing and not existing.endswith('\n'):
                    existing += '\n'
                content = existing + content
            
            file_path.write_text(content, encoding='utf-8')
            
        except PermissionError:
            raise FileOperationError.permission_denied(str(path))
        except Exception as e:
            raise FileOperationError.write_error(str(path), e)
    
    def clear_file(self, path: str) -> None:
        """Clear file content safely."""
        try:
            Path(path).write_text('', encoding='utf-8')
        except PermissionError:
            raise FileOperationError.permission_denied(str(path))
        except Exception as e:
            raise FileOperationError.write_error(str(path), e)


class JsonContextPersistence(ContextPersistencePort):
    """JSON-based context persistence with proper serialization."""
    
    def __init__(self, context_file: str = "data/context.json"):
        """Initialize with context file path."""
        self.context_file = Path(context_file)
        self.context_file.parent.mkdir(parents=True, exist_ok=True)
    
    def load_context(self) -> Optional[FormattingContext]:
        """Load context with error recovery."""
        if not self.context_file.exists():
            return FormattingContext()
        
        try:
            with open(self.context_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return self._deserialize_context(data)
            
        except json.JSONDecodeError:
            # Corrupted file - start fresh
            return FormattingContext()
        except Exception as e:
            raise ProcessingError.context_load_error(e)
    
    def save_context(self, context: FormattingContext) -> None:
        """Save context with atomic write."""
        try:
            data = self._serialize_context(context)
            
            # Write to temp file first
            temp_file = self.context_file.with_suffix('.tmp')
            from ..domain.constants import JSON_INDENT_SPACES
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=JSON_INDENT_SPACES, default=str)
            
            # Atomic rename
            temp_file.replace(self.context_file)
            
        except Exception as e:
            raise ProcessingError.context_save_error(e)
    
    def _serialize_context(self, context: FormattingContext) -> dict:
        """Serialize context to JSON-compatible dict."""
        return {
            'session_history': [
                self._serialize_session(s) for s in context.session_history
            ],
            'custom_instructions': context.custom_instructions,
            'conversation_summary': context.conversation_summary,
            'updated_at': datetime.now().isoformat()
        }
    
    def _serialize_session(self, session: ProcessingSession) -> dict:
        """Serialize session to dict."""
        return {
            'session_id': str(session.session_id),
            'created_at': session.created_at.isoformat(),
            'completed_at': session.completed_at.isoformat() if session.completed_at else None,
            'document': {
                'word_count': int(session.document.word_count),
                'source_file': str(session.document.source_file) if session.document.source_file else None
            },
            'total_chunks': session.total_chunks,
            'summary': session.get_summary()
        }
    
    def _deserialize_context(self, data: dict) -> FormattingContext:
        """Deserialize context from dict."""
        context = FormattingContext(
            custom_instructions=data.get('custom_instructions', ''),
            conversation_summary=data.get('conversation_summary', '')
        )
        
        # Note: We only deserialize session metadata, not full sessions
        # This is sufficient for context purposes
        
        return context


class ConsoleUI(UserInterfacePort):
    """Enhanced console UI with better formatting."""
    
    def __init__(self, verbose: bool = True, use_color: bool = True):
        """Initialize with display options."""
        self.verbose = verbose
        self.use_color = use_color and sys.platform != 'win32'
    
    def show_progress(self, message: str, details: Dict[str, Any] = None) -> None:
        """Show formatted progress message."""
        if not self.verbose:
            return
        
        prefix = self._format_prefix("[PROGRESS]", "blue")
        print(f"\n{prefix} {message}")
        
        if details:
            for key, value in details.items():
                formatted_value = self._format_value(value)
                print(f"  • {key}: {formatted_value}")
    
    def show_result(self, message: str, preview: str = None) -> None:
        """Show formatted result message."""
        print(f"\n{HEADER_SEPARATOR}")
        prefix = self._format_prefix("[SUCCESS]", "green")
        print(f"{prefix} {message}")
        
        if preview and self.verbose:
            print(SECTION_SEPARATOR)
            print(preview)
            
        print(HEADER_SEPARATOR)
    
    def show_error(self, error: str) -> None:
        """Show formatted error message."""
        prefix = self._format_prefix("[ERROR]", "red")
        print(f"\n{prefix} {error}", file=sys.stderr)
    
    def _format_prefix(self, text: str, color: str) -> str:
        """Format prefix with optional color."""
        if not self.use_color:
            return text
        
        from ..domain.constants import (
            ANSI_COLOR_RED, ANSI_COLOR_GREEN, 
            ANSI_COLOR_BLUE, ANSI_COLOR_RESET
        )
        colors = {
            'red': ANSI_COLOR_RED,
            'green': ANSI_COLOR_GREEN,
            'blue': ANSI_COLOR_BLUE,
            'reset': ANSI_COLOR_RESET
        }
        
        color_code = colors.get(color, '')
        reset = colors['reset'] if color_code else ''
        
        return f"{color_code}{text}{reset}"
    
    def _format_value(self, value: Any) -> str:
        """Format value for display."""
        if isinstance(value, bool):
            return "Yes" if value else "No"
        from ..domain.constants import MAX_DISPLAY_NUMBER
        if isinstance(value, int) and value > MAX_DISPLAY_NUMBER:
            return f"{value:,}"
        return str(value)


class Settings(ConfigurationPort):
    """Application settings with validation."""
    
    def __init__(
        self,
        word_limit: int = DEFAULT_WORD_LIMIT,
        output_file: str = f"data/{DEFAULT_OUTPUT_FILE}",
        prompt_file: str = f"data/{DEFAULT_PROMPT_FILE}",
        message_file: str = f"data/{DEFAULT_MESSAGE_FILE}",
        context_enabled: bool = True
    ):
        """Initialize with validated settings."""
        self.word_limit = WordLimit(word_limit)
        self.output_file = output_file
        self.prompt_file = prompt_file
        self.message_file = message_file
        self.context_enabled = context_enabled
    
    def get_word_limit(self) -> int:
        return int(self.word_limit)
    
    def get_output_file(self) -> str:
        return self.output_file
    
    def get_prompt_file(self) -> str:
        return self.prompt_file
    
    def get_message_file(self) -> str:
        return self.message_file
    
    def is_context_enabled(self) -> bool:
        return self.context_enabled