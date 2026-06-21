#!/usr/bin/env python3
"""
search_vault.py
Token-conserving flat-file search utility.
Wraps ripgrep (rg) if available, otherwise falls back to native Python recursive regex search.
"""

import os
import sys
import shutil
import subprocess
import argparse
import re
import json

def get_args():
    parser = argparse.ArgumentParser(
        description="Search Flat-File Markdown Vault in a token-conserving manner."
    )
    parser.add_argument(
        "query",
        type=str,
        help="Search term or regular expression pattern."
    )
    parser.add_argument(
        "-d", "--dir",
        type=str,
        default="perimeter_knowledge",
        help="Target directory to search relative to workspace root (default: perimeter_knowledge)."
    )
    parser.add_argument(
        "-i", "--ignore-case",
        action="store_true",
        help="Perform a case-insensitive search."
    )
    parser.add_argument(
        "-r", "--regex",
        action="store_true",
        help="Treat query as a regular expression pattern."
    )
    parser.add_argument(
        "--json-output",
        action="store_true",
        help="Output results in JSON format."
    )
    return parser.parse_args()

def search_with_ripgrep(rg_path, query, target_dir, ignore_case, is_regex):
    # Construct ripgrep command
    # -n: show line numbers
    # -H: show file names
    # --no-heading: line per match format
    # --color=never: strip ANSI colors
    cmd = [rg_path, "-n", "-H", "--no-heading", "--color=never"]
    
    if ignore_case:
        cmd.append("-i")
    if not is_regex:
        cmd.append("-F")  # Treat query as literal string
        
    cmd.extend([query, target_dir])
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        matches = []
        if result.returncode in (0, 1):  # 0 = matches found, 1 = no matches found
            for line in result.stdout.splitlines():
                if not line.strip():
                    continue
                # rg format: <file>:<line>:<content>
                parts = line.split(":", 2)
                if len(parts) == 3:
                    matches.append({
                        "file": os.path.normpath(parts[0]),
                        "line": int(parts[1]),
                        "content": parts[2].strip()
                    })
            return matches, None
        else:
            return None, result.stderr or f"ripgrep returned status code {result.returncode}"
    except Exception as e:
        return None, str(e)

def search_with_python(query, target_dir, ignore_case, is_regex):
    matches = []
    
    # Prepare regex pattern
    flags = re.IGNORECASE if ignore_case else 0
    try:
        if is_regex:
            pattern = re.compile(query, flags)
        else:
            # Escape literal strings for regex search
            pattern = re.compile(re.escape(query), flags)
    except re.error as e:
        return None, f"Invalid regex pattern: {e}"
        
    # Walk the directory
    for root, _, files in os.walk(target_dir):
        for file in files:
            # We only search markdown (.md) files for Flat-File RAG
            if not file.endswith(".md"):
                continue
                
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    for line_num, line in enumerate(f, start=1):
                        if pattern.search(line):
                            matches.append({
                                "file": os.path.normpath(file_path),
                                "line": line_num,
                                "content": line.strip()
                            })
            except Exception:
                # Silently skip unreadable files to ensure robust execution
                continue
                
    return matches, None

def main():
    args = get_args()
    
    # Resolve the search directory
    # Determine the script's root path (parent of scripts directory)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.dirname(script_dir)
    
    target_path = os.path.abspath(os.path.join(workspace_root, args.dir))
    if not os.path.exists(target_path):
        print(f"Error: Target directory does not exist: {target_path}", file=sys.stderr)
        sys.exit(1)
        
    # Try locating ripgrep in system PATH
    rg_path = shutil.which("rg")
    
    if rg_path:
        matches, err = search_with_ripgrep(rg_path, args.query, target_path, args.ignore_case, args.regex)
        method = "ripgrep"
    else:
        matches, err = search_with_python(args.query, target_path, args.ignore_case, args.regex)
        method = "python_fallback"
        
    if err:
        print(f"Error executing search ({method}): {err}", file=sys.stderr)
        sys.exit(1)
        
    if args.json_output:
        print(json.dumps({
            "query": args.query,
            "directory": target_path,
            "search_method": method,
            "matches_count": len(matches),
            "matches": matches
        }, indent=2))
    else:
        # Print human-readable output
        print(f"--- Search Results (Method: {method}) ---")
        print(f"Query: '{args.query}' in '{os.path.relpath(target_path, workspace_root)}'\n")
        
        if not matches:
            print("No matches found.")
            return
            
        for match in matches:
            rel_file = os.path.relpath(match["file"], workspace_root)
            print(f"{rel_file}:{match['line']}: {match['content']}")
            
        print(f"\nTotal matches found: {len(matches)}")

if __name__ == "__main__":
    main()
