/**
 * Path Utilities for SNIP-DIFF
 * Handles path normalization for consistent Git operations across Windows/Unix
 */

/**
 * Normalize path for comparison
 * Converts backslashes to forward slashes and lowercases for case-insensitive comparison
 */
export function normalizePathForCompare(path: string): string {
  return path.replace(/\\/g, '/').toLowerCase();
}

/**
 * Get relative path from base to target, normalized
 */
export function getRelativePath(from: string, to: string): string {
  // Handle Windows paths
  const fromNormalized = normalizePathForCompare(from);
  const toNormalized = normalizePathForCompare(to);
  
  // If 'to' starts with 'from', remove the base path
  if (toNormalized.startsWith(fromNormalized)) {
    let relative = toNormalized.substring(fromNormalized.length);
    // Remove leading slash
    if (relative.startsWith('/')) {
      relative = relative.substring(1);
    }
    return relative;
  }
  
  return toNormalized;
}

/**
 * Check if two paths match (case-insensitive, slash-normalized)
 */
export function pathsMatch(path1: string, path2: string): boolean {
  return normalizePathForCompare(path1) === normalizePathForCompare(path2);
}

/**
 * Check if childPath is under parentPath
 */
export function isPathUnder(childPath: string, parentPath: string): boolean {
  const childNorm = normalizePathForCompare(childPath);
  const parentNorm = normalizePathForCompare(parentPath);
  
  return childNorm.startsWith(parentNorm + '/') || childNorm === parentNorm;
}
