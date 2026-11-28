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

## DISCLAIMER || Legal and Ethical Use

**Only use this project on files and folders you own or are explicitly authorized to monitor.** Scanning, modifying, or monitoring systems without permission may violate local laws, organizational policies, or contracts. This tool is provided strictly for authorized cybersecurity education and defensive integrity checking in this workspace.

- Do not test or monitor another person's data without written permission.
- Keep test files local and avoid collecting unrelated personal or sensitive data.
- Use the results to detect changes, not to access or disclose protected information.

## Files

- `hash_files.py` — hashes every file in a selected folder and compares results with the previous saved snapshot.
- `filewatch.py` — continuously watches a folder and reports `NEW`, `UNCHANGED`, or `CHANGED` hashes using `hash_file()`.
- `test_folder/` — contains small text files for authorized testing.
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

Both commands would return the same hexadecimal digest as the script would for thesame file

## Avalanche effect on `bravo.txt`

Changing even a small part of `bravo.txt` causes a completely different SHA-256 digest. This is the avalanche effect: a tiny input change produces widespread, seemingly random-looking changes in the output.

![SHA-256 avalanche effect demonstration for bravo.txt](<Screenshot 2026-11-28 023232.png>)

The screenshot demonstrates that the original and modified versions of `bravo.txt` have unrelated-looking 64-character hashes, even though the file contents differ only slightly.

## File Watcher

Run the continuous file watcher:

```powershell
python filewatch.py
```

It watches `test_folder` with SHA-256. Press `Ctrl+C` to stop it. To choose another folder, algorithm, or polling interval:

```powershell
python filewatch.py test_folder --algorithm sha256 --interval 1
python filewatch.py test_folder --algorithm sha1
```

The watcher is a demonstration of defensive file integrity monitoring. It compares hashes observed during consecutive polls; it does not identify which person or process made a change.