"""
Test golden samples for diff transform layer
Validates rendering output for mixed add/remove sequences
"""

from app.core.algorithms.diff_core import HybridDiffEngine
from app.core.transformers.render_views import DiffRenderer
from app.core.models.diff_types import RenderOptions
import json


def test_mixed_add_remove_sequence():
    """Test complex diff sequence with adds, removes, and context"""
    
    engine = HybridDiffEngine()
    renderer = DiffRenderer()
    
    # Test case: mixed operations
    old_content = """def function_a():
    print("old implementation")
    return 42

def function_b():
    # Comment that stays
    value = calculate_old()
    return value * 2

def function_c():
    pass"""

    new_content = """def function_a():
    print("new implementation") 
    print("additional line")
    return 42

def function_b():
    # Comment that stays
    value = calculate_new()
    extra_step = process(value)
    return extra_step * 3

def function_d():
    # This replaces function_c
    return "new function\""""

    # Generate diff
    hunks, stats = engine.generate_unified(old_content, new_content)
    
    # Test all modes
    options = RenderOptions(context_radius=2, show_line_numbers=True, char_level=False)
    all_modes = renderer.render_all_modes(hunks, options)
    
    # Golden sample validation
    print("=== GOLDEN SAMPLE TEST ===")
    print(f"Hunks: {len(hunks)}")
    print(f"Stats: +{stats.lines_added} -{stats.lines_deleted} ~{stats.lines_modified} ={stats.lines_context}")
    
    # Validate unified_full
    unified_full = all_modes['unified_full']
    print(f"\nUnified Full: {len(unified_full)} lines")
    for i, line in enumerate(unified_full[:10]):  # First 10 lines
        print(f"{i+1:2d}: {line['prefix']}{line['text']}")
    
    # Validate side_by_side alignment
    side_by_side = all_modes['side_by_side']
    print(f"\nSide by Side: {len(side_by_side)} rows")
    for i, row in enumerate(side_by_side[:8]):  # First 8 rows
        left = row['left']['text'] if row['left'] else "(empty)"
        right = row['right']['text'] if row['right'] else "(empty)"
        row_type = row['row_type']
        print(f"{i+1:2d}: {row_type:8s} | {left[:30]:30s} | {right[:30]:30s}")
    
    # Validate unified_context hunks
    unified_context = all_modes['unified_context']
    print(f"\nUnified Context: {len(unified_context)} hunks")
    for i, hunk in enumerate(unified_context):
        print(f"Hunk {i+1}: {hunk['header']}")
        print(f"  Lines: {len(hunk['lines'])}")
    
    # Validate inline_full structure
    inline_full = all_modes['inline_full']
    print(f"\nInline Full: {inline_full['total_lines']} lines, {len(inline_full['change_ranges'])} change ranges")
    
    # Export golden data for regression testing
    golden_data = {
        "test_case": "mixed_add_remove_sequence",
        "stats": {
            "lines_added": stats.lines_added,
            "lines_deleted": stats.lines_deleted, 
            "lines_modified": stats.lines_modified,
            "lines_context": stats.lines_context
        },
        "hunks_count": len(hunks),
        "unified_full_lines": len(unified_full),
        "side_by_side_rows": len(side_by_side),
        "unified_context_hunks": len(unified_context),
        "inline_full_lines": inline_full['total_lines'],
        "change_ranges": len(inline_full['change_ranges'])
    }
    
    print("\n=== GOLDEN DATA ===")
    print(json.dumps(golden_data, indent=2))
    
    # Assertions for validation
    assert stats.lines_added > 0, "Should have added lines"
    assert stats.lines_deleted > 0, "Should have deleted lines"
    assert len(unified_full) > 0, "Unified full should have lines"
    assert len(side_by_side) > 0, "Side by side should have rows"
    assert len(unified_context) > 0, "Should have context hunks"
    assert inline_full['total_lines'] > 0, "Inline full should have lines"
    
    print("\n✅ Golden sample test passed!")
    return golden_data


if __name__ == "__main__":
    test_mixed_add_remove_sequence()
