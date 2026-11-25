import argparse
import hashlib
import json
from pathlib import Path
from logo import BANNER

print(BANNER)

CHUNK_SIZE = 4096
SNAPSHOT_FILE = Path(__file__).with_name(".hash_snapshot.json")


def hash_file(path, algorithm="sha256"):
    """Reads the path in binary chunks and return its hexadecimal digest."""
    hasher = hashlib.new(algorithm)
    with open(path, "rb") as file:
        while chunk := file.read(CHUNK_SIZE):
            hasher.update(chunk)
    return hasher.hexdigest()


def load_snapshot():
    try:
        with SNAPSHOT_FILE.open("r", encoding="utf-8"):
            pass
    except FileNotFoundError:
        return None
    except OSError as error:
        print(f"Warning: could not read snapshot: {error}")
        return None

    try:
        with SNAPSHOT_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError) as error:
        print(f"Warning: snapshot is unreadable: {error}")
        return None


def save_snapshot(snapshot):
    try:
        with SNAPSHOT_FILE.open("w", encoding="utf-8") as file:
            json.dump(snapshot, file, indent=2)
    except OSError as error:
        print(f"Warning: could not save snapshot: {error}")


def main():
    parser = argparse.ArgumentParser(description="Hash files in a folder.")
    parser.add_argument("folder", nargs="?", default="test_folder", help="Folder to scan")
    parser.add_argument("-a", "--algorithm", choices=("sha256", "sha1"), default="sha256")
    args = parser.parse_args()

    folder = Path(args.folder)
    if not folder.exists():
        print(f"Error: folder not found: {folder}")
        return
    if not folder.is_dir():
        print(f"Error: not a directory: {folder}")
        return

    previous = load_snapshot()
    previous_hashes = {}
    if previous and previous.get("algorithm") == args.algorithm:
        previous_hashes = previous.get("hashes", {})

    current = {"algorithm": args.algorithm, "hashes": {}}
    print(f"Scanning {folder} with {args.algorithm.upper()}:")

    try:
        files = sorted(path for path in folder.iterdir() if path.is_file())
    except OSError as error:
        print(f"Error: could not list folder: {error}")
        return

    for path in files:
        try:
            digest = hash_file(path, args.algorithm)
        except FileNotFoundError:
            print(f"  MISSING  {path.name}")
            continue
        except PermissionError:
            print(f"  UNREADABLE  {path.name}")
            continue
        except OSError as error:
            print(f"  UNREADABLE  {path.name}: {error}")
            continue

        key = path.name
        current["hashes"][key] = digest
        old_digest = previous_hashes.get(key)
        if old_digest is None:
            status = "NEW"
        elif old_digest == digest:
            status = "UNCHANGED"
        else:
            status = "CHANGED"
        print(f"  {status:9} {path.name}: {digest}")

    save_snapshot(current)


if __name__ == "__main__":
    main()
