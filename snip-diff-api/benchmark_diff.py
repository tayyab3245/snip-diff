"""
Benchmark script for diff algorithms
Tests performance on various file sizes and change patterns
"""

import time
import random
import string
from typing import List
from app.core.algorithms.diff_core import HybridDiffEngine, MyersDiffAlgorithm


def generate_test_content(lines: int, line_length: int = 50) -> str:
    """Generate test file content"""
    content_lines = []
    for i in range(lines):
        line = f"Line {i:04d}: " + ''.join(random.choices(string.ascii_letters + string.digits + ' ', k=line_length-15))
        content_lines.append(line)
    return '\n'.join(content_lines)


def modify_content(content: str, change_ratio: float = 0.1) -> str:
    """Modify content by changing a percentage of lines"""
    lines = content.splitlines()
    num_changes = int(len(lines) * change_ratio)
    
    # Randomly select lines to modify
    change_indices = random.sample(range(len(lines)), min(num_changes, len(lines)))
    
    for i in change_indices:
        if random.random() < 0.5:
            # Modify existing line
            lines[i] = lines[i] + " [MODIFIED]"
        else:
            # Replace with new line
            lines[i] = f"NEW LINE {i}: " + ''.join(random.choices(string.ascii_letters, k=40))
    
    # Add some new lines
    for _ in range(num_changes // 3):
        insert_pos = random.randint(0, len(lines))
        lines.insert(insert_pos, f"INSERTED LINE: " + ''.join(random.choices(string.ascii_letters, k=40)))
    
    # Remove some lines
    for _ in range(num_changes // 4):
        if len(lines) > 10:
            remove_pos = random.randint(0, len(lines) - 1)
            lines.pop(remove_pos)
    
    return '\n'.join(lines)


def benchmark_algorithm(algorithm, old_content: str, new_content: str, name: str) -> dict:
    """Benchmark a single algorithm"""
    start_time = time.time()
    
    if hasattr(algorithm, 'generate_unified'):
        # HybridDiffEngine
        hunks, stats = algorithm.generate_unified(old_content, new_content)
        result = {
            'hunks': len(hunks),
            'lines_added': stats.lines_added,
            'lines_deleted': stats.lines_deleted,
            'lines_modified': stats.lines_modified
        }
    else:
        # MyersDiffAlgorithm
        old_lines = old_content.splitlines()
        new_lines = new_content.splitlines()
        operations = algorithm.compute_diff(old_lines, new_lines)
        result = {
            'operations': len(operations),
            'changes': sum(1 for op in operations if op.operation != 'equal')
        }
    
    duration = (time.time() - start_time) * 1000
    result['duration_ms'] = duration
    result['algorithm'] = name
    
    return result


def run_benchmarks():
    """Run comprehensive benchmarks"""
    print("SNIP-DIFF Algorithm Benchmark")
    print("=" * 50)
    
    # Test cases: (lines, change_ratio, description)
    test_cases = [
        (10, 0.2, "Small file, 20% changes"),
        (100, 0.1, "Medium file, 10% changes"),
        (500, 0.05, "Large file, 5% changes"),
        (1000, 0.02, "Very large file, 2% changes"),
        (50, 0.8, "Small file, major changes"),
    ]
    
    algorithms = [
        (HybridDiffEngine(), "Hybrid (Myers+Patience)"),
        (MyersDiffAlgorithm(), "Myers Only")
    ]
    
    results = []
    
    for lines, change_ratio, description in test_cases:
        print(f"\n{description} ({lines} lines)")
        print("-" * 40)
        
        # Generate test data
        old_content = generate_test_content(lines)
        new_content = modify_content(old_content, change_ratio)
        
        old_line_count = len(old_content.splitlines())
        new_line_count = len(new_content.splitlines())
        print(f"Lines: {old_line_count} → {new_line_count}")
        
        for algorithm, name in algorithms:
            try:
                result = benchmark_algorithm(algorithm, old_content, new_content, name)
                results.append(result)
                print(f"{name:25} {result['duration_ms']:8.1f}ms")
            except Exception as e:
                print(f"{name:25} ERROR: {e}")
    
    # Summary
    print("\n" + "=" * 50)
    print("PERFORMANCE SUMMARY")
    print("=" * 50)
    
    for algorithm_name in ["Hybrid (Myers+Patience)", "Myers Only"]:
        algo_results = [r for r in results if r['algorithm'] == algorithm_name]
        if algo_results:
            avg_time = sum(r['duration_ms'] for r in algo_results) / len(algo_results)
            max_time = max(r['duration_ms'] for r in algo_results)
            print(f"{algorithm_name:25} Avg: {avg_time:6.1f}ms  Max: {max_time:6.1f}ms")
    
    # Check performance targets
    print("\nPERFORMANCE TARGETS")
    print("-" * 30)
    target_met = True
    
    for result in results:
        if 'Small file' in str(result) and result['duration_ms'] > 10:
            print(f"❌ Small file target missed: {result['duration_ms']:.1f}ms > 10ms")
            target_met = False
        elif 'Medium file' in str(result) and result['duration_ms'] > 100:
            print(f"❌ Medium file target missed: {result['duration_ms']:.1f}ms > 100ms") 
            target_met = False
        elif 'Large file' in str(result) and result['duration_ms'] > 500:
            print(f"❌ Large file target missed: {result['duration_ms']:.1f}ms > 500ms")
            target_met = False
    
    if target_met:
        print("✅ All performance targets met!")
    
    return results


if __name__ == "__main__":
    # Set random seed for reproducible results
    random.seed(42)
    
    results = run_benchmarks()
