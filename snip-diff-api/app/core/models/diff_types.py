"""
Diff data types and models for SNIP-DIFF multi-view system
Supports: unified_full, unified_context, side_by_side, inline_full
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel


class LineType(Enum):
    """Type of change for a diff line"""
    CONTEXT = "context"     # Unchanged line (space prefix)
    ADDED = "added"        # Added line (+ prefix)  
    DELETED = "deleted"    # Deleted line (- prefix)
    MODIFIED = "modified"  # Modified line (both add+del)


class ChangeType(Enum):
    """File-level change classification"""
    ADDED = "added"
    DELETED = "deleted" 
    MODIFIED = "modified"
    RENAMED = "renamed"
    UNCHANGED = "unchanged"


@dataclass
class LineToken:
    """Minimal neutral line representation for all diff modes"""
    line_no_old: Optional[int] = None    # Line number in old file (1-based)
    line_no_new: Optional[int] = None    # Line number in new file (1-based)
    line_type: LineType = LineType.CONTEXT
    text: str = ""                       # Line content (no newline)
    
    def __post_init__(self):
        """Validate line number consistency with type"""
        if self.line_type == LineType.DELETED and self.line_no_new is not None:
            self.line_no_new = None
        elif self.line_type == LineType.ADDED and self.line_no_old is not None:
            self.line_no_old = None


@dataclass 
class UnifiedHunk:
    """A contiguous block of changes in unified diff format"""
    old_start: int                       # Starting line in old file
    old_count: int                       # Number of lines in old file
    new_start: int                       # Starting line in new file  
    new_count: int                       # Number of lines in new file
    lines: List[LineToken] = field(default_factory=list)
    header: str = ""                     # @@ -old_start,old_count +new_start,new_count @@
    
    def __post_init__(self):
        """Generate header if not provided"""
        if not self.header:
            self.header = f"@@ -{self.old_start},{self.old_count} +{self.new_start},{self.new_count} @@"


@dataclass
class SideBySideRow:
    """Single row for side-by-side diff display"""
    left: Optional[LineToken] = None     # Left side (old file)
    right: Optional[LineToken] = None    # Right side (new file) 
    row_type: LineType = LineType.CONTEXT
    
    def __post_init__(self):
        """Determine row type from left/right content"""
        if self.left is None and self.right is not None:
            self.row_type = LineType.ADDED
        elif self.left is not None and self.right is None:
            self.row_type = LineType.DELETED
        elif self.left is not None and self.right is not None:
            if self.left.text == self.right.text:
                self.row_type = LineType.CONTEXT
            else:
                self.row_type = LineType.MODIFIED


@dataclass
class DiffStats:
    """Statistics about file changes"""
    lines_added: int = 0
    lines_deleted: int = 0
    lines_modified: int = 0
    lines_context: int = 0
    
    @property
    def total_changes(self) -> int:
        return self.lines_added + self.lines_deleted + self.lines_modified


@dataclass
class FileDiffMeta:
    """Metadata for a single file diff"""
    path: str
    old_path: Optional[str] = None       # For renamed files
    change_type: ChangeType = ChangeType.UNCHANGED
    file_size_old: int = 0
    file_size_new: int = 0
    is_binary: bool = False
    stats: DiffStats = field(default_factory=DiffStats)
    est_tokens_unified: int = 0          # Estimated tokens for unified (incremental/full)
    est_tokens_side_by_side: int = 0     # Estimated tokens for side-by-side textual export
    est_tokens_incremental: int = 0      # Estimated tokens for incremental context slice
    

@dataclass
class FileDiff:
    """Complete diff data for a single file"""
    meta: FileDiffMeta
    hunks: List[UnifiedHunk] = field(default_factory=list)
    
    # Rendered modes - computed on demand
    modes: Dict[str, Any] = field(default_factory=dict)
    
    def add_mode(self, mode_name: str, content: Any):
        """Add a rendered mode to this diff"""
        self.modes[mode_name] = content
    
    def get_mode(self, mode_name: str) -> Optional[Any]:
        """Get a specific rendered mode"""
        return self.modes.get(mode_name)


class DiffMode(Enum):
    """Available diff rendering modes"""
    UNIFIED_FULL = "unified_full"           # All lines with +/- markers
    UNIFIED_CONTEXT = "unified_context"     # Only changed hunks + context
    SIDE_BY_SIDE = "side_by_side"          # Left/right column layout
    INLINE_FULL = "inline_full"            # Full file with change highlights


@dataclass
class RenderOptions:
    """Options for diff rendering"""
    context_radius: int = 3              # Lines of context around changes
    max_lines: Optional[int] = None      # Limit total output lines
    show_line_numbers: bool = True
    collapse_unchanged: bool = False     # For inline_full mode
    char_level: bool = False            # Enable character-level highlighting


# Pydantic models for API serialization
class LineTokenAPI(BaseModel):
    """API serializable version of LineToken"""
    line_no_old: Optional[int] = None
    line_no_new: Optional[int] = None  
    line_type: str
    text: str


class UnifiedHunkAPI(BaseModel):
    """API serializable version of UnifiedHunk"""
    old_start: int
    old_count: int
    new_start: int
    new_count: int
    header: str
    lines: List[LineTokenAPI]


class SideBySideRowAPI(BaseModel):
    """API serializable version of SideBySideRow"""
    left: Optional[LineTokenAPI] = None
    right: Optional[LineTokenAPI] = None
    row_type: str


class DiffStatsAPI(BaseModel):
    """API serializable version of DiffStats"""
    lines_added: int
    lines_deleted: int
    lines_modified: int
    lines_context: int
    total_changes: int


class FileDiffMetaAPI(BaseModel):
    """API serializable version of FileDiffMeta"""
    path: str
    old_path: Optional[str] = None
    change_type: str
    file_size_old: int
    file_size_new: int
    is_binary: bool
    stats: DiffStatsAPI
    est_tokens_unified: int
    est_tokens_side_by_side: int
    est_tokens_incremental: int


class FileDiffAPI(BaseModel):
    """API serializable version of FileDiff"""
    meta: FileDiffMetaAPI
    hunks: List[UnifiedHunkAPI]
    modes: Dict[str, Any] = {}


# Conversion utilities
def line_token_to_api(token: LineToken) -> LineTokenAPI:
    """Convert LineToken to API model"""
    return LineTokenAPI(
        line_no_old=token.line_no_old,
        line_no_new=token.line_no_new,
        line_type=token.line_type.value,
        text=token.text
    )


def unified_hunk_to_api(hunk: UnifiedHunk) -> UnifiedHunkAPI:
    """Convert UnifiedHunk to API model"""
    return UnifiedHunkAPI(
        old_start=hunk.old_start,
        old_count=hunk.old_count,
        new_start=hunk.new_start,
        new_count=hunk.new_count,
        header=hunk.header,
        lines=[line_token_to_api(line) for line in hunk.lines]
    )


def side_by_side_row_to_api(row: SideBySideRow) -> SideBySideRowAPI:
    """Convert SideBySideRow to API model"""
    return SideBySideRowAPI(
        left=line_token_to_api(row.left) if row.left else None,
        right=line_token_to_api(row.right) if row.right else None,
        row_type=row.row_type.value
    )


def file_diff_to_api(file_diff: FileDiff) -> FileDiffAPI:
    """Convert FileDiff to API model"""
    return FileDiffAPI(
        meta=FileDiffMetaAPI(
            path=file_diff.meta.path,
            old_path=file_diff.meta.old_path,
            change_type=file_diff.meta.change_type.value,
            file_size_old=file_diff.meta.file_size_old,
            file_size_new=file_diff.meta.file_size_new,
            is_binary=file_diff.meta.is_binary,
            stats=DiffStatsAPI(
                lines_added=file_diff.meta.stats.lines_added,
                lines_deleted=file_diff.meta.stats.lines_deleted,
                lines_modified=file_diff.meta.stats.lines_modified,
                lines_context=file_diff.meta.stats.lines_context,
                total_changes=file_diff.meta.stats.total_changes
            )
        ),
        hunks=[unified_hunk_to_api(hunk) for hunk in file_diff.hunks],
        modes=file_diff.modes
    )


# API Request/Response Models for Live Diff
class WatchFileRequest(BaseModel):
    file_paths: List[str]

class WatchStatusResponse(BaseModel):
    is_watching: bool
    watched_files: List[str]
    stats: Dict[str, Any]

class FileEventResponse(BaseModel):
    file_path: str
    change_type: str
    timestamp: float
    
class LiveDiffResponse(BaseModel):
    success: bool
    message: str


# Prompt models
class PromptApplyRequest(BaseModel):
    strategy: str  # prepend | append | replace
    text: str

class PromptState(BaseModel):
    active_prompt: str = ""
    strategy: str = "prepend"
    total_tokens: int = 0
