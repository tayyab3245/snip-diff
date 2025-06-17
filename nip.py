import os
import json
import difflib
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

SNAPSHOT_FILE = ".nip_snapshot.json"
IGNORE_LIST = ["build", "dist", ".git", "node_modules", "__pycache__"]


def get_all_files(directory):
    files = {}
    for root, _, filenames in os.walk(directory):
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
                pass
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


class NipGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("NIP - Not-Important-Pseudo-git")
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=40)
        self.text_area.pack(padx=10, pady=10)

        button_frame = tk.Frame(root)
        button_frame.pack(pady=5)

        tk.Button(button_frame, text="Choose Folder", command=self.choose_folder).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Copy Output", command=self.copy_output).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Undo Snapshot", command=self.undo_snapshot).pack(side=tk.LEFT, padx=5)

        self.folder_path = None

    def choose_folder(self):
        self.folder_path = filedialog.askdirectory()
        if self.folder_path:
            old_snapshot = load_snapshot()
            new_snapshot = get_all_files(self.folder_path)
            result = format_output(old_snapshot, new_snapshot)
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, result)
            save_snapshot(new_snapshot)

    def copy_output(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.text_area.get(1.0, tk.END))
        messagebox.showinfo("Copied", "Output copied to clipboard.")

    def undo_snapshot(self):
        if os.path.exists(SNAPSHOT_FILE):
            os.remove(SNAPSHOT_FILE)
            messagebox.showinfo("Undo", "Snapshot removed. Run again to re-capture.")
        else:
            messagebox.showinfo("Undo", "No snapshot file to remove.")


def main():
    root = tk.Tk()
    app = NipGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
