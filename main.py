#!/usr/bin/env python3
"""Clean, refactored main entry point."""

import sys
import os
from dotenv import load_dotenv

from src.infrastructure.dependency_injection import ApplicationFactory
from src.infrastructure.exceptions import ApplicationError


def validate_environment() -> bool:
    """Validate required environment variables."""
    if not os.getenv('OPENAI_API_KEY'):
        print("[ERROR] OPENAI_API_KEY not found in environment", file=sys.stderr)
        print("Please set it in your .env file or environment variables", file=sys.stderr)
        return False
    return True


def main() -> int:
    """Main application entry point with clean error handling."""
    # Load environment
    load_dotenv()
    
    # Validate environment
    if not validate_environment():
        return 1
    
    try:
        # Create and execute use case
        use_case = ApplicationFactory.create_default()
        result = use_case.execute()
        
        # Return appropriate exit code
        return 0 if result.success else 1
        
    except ApplicationError as e:
        # Handle application errors with detailed info
        print(e.get_detailed_message(), file=sys.stderr)
        return e.error_code.value // 1000  # Use error code category as exit code
        
    except KeyboardInterrupt:
        print("\n[INFO] Operation cancelled by user")
        return 130  # Standard exit code for SIGINT
        
    except Exception as e:
        # Unexpected errors
        print(f"[ERROR] Unexpected error: {str(e)}", file=sys.stderr)
        return 255


if __name__ == "__main__":
    sys.exit(main())