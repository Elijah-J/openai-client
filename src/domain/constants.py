"""Domain constants and configuration values."""

# Document processing constants
DEFAULT_WORD_LIMIT = 2000  # Back to original for proper chunking
MIN_WORD_LIMIT = 100
MAX_WORD_LIMIT = 10000

# Display constants
PREVIEW_LENGTH = 300
SEPARATOR_WIDTH = 60
SECTION_SEPARATOR_CHAR = "-"
SECTION_SEPARATOR_WIDTH = 50
SECTION_SEPARATOR = SECTION_SEPARATOR_CHAR * SECTION_SEPARATOR_WIDTH
HEADER_SEPARATOR = "=" * SEPARATOR_WIDTH

# Context management constants
MAX_SESSION_HISTORY = 10
MAX_RECENT_SESSIONS = 3
MAX_PROMPT_STORAGE_LENGTH = 500
MAX_CONTEXT_LENGTH = 2000
MIN_API_KEY_DISPLAY_LENGTH = 8

# Retry and backoff constants
RETRY_BASE_WAIT = 2.0
RETRY_BASE_WAIT_RATE_LIMIT = 5.0
RETRY_MAX_WAIT = 60.0
RETRY_MAX_WAIT_RATE_LIMIT = 120.0
RETRY_BACKOFF_MULTIPLIER = 2
RETRY_TIMEOUT_MULTIPLIER = 0.5
RETRY_JITTER_FACTOR = 0.1

# Formatting constants
MAX_DISPLAY_NUMBER = 999
JSON_INDENT_SPACES = 2

# Validation constants
MIN_CHUNK_NUMBER = 1
MIN_TOTAL_CHUNKS = 1
MIN_WORD_COUNT = 0

# Terminal color codes
ANSI_COLOR_RED = '\033[91m'
ANSI_COLOR_GREEN = '\033[92m'
ANSI_COLOR_BLUE = '\033[94m'
ANSI_COLOR_RESET = '\033[0m'

# File paths (defaults)
DEFAULT_DATA_DIR = "data"
DEFAULT_PROMPT_FILE = "prompt.md"
DEFAULT_MESSAGE_FILE = "message.md"
DEFAULT_OUTPUT_FILE = "output.md"
DEFAULT_CONTEXT_FILE = "context.json"

# API constants
DEFAULT_MODEL = "gpt-4"
API_TIMEOUT_SECONDS = 300  # Increased from 30 to handle slower responses
MAX_RETRY_ATTEMPTS = 3

# Formatting constants
CHUNK_HEADER_FORMAT = "# Text to Format (Part {chunk_num} of {total_chunks}):"
SINGLE_HEADER_FORMAT = "# Text to Format:"
CONTINUATION_HEADER_FORMAT = "# CONTINUATION (Part {chunk_num} of {total_chunks})"
SECTION_DIVIDER = "---"

# Continuity settings
ENABLE_CONTINUITY_INSTRUCTIONS = True
CONTINUITY_STYLE_EMPHASIS = True

# Progress messages
PROGRESS_CONTEXT_LOADED = "Context loaded"
PROGRESS_DOCUMENT_ANALYSIS = "Document analysis"
PROGRESS_CHUNK_PROCESSING = "Processing chunk {chunk_num}/{total_chunks}"
PROGRESS_CONTEXT_UPDATED = "Context updated"

# Error messages
ERROR_NO_PROMPT = "No formatting prompt found in {file}"
ERROR_NO_CONTENT = "No content found in {file}"
ERROR_API_FAILURE = "API error: {error}"
ERROR_FILE_READ = "Failed to read {path}: {error}"
ERROR_FILE_WRITE = "Failed to write to {path}: {error}"
ERROR_INVALID_WORD_LIMIT = "Word limit must be between {min} and {max}"