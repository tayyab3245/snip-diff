"""
Core diff algorithms for SNIP-DIFF
Implements Myers algorithm with Patience fallback for robust diff generation
"""

import time
from typing import List, Tuple, Dict, Optional, Sequence
from dataclasses import dataclass
from app.core.models.diff_types import (
    LineToken, LineType, UnifiedHunk, DiffStats, ChangeType
)


@dataclass
class DiffOperation:
    """Single diff operation"""
    operation: str  # 'equal', 'delete', 'insert'
    old_start: int
    old_end: int  
    new_start: int
    new_end: int
    
    @property
    def old_lines(self) -> int:
        return self.old_end - self.old_start
    
    @property 
    def new_lines(self) -> int:
        return self.new_end - self.new_start


class MyersDiffAlgorithm:
    """
    Implementation of Myers diff algorithm (LCS-based)
    Reference: "An O(ND) Difference Algorithm and Its Variations" by Eugene W. Myers
    """
    
    def __init__(self, max_lines: int = 50000):
        """
        Initialize Myers algorithm with memory safety limits
        
        Args:
            max_lines: Maximum file size to process (prevents memory issues)
        """
        self.max_lines = max_lines
    
    def compute_diff(self, old_lines: List[str], new_lines: List[str]) -> List[DiffOperation]:
        """
        Compute diff operations using Myers algorithm
        Simplified implementation using difflib as base but with structured output
        """
        import difflib
        
        # Handle empty files
        if not old_lines and not new_lines:
            return []
        if not old_lines:
            return [DiffOperation('insert', 0, 0, 0, len(new_lines))]
        if not new_lines:
            return [DiffOperation('delete', 0, len(old_lines), 0, 0)]
            
        # Use difflib for now but convert to our operation format
        # This provides stable, correct results while we can enhance the algorithm later
        operations = []
        matcher = difflib.SequenceMatcher(None, old_lines, new_lines)
        
        for tag, old_start, old_end, new_start, new_end in matcher.get_opcodes():
            if tag == 'equal':
                operations.append(DiffOperation('equal', old_start, old_end, new_start, new_end))
            elif tag == 'delete':
                operations.append(DiffOperation('delete', old_start, old_end, new_start, new_end))
            elif tag == 'insert':
                operations.append(DiffOperation('insert', old_start, old_end, new_start, new_end))
            elif tag == 'replace':
                # Split replace into delete + insert for cleaner output
                operations.append(DiffOperation('delete', old_start, old_end, new_start, new_start))
                operations.append(DiffOperation('insert', old_end, old_end, new_start, new_end))
        
        return operations
    
    def _myers_diff(self, old_lines: List[str], new_lines: List[str]) -> List[DiffOperation]:
        """Core Myers algorithm implementation"""
        n, m = len(old_lines), len(new_lines)
        max_d = n + m
        
        # v[k] = x coordinate of furthest reaching path on diagonal k
        v = {}
        v[1] = 0
        
        # Store path history for backtracking
        trace = []
        
        for d in range(max_d + 1):
            trace.append(v.copy())
            
            for k in range(-d, d + 1, 2):
                # Choose direction: down (delete) or right (insert)
                if k == -d or (k != d and v.get(k-1, -1) < v.get(k+1, -1)):
                    x = v.get(k+1, -1)  # Come from above (insert)
                else:
                    x = v.get(k-1, -1) + 1  # Come from left (delete)
                
                y = x - k
                
                # Extend diagonal (equal lines)
                while (x < n and y < m and old_lines[x] == new_lines[y]):
                    x += 1
                    y += 1
                
                v[k] = x
                
                # Found solution
                if x >= n and y >= m:
                    return self._backtrack_operations(old_lines, new_lines, trace, d)
        
        # Fallback - should not happen with correct algorithm
        return [DiffOperation('delete', 0, n, 0, 0), 
                DiffOperation('insert', 0, 0, 0, m)]
    
    def _backtrack_operations(self, old_lines: List[str], new_lines: List[str], 
                            trace: List[Dict], d: int) -> List[DiffOperation]:
        """Backtrack through the trace to construct diff operations"""
        operations = []
        x, y = len(old_lines), len(new_lines)
        
        for depth in range(d, -1, -1):
            v = trace[depth]
            k = x - y
            
            # Determine previous position
            if k == -depth or (k != depth and v.get(k-1, -1) < v.get(k+1, -1)):
                prev_k = k + 1
                prev_x = v.get(prev_k, -1)
                prev_y = prev_x - prev_k
                # Insert operation
                operations.append(DiffOperation('insert', prev_x, prev_x, prev_y, y))
                x, y = prev_x, prev_y
            else:
                prev_k = k - 1  
                prev_x = v.get(prev_k, -1) + 1
                prev_y = prev_x - prev_k
                # Delete operation
                operations.append(DiffOperation('delete', prev_x, x, prev_y, prev_y))
                x, y = prev_x, prev_y
            
            # Handle diagonal (equal lines)
            if depth > 0:
                while x > 0 and y > 0 and old_lines[x-1] == new_lines[y-1]:
                    x -= 1
                    y -= 1
                    if x < prev_x - 1 or y < prev_y - 1:  # Found equal section
                        operations.append(DiffOperation('equal', x, prev_x-1, y, prev_y-1))
                        break
        
        # Add initial equal section if exists
        if x > 0 and y > 0:
            equal_len = min(x, y)
            equal_end = 0
            while (equal_end < equal_len and 
                   old_lines[equal_end] == new_lines[equal_end]):
                equal_end += 1
            if equal_end > 0:
                operations.append(DiffOperation('equal', 0, equal_end, 0, equal_end))
        
        operations.reverse()
        return self._merge_consecutive_operations(operations)
    
    def _merge_consecutive_operations(self, operations: List[DiffOperation]) -> List[DiffOperation]:
        """Merge consecutive operations of the same type"""
        if not operations:
            return []
            
        merged = [operations[0]]
        
        for op in operations[1:]:
            last = merged[-1]
            
            if (op.operation == last.operation and 
                op.old_start == last.old_end and
                op.new_start == last.new_end):
                # Merge with previous operation
                merged[-1] = DiffOperation(
                    op.operation,
                    last.old_start, op.old_end,
                    last.new_start, op.new_end
                )
            else:
                merged.append(op)
        
        return merged
    
    def _chunked_diff(self, old_lines: List[str], new_lines: List[str]) -> List[DiffOperation]:
        """Handle very large files by chunking"""
        chunk_size = self.max_lines // 2
        operations = []
        
        old_pos, new_pos = 0, 0
        
        while old_pos < len(old_lines) or new_pos < len(new_lines):
            old_chunk = old_lines[old_pos:old_pos + chunk_size]
            new_chunk = new_lines[new_pos:new_pos + chunk_size]
            
            chunk_ops = self._myers_diff(old_chunk, new_chunk)
            
            # Adjust positions for chunk
            for op in chunk_ops:
                operations.append(DiffOperation(
                    op.operation,
                    op.old_start + old_pos, op.old_end + old_pos,
                    op.new_start + new_pos, op.new_end + new_pos
                ))
            
            old_pos += len(old_chunk)
            new_pos += len(new_chunk)
        
        return operations


