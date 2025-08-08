"""Application services for separating concerns."""

from typing import Optional
from pathlib import Path

from ..domain.entities import Document, ProcessingSession, FormattingContext
from ..domain.value_objects import FilePath, ProcessingResult
from ..infrastructure.exceptions import FileOperationError, ValidationError
from .ports import FileSystemPort, ContextPersistencePort


class DocumentLoader:
    """Service for loading and validating documents."""
    
    def __init__(self, file_system: FileSystemPort):
        self.file_system = file_system
    
    def load_formatting_prompt(self, prompt_file: FilePath) -> str:
        """Load and validate formatting prompt."""
        prompt = self.file_system.read_file(str(prompt_file))
        
        if not prompt:
            raise FileOperationError.file_not_found(str(prompt_file))
        
        if not prompt.strip():
            raise ValidationError.empty_content("Formatting prompt")
        
        return prompt
    
    def load_document(self, message_file: FilePath) -> Document:
        """Load and create document from file."""
        content = self.file_system.read_file(str(message_file))
        
        if not content:
            raise FileOperationError.file_not_found(str(message_file))
        
        if not content.strip():
            raise ValidationError.empty_content("Document content")
        
        return Document.from_content(content, str(message_file))


class SessionManager:
    """Service for managing processing sessions and context."""
    
    def __init__(self, context_persistence: ContextPersistencePort):
        self.context_persistence = context_persistence
    
    def load_context(self) -> Optional[FormattingContext]:
        """Load formatting context with error handling."""
        try:
            return self.context_persistence.load_context()
        except Exception as e:
            # Log error but don't fail - context is optional
            print(f"Warning: Could not load context: {e}")
            return None
    
    def save_session(
        self,
        context: FormattingContext,
        session: ProcessingSession
    ) -> None:
        """Save session to context."""
        context.add_session(session)
        self.context_persistence.save_context(context)
    
    def create_new_session(
        self,
        document: Document,
        formatting_prompt: str
    ) -> ProcessingSession:
        """Create new processing session."""
        return ProcessingSession.create_new(document, formatting_prompt)


class OutputWriter:
    """Service for managing output file operations."""
    
    def __init__(self, file_system: FileSystemPort):
        self.file_system = file_system
    
    def prepare_output_file(self, output_file: FilePath) -> None:
        """Prepare output file for writing."""
        self.file_system.clear_file(str(output_file))
    
    def write_chunk(
        self,
        output_file: FilePath,
        content: str,
        append: bool = False
    ) -> None:
        """Write chunk to output file."""
        self.file_system.write_file(str(output_file), content, append)
    
    def finalize_output(self, output_file: FilePath) -> ProcessingResult:
        """Finalize and verify output."""
        # Verify file was written
        if not Path(str(output_file)).exists():
            return ProcessingResult.error_result(
                f"Output file was not created: {output_file}"
            )
        
        # Read preview
        content = self.file_system.read_file(str(output_file))
        preview = content[:300] + "..." if len(content) > 300 else content
        
        return ProcessingResult.success_result(
            message=f"Output saved to {output_file}",
            preview=preview
        )


class ProgressTracker:
    """Service for tracking and reporting progress."""
    
    def __init__(self):
        self.current_step = ""
        self.total_steps = 0
        self.completed_steps = 0
    
    def start_tracking(self, total_steps: int) -> None:
        """Start tracking progress."""
        self.total_steps = total_steps
        self.completed_steps = 0
    
    def update_step(self, step_name: str) -> None:
        """Update current step."""
        self.current_step = step_name
        self.completed_steps += 1
    
    def get_progress_percentage(self) -> float:
        """Get progress percentage."""
        if self.total_steps == 0:
            return 0.0
        return (self.completed_steps / self.total_steps) * 100
    
    def get_status(self) -> dict:
        """Get current status."""
        return {
            "current_step": self.current_step,
            "completed": self.completed_steps,
            "total": self.total_steps,
            "percentage": self.get_progress_percentage()
        }