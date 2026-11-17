# Frontend rules

Apply these within the requested scope and existing design system. These rules do not authorize adding features.

## Interface rules

- Keep the interface minimal and information-dense. Let the UI communicate state; remove redundant labels, commentary, repeated titles or numbers, duplicate icons, and data already evident from adjacent content.
- Establish clear hierarchy and readable contrast. Keep text vertically aligned with neighboring icons and controls; align actions consistently.
- Use deliberate spacing and padding. Avoid oversized gaps, cramped sheets, and unnecessary scrolling. Use remaining space intentionally; make scrollable content end with breathing room.
- Use concentric corner radii for nested surfaces. Do not prescribe platform-specific APIs when working across platforms; follow each platform's native conventions.
- Make pills hug their content and keep short labels on one line when space permits. A compound action should read as one control (for example, action plus chevron), not a row of duplicate controls.
- Use lining numerals where appropriate; compare font variants when typography materially affects hierarchy, and typeset mathematics correctly.
- Keep related states within one color family, with weaker states lighter; use a consistent subdued grey for inactive states. Do not rely on color alone to communicate meaning.
- Put secondary information (hints, explanations, learn-more content) behind a disclosure when it should not dominate the primary task.
- Use standard platform and UI terminology. Briefly translate a user's informal description into the standard pattern name where helpful.
- Avoid Liquid Glass, new hand-drawn decorations, and liquid/sloshing gauges. Do not add new illustrative art unless explicitly requested; existing product artwork can remain. Do not overuse progress bars.
- Motion must not jump, snap unexpectedly, reflow content over text, or obscure controls. Check entrances and exits and scroll both down and back up.
- Preserve honest state semantics. Do not show an action as complete when it failed, is pending, or still needs approval.

## Shared behavior

- Keep layout stable across filtering, empty, loading, and populated states.
- Prefer proven components that supply the required interaction, keyboard, focus, and dismissal behavior.
- Reuse the same component for the same action across views.
- Actions operate on the relevant view's filters, sorting, selection, and ranking unless the specification says otherwise.
- Keep complete underlying data separate from compact presentation.
- Use visible separators between distinct action groups when needed.

## Examples

These are schematic examples, not required component names, APIs, or features. Apply them only when the corresponding concern exists. Example codes remain stable.

### E1 — Remove redundant information

Good:

```tsx
<section>
  <header className="flex items-center justify-between">
    <h1>Projects</h1>
    <span>{projects.length} results</span>
  </header>
  <ProjectFilters />
  <ProjectGrid projects={projects} />
</section>
```

Bad:

```tsx
<section>
  <span>Workspace</span>
  <h1>Explore projects</h1>
  <p>Discover your next opportunity</p>
  <span>The collection</span>
  <span>Grid view</span>
  <h2>Projects</h2>
  <span>{projects.length} results</span>
  <p>Search and filter the projects below.</p>
  <ProjectFilters />
  <ProjectGrid projects={projects} />
</section>
```

The bad version adds several labels without adding information or actions.

### E2 — Keep spacing and layout stable

Good: Applying a category filter updates the results without moving the search controls or the top of the results grid. Empty-tier text is centered within its row.

Bad: A filter-summary row appears and pushes the grid down. Clearing the filter moves everything back. Empty-tier text sits near the top because it inherited card padding.

### E3 — Use proven interaction components

Good: A multi-select filter uses an established menu component with checkbox items. It stays open for multiple selections, supports keyboard navigation, and returns focus appropriately when dismissed.

Bad: A styled `div` imitates a dropdown but has no keyboard behavior. Alternatively, the project installs shadcn but leaves the requested multi-select interaction implemented as a native single-select control.

### E4 — Reuse controls without mixing their data

Good:

```tsx
<ExportMenu items={filteredSortedProjects} />
<ExportMenu items={projectsInTierOrder} />
```

Bad:

```tsx
// Separate implementations drift in labels and supported formats.
<ProjectExportButtons />
<TierExportDropdown />

// Or both export everything, ignoring the current view.
<ExportMenu items={allProjects} />
```

### E5 — Keep full data behind compact presentation

Good: A project card displays code, title, and a short summary. "All details" exports the complete record. "Code and name" deliberately exports a reduced representation.

Bad: The application truncates descriptions when loading data, then exports those truncated strings under "All details."

### E6 — Group actions visibly

Good:

```tsx
<DropdownMenuContent>
  <DropdownMenuItem onSelect={copyJson}>Copy JSON</DropdownMenuItem>
  <DropdownMenuItem onSelect={copyMarkdown}>Copy Markdown</DropdownMenuItem>
  <DropdownMenuSeparator />
  <DropdownMenuItem onSelect={downloadJson}>Download JSON</DropdownMenuItem>
  <DropdownMenuItem onSelect={downloadMarkdown}>Download Markdown</DropdownMenuItem>
</DropdownMenuContent>
```

Bad:

```tsx
<DropdownMenuContent>
  <DropdownMenuItem onSelect={copyJson}>Copy JSON</DropdownMenuItem>
  <DropdownMenuItem onSelect={copyMarkdown}>Copy Markdown</DropdownMenuItem>
  <div className="h-6" />
  <DropdownMenuItem onSelect={downloadJson}>Download JSON</DropdownMenuItem>
  <DropdownMenuItem onSelect={downloadMarkdown}>Download Markdown</DropdownMenuItem>
</DropdownMenuContent>
```

### E8 — Make state truthful and motion stable

Good: Saving shows a pending state, then success only after confirmation. Failure keeps the user's input and offers retry. Opening a menu doesn't shift nearby controls.

Bad: Show "Saved" immediately, even if persistence fails. Insert a spinner that moves the button label and neighboring actions.