class PatienceDiffAlgorithm:
    """
    Patience diff algorithm for better handling of moved blocks
    Used as fallback for large change spans
    """
    
    def compute_diff(self, old_lines: List[str], new_lines: List[str]) -> List[DiffOperation]:
        """
        Compute diff using patience algorithm
        Simplified implementation - identifies unique lines as anchors
        """
        # Find unique lines that appear in both files
        old_unique = {}
        new_unique = {}
        
        for i, line in enumerate(old_lines):
            if old_lines.count(line) == 1:
                old_unique[line] = i
                
        for i, line in enumerate(new_lines):
            if new_lines.count(line) == 1:
                new_unique[line] = i
        
        # Find common unique lines (anchors)
        anchors = []
        for line in old_unique:
            if line in new_unique:
                anchors.append((old_unique[line], new_unique[line], line))
        
        # Sort anchors by old file position
        anchors.sort(key=lambda x: x[0])
        
        # Build operations between anchors
        operations = []
        old_pos, new_pos = 0, 0
        
        for old_anchor, new_anchor, line in anchors:
            # Process section before anchor
            if old_pos < old_anchor or new_pos < new_anchor:
                if old_pos < old_anchor and new_pos < new_anchor:
                    # Both sections exist - recursively diff them
                    sub_ops = MyersDiffAlgorithm()._myers_diff(
                        old_lines[old_pos:old_anchor],
                        new_lines[new_pos:new_anchor]
                    )
                    for op in sub_ops:
                        operations.append(DiffOperation(
                            op.operation,
                            op.old_start + old_pos, op.old_end + old_pos,
                            op.new_start + new_pos, op.new_end + new_pos
                        ))
                elif old_pos < old_anchor:
                    # Only old section - delete
                    operations.append(DiffOperation('delete', old_pos, old_anchor, new_pos, new_pos))
                else:
                    # Only new section - insert  
                    operations.append(DiffOperation('insert', old_pos, old_pos, new_pos, new_anchor))
            
            # Add anchor as equal
            operations.append(DiffOperation('equal', old_anchor, old_anchor + 1, new_anchor, new_anchor + 1))
            old_pos, new_pos = old_anchor + 1, new_anchor + 1
        
        # Handle remaining sections
        if old_pos < len(old_lines) or new_pos < len(new_lines):
            if old_pos < len(old_lines) and new_pos < len(new_lines):
                sub_ops = MyersDiffAlgorithm()._myers_diff(
                    old_lines[old_pos:], new_lines[new_pos:]
                )
                for op in sub_ops:
                    operations.append(DiffOperation(
                        op.operation,
                        op.old_start + old_pos, op.old_end + old_pos,
                        op.new_start + new_pos, op.new_end + new_pos
                    ))
            elif old_pos < len(old_lines):
                operations.append(DiffOperation('delete', old_pos, len(old_lines), new_pos, new_pos))
            else:
                operations.append(DiffOperation('insert', old_pos, old_pos, new_pos, len(new_lines)))
        
        return operations


