#!/bin/sh
set -eu

manager_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
target_dir=$(CDPATH= cd -- "$manager_dir/.." && pwd)
parent_dir=$(CDPATH= cd -- "$target_dir/.." && pwd)
manifest="$manager_dir/skills.txt"
cli_package="skills@1.7.0"
source_repo="mattpocock/skills"
mode=${1:-verify}
temp_root=
backup_dir=
transaction_file=

atomic_exchange() {
  left=$1
  right=$2
  python3 - "$left" "$right" <<'PY'
import ctypes
import os
import platform
import signal
import sys

left = os.fsencode(sys.argv[1])
right = os.fsencode(sys.argv[2])
signals = {signal.SIGHUP, signal.SIGINT, signal.SIGTERM}
old_mask = signal.pthread_sigmask(signal.SIG_BLOCK, signals)
try:
    libc = ctypes.CDLL(None, use_errno=True)
    system = platform.system()
    if system == "Darwin":
        exchange = libc.renameatx_np
        exchange.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
        result = exchange(-2, left, -2, right, 0x00000002)
    elif system == "Linux" and hasattr(libc, "renameat2"):
        exchange = libc.renameat2
        exchange.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
        result = exchange(-100, left, -100, right, 0x00000002)
    else:
        raise SystemExit(f"atomic directory exchange is unsupported on {system}")
    if result != 0:
        errno = ctypes.get_errno()
        raise OSError(errno, os.strerror(errno))
finally:
    signal.pthread_sigmask(signal.SIG_SETMASK, old_mask)
PY
}

tree_fingerprint() {
  python3 - "$1" <<'PY'
import hashlib
import os
import pathlib
import stat
import sys

root = pathlib.Path(sys.argv[1])
digest = hashlib.sha256()
root_info = root.lstat()
root_mode = f"{stat.S_IMODE(root_info.st_mode):o}".encode()
digest.update(b".\0root\0" + root_mode + b"\0")
for current, dirs, files in os.walk(root, followlinks=False):
    dirs.sort()
    files.sort()
    for name in dirs + files:
        path = pathlib.Path(current) / name
        info = path.lstat()
        relative = os.fsencode(path.relative_to(root).as_posix())
        mode = f"{stat.S_IMODE(info.st_mode):o}".encode()
        if stat.S_ISDIR(info.st_mode):
            kind, payload = b"directory", b""
        elif stat.S_ISREG(info.st_mode):
            kind, payload = b"file", path.read_bytes()
        elif stat.S_ISLNK(info.st_mode):
            kind, payload = b"symlink", os.fsencode(os.readlink(path))
        else:
            kind, payload = b"special", str(info.st_mode).encode()
        digest.update(relative + b"\0" + kind + b"\0" + mode + b"\0" + payload + b"\0")
print(digest.hexdigest())
PY
}

write_transaction() {
  old_fingerprint=$(tree_fingerprint "$target_dir")
  new_fingerprint=$(tree_fingerprint "$backup_dir")
  transaction_file="$temp_root/transaction"
  python3 - "$transaction_file" "$old_fingerprint" "$new_fingerprint" <<'PY'
import json
import os
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
temporary = path.with_suffix(".tmp")
with temporary.open("w") as file:
    json.dump({"old": sys.argv[2], "new": sys.argv[3]}, file, sort_keys=True)
    file.write("\n")
    file.flush()
    os.fsync(file.fileno())
os.replace(temporary, path)
directory = os.open(path.parent, os.O_RDONLY)
try:
    os.fsync(directory)
finally:
    os.close(directory)
PY
}

transaction_state() {
  test -n "$transaction_file" && test -f "$transaction_file" || {
    echo none
    return
  }
  test -e "$target_dir" && test -n "$backup_dir" && test -e "$backup_dir" || {
    echo unknown
    return
  }
  old_fingerprint=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["old"])' "$transaction_file")
  new_fingerprint=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["new"])' "$transaction_file")
  target_fingerprint=$(tree_fingerprint "$target_dir") || {
    echo unknown
    return
  }
  backup_fingerprint=$(tree_fingerprint "$backup_dir") || {
    echo unknown
    return
  }
  if [ "$target_fingerprint" = "$old_fingerprint" ]; then
    echo old
  elif [ "$target_fingerprint" = "$new_fingerprint" ] \
    && [ "$backup_fingerprint" = "$old_fingerprint" ]; then
    echo swapped
  else
    echo unknown
  fi
}

