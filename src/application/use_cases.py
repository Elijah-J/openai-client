"""Refactored use cases with simplified methods and better separation."""

from typing import Optional, List
from datetime import datetime

from ..domain.entities import (
    Document, ProcessedChunk, ProcessingSession, FormattingContext
)
from ..domain.services import (
    TextChunkingService, PromptBuilder, ContextBuilder
)
from ..domain.prompt_continuity import ContinuousPromptBuilder
from ..domain.value_objects import (
    WordLimit, FilePath, ChunkInfo, ProcessingResult
)
from .services import (
    DocumentLoader, SessionManager, OutputWriter, ProgressTracker
)
from .ports import (
    TextFormatterPort, FileSystemPort, ContextPersistencePort,
    UserInterfacePort, ConfigurationPort
)


class FormatDocumentUseCase:
    """Simplified use case for formatting documents."""
    
    def __init__(
        self,
        text_formatter: TextFormatterPort,
        file_system: FileSystemPort,
        context_persistence: ContextPersistencePort,
        user_interface: UserInterfacePort,
        configuration: ConfigurationPort
    ):
        # Core dependencies
        self.text_formatter = text_formatter
        self.configuration = configuration
        self.user_interface = user_interface
        
        # Domain services
        self.chunking_service = TextChunkingService()
        base_prompt_builder = PromptBuilder()
        self.prompt_builder = ContinuousPromptBuilder(base_prompt_builder)
        self.context_builder = ContextBuilder()
        
        # Application services
        self.document_loader = DocumentLoader(file_system)
        self.session_manager = SessionManager(context_persistence)
        self.output_writer = OutputWriter(file_system)
        self.progress_tracker = ProgressTracker()
    
    def execute(self) -> ProcessingResult:
        """Execute document formatting workflow with simplified flow."""
        try:
            # Step 1: Load and validate inputs
            inputs = self._load_inputs()
            
            # Step 2: Process document
            session = self._process_document(inputs)
            
            # Step 3: Save results
            result = self._save_results(session, inputs.context)
            
            return result
            
        except Exception as e:
            self.user_interface.show_error(str(e))
            return ProcessingResult.error_result(str(e))
    
    def _load_inputs(self) -> 'ProcessingInputs':
        """Load all required inputs."""
        # Load files
        prompt_file = FilePath(self.configuration.get_prompt_file())
        message_file = FilePath(self.configuration.get_message_file())
        
        formatting_prompt = self.document_loader.load_formatting_prompt(prompt_file)
        document = self.document_loader.load_document(message_file)
        
        # Load context if enabled
        context = None
        if self.configuration.is_context_enabled():
            context = self.session_manager.load_context()
            if context:
                self._show_context_status(context)
        
        # Show analysis
        self._show_document_analysis(document)
        
        return ProcessingInputs(
            document=document,
            formatting_prompt=formatting_prompt,
            context=context
        )
    
    def _process_document(self, inputs: 'ProcessingInputs') -> ProcessingSession:
        """Process document with chunking if needed."""
        # Create session
        session = self.session_manager.create_new_session(
            inputs.document,
            inputs.formatting_prompt
        )
        
        # Prepare output
        output_file = FilePath(self.configuration.get_output_file())
        self.output_writer.prepare_output_file(output_file)
        
        # Get chunks
        word_limit = WordLimit(self.configuration.get_word_limit())
        chunks = self.chunking_service.chunk_document(inputs.document, word_limit)
        
        # Process each chunk
        context_prompt = self._build_context_prompt(inputs.context)
        
        for i, chunk_content in enumerate(chunks, 1):
            chunk_info = ChunkInfo(i, len(chunks))
            processed_chunk = self._process_single_chunk(
                chunk_content,
                chunk_info,
                inputs.formatting_prompt,
                context_prompt,
                output_file
            )
            session.add_chunk(processed_chunk)
        
        session.complete()
        return session
    
    def _process_single_chunk(
        self,
        content: str,
        chunk_info: ChunkInfo,
        formatting_prompt: str,
        context_prompt: str,
        output_file: FilePath
    ) -> ProcessedChunk:
        """Process a single chunk of text."""
        # Show progress
        self.user_interface.show_progress(
            f"Processing chunk {chunk_info}",
            {"words": len(content.split())}
        )
        
        # Build prompt (context only for first chunk)
        context_to_use = context_prompt if chunk_info.is_first else None
        prompt = self.prompt_builder.build_formatting_prompt(
            instructions=formatting_prompt,
            content=content,
            context=context_to_use,
            chunk_info=chunk_info if not chunk_info.is_single else None
        )
        
        # Format text
        formatted = self.text_formatter.format_text(prompt)
        
        # Add continuation header if needed
        if chunk_info.needs_continuation_header:
            header = self.prompt_builder.build_continuation_header(chunk_info)
            formatted = header + formatted
        
        # Write to file
        self.output_writer.write_chunk(
            output_file,
            formatted,
            append=not chunk_info.is_first
        )
        
        return ProcessedChunk.create(formatted, chunk_info.current, chunk_info.total)
    
    def _save_results(
        self,
        session: ProcessingSession,
        context: Optional[FormattingContext]
    ) -> ProcessingResult:
        """Save processing results and update context."""
        # Update context if enabled
        if self.configuration.is_context_enabled() and context:
            self.session_manager.save_session(context, session)
            self.user_interface.show_progress(
                "Context updated",
                {"sessions": len(context.session_history)}
            )
        
        # Finalize output
        output_file = FilePath(self.configuration.get_output_file())
        result = self.output_writer.finalize_output(output_file)
        
        # Show completion
        self.user_interface.show_result(
            result.message,
            preview=result.preview
        )
        
        return result
    
    def _build_context_prompt(
        self,
        context: Optional[FormattingContext]
    ) -> str:
        """Build context prompt if context exists."""
        if not context:
            return ""
        
        return self.context_builder.build_context_prompt(
            conversation_summary=context.conversation_summary,
            custom_instructions=context.custom_instructions,
            recent_sessions=context.get_recent_sessions()
        )
    
    def _show_document_analysis(self, document: Document) -> None:
        """Show document analysis to user."""
        word_limit = WordLimit(self.configuration.get_word_limit())
        chunks_needed = self.chunking_service.calculate_chunks_needed(
            document, word_limit
        )
        
        self.user_interface.show_progress(
            "Document analysis",
            {
                "total_words": str(document.word_count),
                "word_limit": int(word_limit),
                "chunks_needed": chunks_needed
            }
        )
    
    def _show_context_status(self, context: FormattingContext) -> None:
        """Show context status to user."""
        self.user_interface.show_progress(
            "Context loaded",
            {
                "sessions": len(context.session_history),
                "total_words": str(context.get_total_words_processed()),
                "custom_instructions": context.has_custom_instructions()
            }
        )


class ProcessingInputs:
    """Data class for processing inputs."""
    
    def __init__(
        self,
        document: Document,
        formatting_prompt: str,
        context: Optional[FormattingContext] = None
    ):
        self.document = document
        self.formatting_prompt = formatting_prompt
        self.context = context