class HybridDiffEngine:
    """
    Hybrid diff engine combining Myers + Patience algorithms
    Uses Myers by default, falls back to Patience for large change blocks
    """
    
    def __init__(self, patience_threshold: int = 100):
        """
        Initialize hybrid engine
        
        Args:
            patience_threshold: Use patience algorithm for change blocks larger than this
        """
        self.myers = MyersDiffAlgorithm()
        self.patience = PatienceDiffAlgorithm()
        self.patience_threshold = patience_threshold
    
    def generate_unified(self, old_content: str, new_content: str) -> Tuple[List[UnifiedHunk], DiffStats]:
        """
        Generate unified diff hunks with statistics
        
        Args:
            old_content: Original file content
            new_content: New file content
            
        Returns:
            Tuple of (hunks, stats)
        """
        start_time = time.time()
        
        # Normalize line endings and split
        old_lines = self._normalize_lines(old_content)
        new_lines = self._normalize_lines(new_content)
        
        # Choose algorithm based on change size
        operations = self._compute_operations(old_lines, new_lines)
        
        # Convert operations to line tokens
        line_tokens = self._operations_to_tokens(operations, old_lines, new_lines)
        
        # Group into hunks and compute stats
        hunks = self._group_into_hunks(line_tokens)
        stats = self._compute_stats(line_tokens)
        
        # Log performance
        duration = (time.time() - start_time) * 1000
        print(f"Diff computed in {duration:.1f}ms for {len(old_lines)}/{len(new_lines)} lines")
        
        return hunks, stats
    
    def _normalize_lines(self, content: str) -> List[str]:
        """Normalize line endings and split content"""
        if not content:
            return []
        # Handle different line endings
        content = content.replace('\r\n', '\n').replace('\r', '\n')
        return content.splitlines()
    
    def _compute_operations(self, old_lines: List[str], new_lines: List[str]) -> List[DiffOperation]:
        """Choose algorithm and compute operations"""
        # Start with Myers algorithm
        operations = self.myers.compute_diff(old_lines, new_lines)
        
        # Check for large change blocks that might benefit from patience
        should_use_patience = False
        for op in operations:
            if (op.operation in ('delete', 'insert') and 
                (op.old_lines + op.new_lines) > self.patience_threshold):
                should_use_patience = True
                break
        
        if should_use_patience:
            # Re-compute with patience algorithm
            operations = self.patience.compute_diff(old_lines, new_lines)
        
        return operations
    
    def _operations_to_tokens(self, operations: List[DiffOperation], 
                            old_lines: List[str], new_lines: List[str]) -> List[LineToken]:
        """Convert diff operations to line tokens"""
        tokens = []
        old_line_no, new_line_no = 1, 1
        
        for op in operations:
            if op.operation == 'equal':
                # Context lines
                for i in range(op.old_lines):
                    tokens.append(LineToken(
                        line_no_old=old_line_no + i,
                        line_no_new=new_line_no + i,
                        line_type=LineType.CONTEXT,
                        text=old_lines[op.old_start + i]
                    ))
                old_line_no += op.old_lines
                new_line_no += op.new_lines
            elif op.operation == 'delete':
                # Deleted lines
                for i in range(op.old_lines):
                    tokens.append(LineToken(
                        line_no_old=old_line_no + i,
                        line_no_new=None,
                        line_type=LineType.DELETED,
                        text=old_lines[op.old_start + i]
                    ))
                old_line_no += op.old_lines
            elif op.operation == 'insert':
                # Added lines
                for i in range(op.new_lines):
                    tokens.append(LineToken(
                        line_no_old=None,
                        line_no_new=new_line_no + i,
                        line_type=LineType.ADDED,
                        text=new_lines[op.new_start + i]
                    ))
                new_line_no += op.new_lines
        
        return tokens
    
    def _group_into_hunks(self, tokens: List[LineToken], context_radius: int = 3) -> List[UnifiedHunk]:
        """Group line tokens into unified hunks"""
        if not tokens:
            return []
        
        hunks = []
        current_hunk_tokens = []
        last_change_index = -1
        
        for i, token in enumerate(tokens):
            is_change = token.line_type in (LineType.ADDED, LineType.DELETED, LineType.MODIFIED)
            
            if is_change:
                # Include context before change
                start_context = max(0, last_change_index + 1, i - context_radius)
                for j in range(start_context, i):
                    if j >= len(current_hunk_tokens):
                        current_hunk_tokens.append(tokens[j])
                
                current_hunk_tokens.append(token)
                last_change_index = i
            elif current_hunk_tokens and i <= last_change_index + context_radius:
                # Include context after change
                current_hunk_tokens.append(token)
            elif current_hunk_tokens:
                # End current hunk and start new one
                hunk = self._create_hunk_from_tokens(current_hunk_tokens)
                hunks.append(hunk)
                current_hunk_tokens = []
        
        # Add final hunk if exists
        if current_hunk_tokens:
            hunk = self._create_hunk_from_tokens(current_hunk_tokens)
            hunks.append(hunk)
        
        return hunks
    
    def _create_hunk_from_tokens(self, tokens: List[LineToken]) -> UnifiedHunk:
        """Create a UnifiedHunk from line tokens"""
        if not tokens:
            return UnifiedHunk(0, 0, 0, 0, [])
        
        old_lines = [t for t in tokens if t.line_no_old is not None]
        new_lines = [t for t in tokens if t.line_no_new is not None]
        
        old_start = min(t.line_no_old for t in old_lines) if old_lines else 1
        new_start = min(t.line_no_new for t in new_lines) if new_lines else 1
        
        old_count = len(old_lines)
        new_count = len(new_lines)
        
        return UnifiedHunk(
            old_start=old_start,
            old_count=old_count,
            new_start=new_start, 
            new_count=new_count,
            lines=tokens
        )
    
    def _compute_stats(self, tokens: List[LineToken]) -> DiffStats:
        """Compute diff statistics from line tokens"""
        stats = DiffStats()
        
        for token in tokens:
            if token.line_type == LineType.ADDED:
                stats.lines_added += 1
            elif token.line_type == LineType.DELETED:
                stats.lines_deleted += 1
            elif token.line_type == LineType.MODIFIED:
                stats.lines_modified += 1
            elif token.line_type == LineType.CONTEXT:
                stats.lines_context += 1
        
        return stats


# Global instance for the application
diff_engine = HybridDiffEngine()

__all__ = ['HybridDiffEngine', 'MyersDiffAlgorithm', 'PatienceDiffAlgorithm', 'diff_engine']
