/*
 * Copyright 2025 Tayyab
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

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