restore_transaction() {
  state=$(transaction_state)
  if [ "$state" = "swapped" ]; then
    atomic_exchange "$target_dir" "$backup_dir" || true
    state=$(transaction_state)
  fi
  if [ "$state" = "old" ]; then
    rm -f "$transaction_file"
    return 0
  fi
  echo "Could not confirm rollback; preserving recovery tree at $temp_root" >&2
  return 1
}

cleanup() {
  status=$?
  trap - EXIT HUP INT TERM
  preserve=false
  if [ -n "$transaction_file" ] && [ -e "$transaction_file" ]; then
    restore_transaction || preserve=true
  fi
  if [ "$preserve" = false ] && [ -n "$temp_root" ] && [ -d "$temp_root" ]; then
    rm -rf "$temp_root"
  fi
  exit "$status"
}
trap cleanup EXIT
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM

validate_location() {
  test "$(basename "$manager_dir")" = ".manager" \
    && test "$(basename "$target_dir")" = "matt" \
    && test "$manager_dir" = "$target_dir/.manager" || {
      echo "Refusing to manage unexpected target: $target_dir" >&2
      exit 1
    }
}

validate_manifest() {
  test -s "$manifest" || {
    echo "Missing or empty manifest: $manifest" >&2
    exit 1
  }

  invalid=$(grep -Ev '^[a-z0-9][a-z0-9-]*$' "$manifest" || true)
  test -z "$invalid" || {
    echo "Invalid skill name in $manifest: $invalid" >&2
    exit 1
  }

  duplicates=$(sort "$manifest" | uniq -d)
  test -z "$duplicates" || {
    echo "Duplicate skill in $manifest: $duplicates" >&2
    exit 1
  }
}

