```text
██╗  ██╗ █████╗ ███████╗██╗  ██╗ █████╗ ███╗   ███╗
██║  ██║██╔══██╗██╔════╝██║  ██║██╔══██╗████╗ ████║
███████║███████║███████╗███████║███████║██╔████╔██║
██╔══██║██╔══██║╚════██║██╔══██║██╔══██║██║╚██╔╝██║
██║  ██║██║  ██║███████║██║  ██║██║  ██║██║ ╚═╝ ██║
╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝
═══════════════════════════════════════════════════
   SHA-256 File Hashing in Python · SkillMe Week 1
   Internship Project.
   One tiny change, a completely different hash
═══════════════════════════════════════════════════
                          By: odegejr
                          Socials: @odegejrofficial
```

# **Hasham Documentation**
Hasham Python script calculates cryptographic hashes for text or binary files in a folder. It reads each file in 4096-byte chunks so it uses a small amount of memory even for large files.

## DISCLAIMER || Legal and Ethical use.

**Scanning or attacking systems you do not own or do not have written permission to test is illegal.** This tool only monitors files in this workspace's own `test_folder`; use it on test data you control.

## Files

- `hash_files.py` — hashes every file in the selected folder and compares the result with the previous run.
- `test_folder/` — contains six small text files for testing.
- `.hash_snapshot.json` — automatically stores the previous hashes outside `test_folder`.

## Run

From the project folder:

```powershell
python hash_files.py
```

By default, the script scans `test_folder` and uses SHA-256. It prints `NEW` on the first run, `UNCHANGED` when a hash is identical, and `CHANGED` after a file's contents change.

## Stretch option: SHA-1

```powershell
python hash_files.py --algorithm sha1
```

**NB** Both SHA-256 and SHA-1 are available. I recommend SHA-256 for new file-integrity applications because it has a larger digest and stronger resistance to practical collision attacks. SHA-1 is included for comparison and practice only and should not be used for security-sensitive verification.

## Proof of concept.

Windows
```powershell
certutil -hashfile test_folder\bravo.txt SHA256
```

Linux
```bash
sha256sum test_folder/bravo.txt
```

Both commands would return the same hexadecimal digest as the script.