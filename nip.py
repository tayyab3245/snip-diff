import os
import json
import difflib

SNAPSHOT_FILE = ".snapshot.json"
IGNORE_LIST = ["build", "dist", ".git", "node_modules", "__pycache__"]


def get_all_files(directory):
    files = {}
    for root, _, filenames in os.walk(directory):
        # Skip ignored directories
        if any(ignored in root for ignored in IGNORE_LIST):
            continue
        for filename in filenames:
            path = os.path.join(root, filename)
            rel_path = os.path.relpath(path, directory)
            if any(part in IGNORE_LIST for part in rel_path.split(os.sep)):
                continue
            try:
                with open(path, "r", encoding="utf-8") as f:
                    files[rel_path] = {
                        "content": f.read(),
                        "mtime": os.path.getmtime(path)
                    }
            except Exception:
                pass  # skip unreadable files
    return files


def load_snapshot():
    if not os.path.exists(SNAPSHOT_FILE):
        return {}
    with open(SNAPSHOT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_snapshot(snapshot):
    simple_snapshot = {k: v["content"] if isinstance(v, dict) else v for k, v in snapshot.items()}
    with open(SNAPSHOT_FILE, "w", encoding="utf-8") as f:
        json.dump(simple_snapshot, f, indent=2)


def diff_files(old, new):
    return list(difflib.unified_diff(
        old.splitlines(), new.splitlines(), lineterm=""
    ))


def format_output(old_snapshot, new_snapshot):
    output = []
    sorted_paths = sorted(new_snapshot.items(), key=lambda x: -x[1].get("mtime", 0))
    sorted_paths = [p[0] for p in sorted_paths]
    all_paths = set(old_snapshot.keys()) | set(new_snapshot.keys())

    sorted_all = sorted(all_paths, key=lambda p: -new_snapshot.get(p, {}).get("mtime", 0))

    for path in sorted_all:
        output.append("-----------------------")
        output.append(path)

        old_content = old_snapshot.get(path, "")
        new_content = new_snapshot.get(path, {}).get("content", None)

        if new_content is None:
            output.append("(deleted)")
        elif old_content == new_content:
            output.append(new_content)
        elif old_content == "":
            output.append(new_content)
        else:
            diff = diff_files(old_content, new_content)
            output.extend(diff)
        output.append("-----------------------")

    return "\n".join(output)


def main():
    directory = input("Enter the directory to scan: ").strip()
    old_snapshot = load_snapshot()
    new_snapshot = get_all_files(directory)

    result = format_output(old_snapshot, new_snapshot)
    print("\n" + result)

    save_snapshot(new_snapshot)


if __name__ == "__main__":
    main()