validate_tree() {
  tree=$1
  lock=$2
  content_lock=$3
  python3 - "$tree" "$manifest" "$lock" "$content_lock" "$source_repo" <<'PY'
import hashlib
import json
import os
import pathlib
import stat
import sys

tree = pathlib.Path(sys.argv[1])
manifest = pathlib.Path(sys.argv[2])
lock_path = pathlib.Path(sys.argv[3])
content_lock_arg = sys.argv[4]
source = sys.argv[5]
expected = [line.strip() for line in manifest.read_text().splitlines() if line.strip()]
expected_set = set(expected)

root_info = tree.lstat()
if not stat.S_ISDIR(root_info.st_mode):
    raise SystemExit(f"managed tree is not a directory: {tree}")
for root, dirs, files in os.walk(tree, followlinks=False):
    for entry in dirs + files:
        path = pathlib.Path(root) / entry
        info = path.lstat()
        if stat.S_ISLNK(info.st_mode):
            raise SystemExit(f"unexpected symlink in managed tree: {path}")
        if not stat.S_ISDIR(info.st_mode) and not stat.S_ISREG(info.st_mode):
            raise SystemExit(f"unexpected filesystem entry in managed tree: {path}")

root_entries = {child.name for child in tree.iterdir() if child.name != ".manager"}
actual = sorted(
    child.name
    for child in tree.iterdir()
    if stat.S_ISDIR(child.lstat().st_mode) and child.name != ".manager"
)
if root_entries != expected_set or actual != sorted(expected):
    missing = sorted(expected_set - set(actual))
    extra = sorted(root_entries - expected_set)
    raise SystemExit(f"managed skill mismatch; missing={missing}, extra={extra}")

for name in expected:
    skill_file = tree / name / "SKILL.md"
    if not skill_file.is_file():
        raise SystemExit(f"missing {skill_file}")
    frontmatter_name = None
    frontmatter_closed = False
    lines = skill_file.read_text().splitlines()
    if not lines or lines[0] != "---":
        raise SystemExit(f"missing frontmatter in {skill_file}")
    for line in lines[1:]:
        if line == "---":
            frontmatter_closed = True
            break
        if line.startswith("name:"):
            frontmatter_name = line.split(":", 1)[1].strip()
    if not frontmatter_closed:
        raise SystemExit(f"unclosed frontmatter in {skill_file}")
    if frontmatter_name != name:
        raise SystemExit(
            f"frontmatter name mismatch in {skill_file}: {frontmatter_name!r}"
        )

lock = json.loads(lock_path.read_text())
locked = lock.get("skills", {})
if set(locked) != expected_set:
    raise SystemExit(
        f"lockfile skill mismatch; missing={sorted(expected_set - set(locked))}, "
        f"extra={sorted(set(locked) - expected_set)}"
    )
for name, record in locked.items():
    if record.get("source") != source:
        raise SystemExit(f"unexpected source for {name}: {record.get('source')!r}")

def hash_skill(path):
    digest = hashlib.sha256()
    root_mode = f"{path.stat().st_mode & 0o7777:o}".encode()
    digest.update(b".\0root\0" + root_mode + b"\0")
    for item in sorted(path.rglob("*")):
        relative = item.relative_to(path).as_posix().encode()
        kind = b"directory" if item.is_dir() else b"file"
        mode = f"{item.stat().st_mode & 0o7777:o}".encode()
        digest.update(relative + b"\0" + kind + b"\0" + mode + b"\0")
        if item.is_file():
            digest.update(item.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()

if content_lock_arg != "-":
    content_lock = json.loads(pathlib.Path(content_lock_arg).read_text())
    if set(content_lock) != expected_set:
        raise SystemExit("content lock skill set does not match skills.txt")
    for name in expected:
        actual_hash = hash_skill(tree / name)
        if actual_hash != content_lock[name]:
            raise SystemExit(f"unrecorded managed-file change in {name}")
PY
}

write_content_lock() {
  tree=$1
  output=$2
  python3 - "$tree" "$manifest" "$output" <<'PY'
import hashlib
import json
import pathlib
import sys

tree = pathlib.Path(sys.argv[1])
manifest = pathlib.Path(sys.argv[2])
output = pathlib.Path(sys.argv[3])

result = {}
for name in (line.strip() for line in manifest.read_text().splitlines()):
    if not name:
        continue
    skill = tree / name
    digest = hashlib.sha256()
    root_mode = f"{skill.stat().st_mode & 0o7777:o}".encode()
    digest.update(b".\0root\0" + root_mode + b"\0")
    for item in sorted(skill.rglob("*")):
        relative = item.relative_to(skill).as_posix().encode()
        kind = b"directory" if item.is_dir() else b"file"
        mode = f"{item.stat().st_mode & 0o7777:o}".encode()
        digest.update(relative + b"\0" + kind + b"\0" + mode + b"\0")
        if item.is_file():
            digest.update(item.read_bytes())
        digest.update(b"\0")
    result[name] = digest.hexdigest()
output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
PY
}

validate_patches_applied() {
  tree=$1
  patches_dir=$2
  found=false
  for patch_file in "$patches_dir"/*.patch; do
    test -e "$patch_file" || continue
    found=true
    if ! patch --batch --dry-run -F 0 -R -p1 -d "$tree" < "$patch_file" >/dev/null; then
      echo "Local patch is not present in the managed tree: $patch_file" >&2
      return 1
    fi
  done
  if [ "$found" = false ]; then
    echo "No local patches found." >&2
  fi
}

apply_patches() {
  tree=$1
  patches_dir=$2
  for patch_file in "$patches_dir"/*.patch; do
    test -e "$patch_file" || continue
    echo "Applying $(basename "$patch_file")"
    patch --batch --forward -F 0 -p1 -d "$tree" < "$patch_file"
  done
}

build_candidate() {
  temp_root=$(mktemp -d "$parent_dir/.matt-manager.XXXXXX")
  install_root="$temp_root/install"
  candidate_dir="$temp_root/matt"
  mkdir -p "$install_root" "$candidate_dir/.manager"

  set -- add "$source_repo" --agent pi --copy --yes
  while IFS= read -r skill; do
    set -- "$@" --skill "$skill"
  done < "$manifest"

  (cd "$install_root" && npx --yes "$cli_package" "$@")

  installed="$install_root/.pi/skills"
  test -d "$installed" || {
    echo "Installer did not produce $installed" >&2
    exit 1
  }
  cp -R "$installed/". "$candidate_dir/"

  cp "$manager_dir/manage.sh" "$candidate_dir/.manager/manage.sh"
  cp "$manager_dir/README.md" "$candidate_dir/.manager/README.md"
  cp "$manager_dir/test-harnesses.py" "$candidate_dir/.manager/test-harnesses.py"
  cp "$manager_dir/skills.txt" "$candidate_dir/.manager/skills.txt"
  cp -R "$manager_dir/patches" "$candidate_dir/.manager/patches"
  cp "$install_root/skills-lock.json" "$candidate_dir/.manager/skills-lock.json"
  chmod +x "$candidate_dir/.manager/manage.sh"

  apply_patches "$candidate_dir" "$candidate_dir/.manager/patches"
  validate_tree "$candidate_dir" "$candidate_dir/.manager/skills-lock.json" -
  write_content_lock "$candidate_dir" "$candidate_dir/.manager/content-lock.json"
  validate_tree "$candidate_dir" "$candidate_dir/.manager/skills-lock.json" "$candidate_dir/.manager/content-lock.json"
  validate_patches_applied "$candidate_dir" "$candidate_dir/.manager/patches"
}

verify_current() {
  validate_tree "$target_dir" "$manager_dir/skills-lock.json" "$manager_dir/content-lock.json"
  validate_patches_applied "$target_dir" "$manager_dir/patches"
  echo "Verified $(wc -l < "$manifest" | tr -d ' ') managed Matt skills."
}

replace_current() {
  candidate_dir="$temp_root/matt"
  backup_dir="$candidate_dir"
  write_transaction

  if ! atomic_exchange "$target_dir" "$candidate_dir"; then
    state=$(transaction_state)
    test "$state" = "swapped" || exit 1
  fi
  if ! "$target_dir/.manager/manage.sh" verify; then
    if restore_transaction; then
      echo "Post-install verification failed; restored previous installation." >&2
    fi
    exit 1
  fi

  rm -f "$transaction_file"
  transaction_file=
  rm -rf "$backup_dir"
  backup_dir=
  echo "Installed $(wc -l < "$target_dir/.manager/skills.txt" | tr -d ' ') managed Matt skills."
}

harness_links() {
  python3 - "$target_dir" "$manifest" "$mode" <<'PY'
import os
import pathlib
import sys

source = pathlib.Path(sys.argv[1])
names = pathlib.Path(sys.argv[2]).read_text().splitlines()
check = sys.argv[3] == "verify-harnesses"
destinations = [pathlib.Path.home() / harness / "skills" for harness in (".claude", ".gemini")]
links = [(destination / name, source / name) for destination in destinations for name in names]

# Preflight every destination before creating any links.
errors = []
for destination in destinations:
    if os.path.lexists(destination) and (destination.is_symlink() or not destination.is_dir()):
        errors.append(f"expected a real skills directory: {destination}")
for link, target in links:
    if not (target / "SKILL.md").is_file():
        errors.append(f"missing skill: {target / 'SKILL.md'}")
    if os.path.lexists(link):
        if not link.is_symlink() or link.resolve() != target.resolve():
            errors.append(f"refusing to overwrite existing entry: {link}")
    elif check:
        errors.append(f"missing harness link: {link}")
if errors:
    raise SystemExit("\n".join(errors))

created = 0
if not check:
    for link, target in links:
        link.parent.mkdir(parents=True, exist_ok=True)
        if not os.path.lexists(link):
            link.symlink_to(target, target_is_directory=True)
            created += 1
for link, target in links:
    if not link.is_symlink() or link.resolve() != target.resolve():
        raise SystemExit(f"invalid harness link: {link}")
    if (link / "SKILL.md").read_bytes() != (target / "SKILL.md").read_bytes():
        raise SystemExit(f"skill content mismatch: {link}")
print(f"Verified {len(links)} Matt skill links for Claude and Gemini. Created {created} links.")
PY
}

validate_location
validate_manifest

case "$mode" in
  install|update)
    build_candidate
    replace_current
    ;;
  check)
    verify_current >/dev/null
    build_candidate
    candidate_manager_fingerprint=$(tree_fingerprint "$temp_root/matt/.manager")
    current_manager_fingerprint=$(tree_fingerprint "$manager_dir")
    if cmp -s "$temp_root/matt/.manager/content-lock.json" "$manager_dir/content-lock.json" \
      && cmp -s "$temp_root/matt/.manager/skills-lock.json" "$manager_dir/skills-lock.json" \
      && [ "$candidate_manager_fingerprint" = "$current_manager_fingerprint" ]; then
      echo "Managed Matt skills are up to date."
    else
      echo "Managed Matt skills differ from the latest staged installation."
      diff -qr -x .manager "$temp_root/matt" "$target_dir" || true
      diff -qr "$temp_root/matt/.manager" "$manager_dir" || true
      exit 1
    fi
    ;;
  verify)
    verify_current
    ;;
  link-harnesses|verify-harnesses)
    verify_current
    harness_links
    ;;
  *)
    echo "Usage: $0 [install|update|check|verify|link-harnesses|verify-harnesses]" >&2
    exit 2
    ;;
esac
