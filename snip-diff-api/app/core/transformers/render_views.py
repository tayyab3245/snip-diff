"""
Diff rendering transformers for SNIP-DIFF multi-view system
Converts base line operations into different view modes without re-diffing
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from app.core.models.diff_types import (
    LineToken, LineType, UnifiedHunk, SideBySideRow, RenderOptions,
    DiffMode
)


class DiffRenderer:
    """
    Transform base diff hunks into multiple rendered modes
    Reuses base line array to avoid recomputation
    """
    
    def render_all_modes(self, hunks: List[UnifiedHunk], 
                        options: RenderOptions) -> Dict[str, Any]:
        """
        Generate all diff modes from base hunks
        
        Args:
            hunks: Base unified hunks from diff algorithm
            options: Rendering configuration
            
        Returns:
            Dict with keys: unified_full, unified_context, side_by_side, inline_full
        """
        # Extract all line tokens from hunks
        all_lines = []
        for hunk in hunks:
            all_lines.extend(hunk.lines)
        
        return {
            DiffMode.UNIFIED_FULL.value: self.render_unified_full(all_lines, options),
            DiffMode.UNIFIED_CONTEXT.value: self.render_unified_context(hunks, options),
            DiffMode.SIDE_BY_SIDE.value: self.render_side_by_side(all_lines, options),
            DiffMode.INLINE_FULL.value: self.render_inline_full(all_lines, options)
        }
    
    def render_unified_full(self, lines: List[LineToken], 
                           options: RenderOptions) -> List[Dict[str, Any]]:
        """
        Render unified diff with all lines (no context filtering)
        
        Returns:
            List of line dicts with format info for UI rendering
        """
        rendered_lines = []
        
        for line in lines:
            if options.max_lines and len(rendered_lines) >= options.max_lines:
                break
                
            # Determine line prefix symbol
            if line.line_type == LineType.ADDED:
                prefix = "+"
                css_class = "diff-added"
            elif line.line_type == LineType.DELETED:
                prefix = "-"
                css_class = "diff-deleted"
            elif line.line_type == LineType.MODIFIED:
                prefix = "~"
                css_class = "diff-modified"
            else:
                prefix = " "
                css_class = "diff-context"
            
            # Format line numbers
            old_no = str(line.line_no_old) if line.line_no_old else ""
            new_no = str(line.line_no_new) if line.line_no_new else ""
            
            rendered_lines.append({
                "line_no_old": old_no,
                "line_no_new": new_no,
                "prefix": prefix,
                "text": line.text,
                "css_class": css_class,
                "line_type": line.line_type.value,
                "show_line_numbers": options.show_line_numbers
            })
        
        return rendered_lines
    
    def render_unified_context(self, hunks: List[UnifiedHunk], 
                              options: RenderOptions) -> List[Dict[str, Any]]:
        """
        Render unified diff with only changed hunks + context
        
        Returns:
            List of hunk sections with headers and lines
        """
        rendered_hunks = []
        
        for hunk in hunks:
            if options.max_lines and len(rendered_hunks) * 20 >= options.max_lines:
                break
            
            # Apply context filtering to hunk
            context_lines = self._filter_context_lines(hunk.lines, options.context_radius)
            
            if not context_lines:
                continue
            
            # Render hunk header
            hunk_data = {
                "header": hunk.header,
                "old_start": hunk.old_start,
                "old_count": hunk.old_count,
                "new_start": hunk.new_start,
                "new_count": hunk.new_count,
                "lines": []
            }
            
            # Render hunk lines
            for line in context_lines:
                prefix = "+" if line.line_type == LineType.ADDED else \
                        "-" if line.line_type == LineType.DELETED else \
                        "~" if line.line_type == LineType.MODIFIED else " "
                
                css_class = f"diff-{line.line_type.value}"
                
                hunk_data["lines"].append({
                    "line_no_old": str(line.line_no_old) if line.line_no_old else "",
                    "line_no_new": str(line.line_no_new) if line.line_no_new else "",
                    "prefix": prefix,
                    "text": line.text,
                    "css_class": css_class,
                    "line_type": line.line_type.value
                })
            
            rendered_hunks.append(hunk_data)
        
        return rendered_hunks
    
    def render_side_by_side(self, lines: List[LineToken], 
                           options: RenderOptions) -> List[Dict[str, Any]]:
        """
        Render side-by-side diff with left/right alignment
        
        Returns:
            List of row dicts with left/right content
        """
        # Convert line tokens to side-by-side rows
        rows = self._align_side_by_side(lines)
        
        rendered_rows = []
        
        for row in rows:
            if options.max_lines and len(rendered_rows) >= options.max_lines:
                break
            
            # Format left side (old file)
            left_data = None
            if row.left:
                left_data = {
                    "line_no": str(row.left.line_no_old) if row.left.line_no_old else "",
                    "text": row.left.text,
                    "css_class": f"diff-{row.left.line_type.value}"
                }
            
            # Format right side (new file)  
            right_data = None
            if row.right:
                right_data = {
                    "line_no": str(row.right.line_no_new) if row.right.line_no_new else "",
                    "text": row.right.text,
                    "css_class": f"diff-{row.right.line_type.value}"
                }
            
            # Row styling based on change type
            if row.row_type == LineType.ADDED:
                row_class = "diff-row-added"
            elif row.row_type == LineType.DELETED:
                row_class = "diff-row-deleted"
            elif row.row_type == LineType.MODIFIED:
                row_class = "diff-row-modified"
            else:
                row_class = "diff-row-context"
            
            rendered_rows.append({
                "left": left_data,
                "right": right_data,
                "row_type": row.row_type.value,
                "css_class": row_class,
                "show_line_numbers": options.show_line_numbers
            })
        
        return rendered_rows
    
    def render_inline_full(self, lines: List[LineToken], 
                          options: RenderOptions) -> Dict[str, Any]:
        """
        Render full file content with inline change highlights
        
        Returns:
            Dict with full file content and change annotations
        """
        # Build complete file content with change markers
        file_lines = []
        change_ranges = []
        current_line_no = 1
        
        for line in lines:
            if options.max_lines and len(file_lines) >= options.max_lines:
                break
            
            if line.line_type == LineType.CONTEXT:
                # Regular line - add as-is
                file_lines.append({
                    "line_no": current_line_no,
                    "text": line.text,
                    "type": "context",
                    "css_class": "diff-context"
                })
                current_line_no += 1
                
            elif line.line_type == LineType.ADDED:
                # Added line - highlight as insertion
                file_lines.append({
                    "line_no": current_line_no,
                    "text": line.text,
                    "type": "added",
                    "css_class": "diff-added-inline",
                    "highlight": True
                })
                change_ranges.append({
                    "start_line": current_line_no,
                    "end_line": current_line_no,
                    "type": "addition"
                })
                current_line_no += 1
                
            elif line.line_type == LineType.DELETED:
                # Deleted line - show as strikethrough or background highlight
                if not options.collapse_unchanged:
                    file_lines.append({
                        "line_no": "del",
                        "text": line.text,
                        "type": "deleted", 
                        "css_class": "diff-deleted-inline",
                        "highlight": True,
                        "strikethrough": True
                    })
                
                change_ranges.append({
                    "start_line": current_line_no - 1,
                    "end_line": current_line_no - 1,
                    "type": "deletion"
                })
                
            elif line.line_type == LineType.MODIFIED:
                # Modified line - show both old and new with char-level diff if enabled
                if options.char_level:
                    char_diff = self._compute_char_diff(line.text, line.text)  # Placeholder
                    file_lines.append({
                        "line_no": current_line_no,
                        "text": line.text,
                        "type": "modified",
                        "css_class": "diff-modified-inline",
                        "highlight": True,
                        "char_diff": char_diff
                    })
                else:
                    file_lines.append({
                        "line_no": current_line_no,
                        "text": line.text,
                        "type": "modified",
                        "css_class": "diff-modified-inline",
                        "highlight": True
                    })
                
                change_ranges.append({
                    "start_line": current_line_no,
                    "end_line": current_line_no,
                    "type": "modification"
                })
                current_line_no += 1
        
        return {
            "lines": file_lines,
            "change_ranges": change_ranges,
            "total_lines": len(file_lines),
            "show_line_numbers": options.show_line_numbers,
            "collapse_unchanged": options.collapse_unchanged,
            "char_level": options.char_level
        }
    
    def _filter_context_lines(self, lines: List[LineToken], 
                             context_radius: int) -> List[LineToken]:
        """Filter lines to include only changes + context"""
        if context_radius <= 0:
            # Return only changed lines
            return [line for line in lines if line.line_type != LineType.CONTEXT]
        
        # Mark which lines to include
        include_mask = [False] * len(lines)
        
        # Mark change lines
        for i, line in enumerate(lines):
            if line.line_type != LineType.CONTEXT:
                include_mask[i] = True
                
                # Mark context around changes
                start = max(0, i - context_radius)
                end = min(len(lines), i + context_radius + 1)
                for j in range(start, end):
                    include_mask[j] = True
        
        # Return filtered lines
        return [lines[i] for i, include in enumerate(include_mask) if include]
    
    def _align_side_by_side(self, lines: List[LineToken]) -> List[SideBySideRow]:
        """Convert line tokens to aligned side-by-side rows"""
        rows = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            if line.line_type == LineType.CONTEXT:
                # Context line appears on both sides
                rows.append(SideBySideRow(left=line, right=line))
                i += 1
                
            elif line.line_type == LineType.ADDED:
                # Added line - only on right side
                rows.append(SideBySideRow(left=None, right=line))
                i += 1
                
            elif line.line_type == LineType.DELETED:
                # Deleted line - check if next line is addition (replacement)
                if (i + 1 < len(lines) and 
                    lines[i + 1].line_type == LineType.ADDED):
                    # Replacement - show delete on left, add on right
                    rows.append(SideBySideRow(left=line, right=lines[i + 1]))
                    i += 2
                else:
                    # Pure deletion - only on left side
                    rows.append(SideBySideRow(left=line, right=None))
                    i += 1
                    
            else:
                # Modified or other types
                rows.append(SideBySideRow(left=line, right=line))
                i += 1
        
        return rows
    
    def _compute_char_diff(self, old_text: str, new_text: str) -> List[Dict[str, Any]]:
        """
        Compute character-level diff for inline highlighting
        Placeholder implementation - can be enhanced later
        """
        import difflib
        
        if len(old_text) > 300 or len(new_text) > 300:
            # Skip char diff for very long lines
            return []
        
        char_diff = []
        matcher = difflib.SequenceMatcher(None, old_text, new_text)
        
        for tag, old_start, old_end, new_start, new_end in matcher.get_opcodes():
            if tag == 'equal':
                char_diff.append({
                    "type": "unchanged",
                    "text": old_text[old_start:old_end],
                    "start": old_start,
                    "end": old_end
                })
            elif tag == 'delete':
                char_diff.append({
                    "type": "deleted",
                    "text": old_text[old_start:old_end],
                    "start": old_start,
                    "end": old_end
                })
            elif tag == 'insert':
                char_diff.append({
                    "type": "added",
                    "text": new_text[new_start:new_end],
                    "start": new_start,
                    "end": new_end
                })
            elif tag == 'replace':
                char_diff.append({
                    "type": "deleted",
                    "text": old_text[old_start:old_end],
                    "start": old_start,
                    "end": old_end
                })
                char_diff.append({
                    "type": "added", 
                    "text": new_text[new_start:new_end],
                    "start": new_start,
                    "end": new_end
                })
        
        return char_diff


# Convenience functions for single-mode rendering
def render_unified_full(hunks: List[UnifiedHunk], 
                       options: RenderOptions = None) -> List[Dict[str, Any]]:
    """Render unified full mode"""
    if options is None:
        options = RenderOptions()
    
    renderer = DiffRenderer()
    all_lines = []
    for hunk in hunks:
        all_lines.extend(hunk.lines)
    
    return renderer.render_unified_full(all_lines, options)


def render_unified_context(hunks: List[UnifiedHunk], 
                          options: RenderOptions = None) -> List[Dict[str, Any]]:
    """Render unified context mode"""
    if options is None:
        options = RenderOptions()
    
    renderer = DiffRenderer()
    return renderer.render_unified_context(hunks, options)


def render_side_by_side(hunks: List[UnifiedHunk], 
                       options: RenderOptions = None) -> List[Dict[str, Any]]:
    """Render side-by-side mode"""
    if options is None:
        options = RenderOptions()
    
    renderer = DiffRenderer()
    all_lines = []
    for hunk in hunks:
        all_lines.extend(hunk.lines)
    
    return renderer.render_side_by_side(all_lines, options)


def render_inline_full(hunks: List[UnifiedHunk], 
                      options: RenderOptions = None) -> Dict[str, Any]:
    """Render inline full mode"""
    if options is None:
        options = RenderOptions()
    
    renderer = DiffRenderer()
    all_lines = []
    for hunk in hunks:
        all_lines.extend(hunk.lines)
    
    return renderer.render_inline_full(all_lines, options)


# Global renderer instance
diff_renderer = DiffRenderer()

__all__ = [
    'DiffRenderer', 'diff_renderer',
    'render_unified_full', 'render_unified_context', 
    'render_side_by_side', 'render_inline_full'
]
