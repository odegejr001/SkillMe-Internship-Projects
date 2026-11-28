import argparse
import hashlib
import time
from pathlib import Path

CHUNK_SIZE = 4096


def hash_file(path, algorithm="sha256"):
    """Return a hexadecimal hash for a file."""
    hasher = hashlib.new(algorithm)
    with open(path, "rb") as file:
        while chunk := file.read(CHUNK_SIZE):
            hasher.update(chunk)
    return hasher.hexdigest()


def filewatch(folder="test_folder", algorithm="sha256", interval=1):
    """Monitor files and report changed hashes until interrupted."""
    folder = Path(folder)
    if not folder.exists():
        print(f"Error: folder not found: {folder}")
        return
    if not folder.is_dir():
        print(f"Error: not a directory: {folder}")
        return

    previous = {}
    print(f"Watching {folder} with {algorithm.upper()} (Ctrl+C to stop)")

    try:
        while True:
            current = {}
            try:
                files = sorted(path for path in folder.iterdir() if path.is_file())
            except OSError as error:
                print(f"Error: could not list folder: {error}")
                time.sleep(interval)
                continue

            for path in files:
                try:
                    digest = hash_file(path, algorithm)
                except (FileNotFoundError, PermissionError, OSError) as error:
                    print(f"  UNREADABLE  {path.name}: {error}")
                    continue

                current[path.name] = digest
                if path.name not in previous:
                    status = "NEW"
                elif previous[path.name] == digest:
                    status = "UNCHANGED"
                else:
                    status = "CHANGED"
                print(f"  {status:9} {path.name}: {digest}")

            previous = current
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nFile watch stopped.")


def main():
    parser = argparse.ArgumentParser(description="Watch files and detect hash changes.")
    parser.add_argument("folder", nargs="?", default="test_folder")
    parser.add_argument("-a", "--algorithm", choices=("sha256", "sha1"), default="sha256")
    parser.add_argument("-i", "--interval", type=float, default=1)
    args = parser.parse_args()
    filewatch(args.folder, args.algorithm, args.interval)


if __name__ == "__main__":
    main()
