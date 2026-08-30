---
name: vault-tagger
description: Tag notes in an Obsidian-style vault with appropriate category tags. Use this skill whenever the user asks to tag, categorize, clean up, organize, or add tags to notes in their vault. Also use when the user mentions tagging notes, vault cleanup, or organizing notes with tags. Applies to any markdown-based note vault system (Obsidian, Logseq, etc.).
---

# Vault Tagger

This skill tags notes in a vault with appropriate category tags based on a tag guide.

## Workflow

### Step 1: Find the tag guide

Look for a file named something like "A Guide to Tags" or "Tags and Links" in the Notes directory. Read it to understand available tags. Common patterns:
- `@Notes/A Guide to Tags and Links*.md`
- `@Notes/Tag Guide*.md`

If the user provides a specific guide file via @ reference, use that directly.

### Step 2: Find all notes to tag

Use the glob tool to find all .md files in the Notes directory:
```
Notes/*.md
```

Exclude the tag guide itself from tagging.

### Step 3: Read and analyze each note

For each note file:
1. Read the file content
2. Determine which tags from the guide apply based on content:
   - School courses → use `#2526s2/course` format (e.g., `#2526s2/cs2105`, `#2526s2/nst2062`)
   - Projects → `#project`
   - UROP → `#urop`
   - Hackathons → `#hackathon`
   - Job search → `#jobsearch`
   - Entrepreneurship → `#entrepreneurship`
   - Communication → `#communication`
   - NUSWS → `#nusws`
   - TechD → `#techd`
   - Marimo → `#marimo`
   - Leetcode → `#leetcode`
   - Obsidian tips → `#obsidian`
   - Blog posts → `#blog`
   - If no category fits → `#no-tag`

### Step 4: Apply tags

**Tag placement:**
- Place tags on the line immediately after the title (the `# Title` line)
- Format: `> #tag1 #tag2` on a single line in the summary block
- Example:
  ```markdown
  > [! SUMMARY] Gist
  >
  > #tag1 #tag2

  # Note Title
  ```

**If note already has tags:**
- Remove existing tags that are NOT in the tag guide
- Replace with appropriate guide tags
- Keep tags where they currently are in the file

**Multiple tags:**
- Only use multiple tags if the note genuinely covers multiple topics
- Most notes should have 1-2 tags max

### Step 5: Edit each note

Use the edit tool to modify each note file:
1. Find the existing summary block (lines with `> [! SUMMARY]`)
2. Add/replace tags on the line after `> [! SUMMARY] Gist` or after `>`

## Important Rules

1. ** ONLY use tags from the guide** - no new tags allowed
2. **Every note must have a tag** - use `#no-tag` if nothing fits
3. **Remove old tags** - replace deprecated tags (like `0_code/*`, `1_context/*`, etc.) with guide tags
4. **Tag placement** - always in the summary block, right after the title