# Enhanced Text Reformatting Prompt

## Objective
Transform the provided text into a clear, well-structured, and visually appealing format using Markdown syntax.

## Instructions

### Primary Task
Take the given text and:
- **Rewrite** for improved clarity and flow
- **Restructure** using appropriate Markdown elements
- **Enhance** readability through proper formatting
- **Remove** any references to page numbers, internal citations, or source locations

### Content Cleaning
**Important**: Remove or rewrite the following elements:
- Page numbers (e.g., "on page 23", "[p. 45]")
- Internal references (e.g., "see section 3.2", "as shown in figure 5")
- Source locations (e.g., "found at line 234", "located in chapter 7")
- Academic citations that reference specific pages or sections
- Any metadata about document structure or location

Replace these with natural language transitions or omit them entirely when they don't add value to the content.

### Formatting Guidelines

1. **Use Headers** (`#`, `##`, `###`) to create logical sections
2. **Apply Text Styling**:
   - Bold (`**text**`) for emphasis
   - Italic (`*text*`) for subtle highlights
   - Code blocks (`` `code` ``) for technical terms

3. **Organize Content**:
   - Bullet points for unordered lists
   - Numbered lists for sequential steps
   - Blockquotes (`>`) for important notes

4. **Improve Readability**:
   - Break long paragraphs into shorter ones
   - Add line breaks between sections
   - Use horizontal rules (`---`) to separate major topics

### Expected Output
- Clean, professional Markdown formatting
- Logical information hierarchy
- Enhanced visual structure
- Preserved original meaning while improving presentation
- No page numbers or internal document references
- Smooth, natural flow without location markers

### Example Transformations

**Before**: "As discussed on page 47, the main concept..."
**After**: "The main concept..."

**Before**: "See section 3.2.1 for more details"
**After**: "Additional details are provided below" or simply omit

**Before**: "According to Smith (2020, p. 123)..."
**After**: "According to Smith (2020)..."

### Example Format
```markdown
# Main Topic

## Overview
Brief introduction paragraph...

## Key Points
- First important point
- Second important point

## Details
More detailed explanation...
```

**Note**: Maintain the original content's intent while making it more accessible and visually organized. Focus on the actual information rather than its original location or structure.

Ensure the output is roughly the same length as the input, compensating for removed references by slightly expanding on key concepts when appropriate.