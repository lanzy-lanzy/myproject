# Using LABB Components with AI Assistants

This guide explains how to work with LABB components when using AI assistants such as ChatGPT, Codex, Cursor, Copilot, Cline, Windsurf, Gemini, or similar tools.

It is based on the official LABB LLM reference:

- Web reference: `https://labb.io/docs/guide/references/llms.txt/`
- Raw reference endpoint: `https://labb.io/llms.txt`
- Local saved copy in this project: `docs/labb-llms-reference.md`

Use this guide together with the saved reference file. The saved reference contains the compact source-of-truth component notes, while this guide explains how to apply those notes in AI-assisted development.

## 1. Core Rule: Do Not Ask AI to Guess LABB Syntax

LABB components have specific component names, parameter names, enum values, sub-component names, icon conventions, and reactive variants. AI assistants can write good LABB code only when they have accurate component documentation.

The safest workflow is:

1. Give the AI the LABB LLM reference.
2. Ask the AI to inspect the component before writing code.
3. Ask the AI to use examples from the CLI.
4. Ask the AI to avoid guessed prop names and guessed icons.
5. Rebuild CSS and run Django checks after changes.

Bad prompt:

```text
Make me a nice LABB card with buttons.
```

Better prompt:

```text
Use docs/labb-llms-reference.md and inspect the LABB card and button components before editing.
Create a project card using valid LABB component props only.
Use labb components inspect card, labb components inspect button, and labb components ex card before implementing.
Do not guess parameter names.
```

## 2. Files to Give an AI Assistant

When asking an AI to work on LABB frontend code, provide these project files:

```text
docs/labb-llms-reference.md
labb.yaml
static_src/input.css
static/css/output.css
myproject/settings.py
portfolio/templates/portfolio/base.html
portfolio/urls.py
```

If the work involves custom Cotton components, also provide:

```text
portfolio/templates/cotton/
portfolio/templates/cotton/component/
```

If the work involves a specific page, provide that page template too:

```text
portfolio/templates/portfolio/home.html
portfolio/templates/portfolio/projects.html
portfolio/templates/portfolio/contact.html
```

## 3. How to Save and Refresh the LABB LLM Reference

The raw LABB reference was saved locally with:

```powershell
Invoke-WebRequest -Uri 'https://labb.io/llms.txt' -UseBasicParsing -OutFile 'docs\labb-llms-reference.md'
```

You can also generate the reference through the LABB CLI:

```powershell
uv run labb llms > docs\labb-llms-reference.md
```

Refresh it whenever LABB is upgraded:

```powershell
uv run labb llms > docs\labb-llms-reference.md
```

Then commit or keep the refreshed file with the project so AI assistants can read the correct version.

## 4. CLI Commands AI Assistants Should Use

### 4.1 Show LABB CLI Help

```powershell
uv run labb --help
```

Useful commands include:

```text
init
setup
config
build
dev
llms
scan
icons
components
```

### 4.2 Show Current LABB Config

```powershell
uv run labb config
```

Use this before changing build paths. In this project, `labb.yaml` maps:

```text
input: static_src/input.css
output: static/css/output.css
scan output: static_src/labb-classes.txt
```

### 4.3 Scan Templates

```powershell
uv run labb scan
```

This scans Django templates and Cotton components, then writes extracted LABB classes to:

```text
static_src/labb-classes.txt
```

Run this after adding or changing LABB components.

### 4.4 Build CSS

```powershell
uv run labb build
```

Alternative direct Tailwind command:

```powershell
& 'C:\nvm4w\nodejs\npx.cmd' @tailwindcss/cli -i static_src\input.css -o static\css\output.css --minify
```

Run this after:

- Editing `static_src/input.css`.
- Adding Tailwind classes to templates.
- Adding LABB components that introduce classes.
- Changing DaisyUI themes.

### 4.5 Inspect a Component

```powershell
uv run labb components inspect button
```

Use this to get:

- Component description.
- Template path.
- Base classes.
- Variables.
- Types.
- Defaults.
- Valid enum values.
- Icon modifiers.
- Reactive props.

### 4.6 View Component Examples

List examples:

```powershell
uv run labb components ex button
```

View one example:

```powershell
uv run labb components ex button with-icons
```

View multiple examples:

```powershell
uv run labb components ex button variants sizes with-icons
```

Browse all examples:

```powershell
uv run labb components ex --tree
```

### 4.7 Search Icons

```powershell
uv run labb icons search "arrow"
```

Get icon details:

```powershell
uv run labb icons info rmx.arrow-right
```

List icon packs:

```powershell
uv run labb icons packs
```

## 5. Component Inspection Workflow for AI

Use this workflow whenever an AI assistant needs to add a LABB component:

```powershell
uv run labb components inspect <component>
uv run labb components ex <component>
uv run labb components ex <component> <specific-example>
```

Then ask the AI to write code using only the inspected props.

Example for a button:

```powershell
uv run labb components inspect button
uv run labb components ex button with-icons
```

The inspected button component includes props such as:

```text
as
variant
btnStyle
behavior
size
modifier
icon
icon.fill
icon.end
icon.class
class
```

This means an AI should use:

```django
<c-lb.button variant="primary" btnStyle="outline" size="sm">
    View Project
</c-lb.button>
```

Not:

```django
<c-lb.button color="primary" style="outline" small>
    View Project
</c-lb.button>
```

The second example guesses props that are not guaranteed to exist.

## 6. How to Reference LABB Components in AI Prompts

A good LABB prompt should include:

- The relevant template path.
- The component name.
- The exact UI goal.
- The required CLI inspection commands.
- Whether icons are allowed.
- Whether reactive `.x` components are needed.
- A build and verification checklist.

Prompt template:

```text
You are editing a Django project that uses LABB, Django Cotton, Tailwind CSS 4, and DaisyUI 5.

Before writing code:
1. Read docs/labb-llms-reference.md.
2. Run uv run labb components inspect <component>.
3. Run uv run labb components ex <component>.
4. If using icons, run uv run labb icons search "<keyword>".

Task:
<specific UI task>

Rules:
- Use only valid LABB props from component inspection.
- Do not guess icon names.
- Do not invent manual SVG icons if labbicons has a matching icon.
- Keep custom CSS in static_src/input.css.
- After edits, run uv run labb scan, uv run labb build, and uv run python manage.py check.
```

## 7. Well-Structured Prompt Examples

### 7.1 Button with Icon

```text
Use docs/labb-llms-reference.md.
I need a LABB button for a Django template.
Inspect the button component and view the with-icons example first:
- uv run labb components inspect button
- uv run labb components ex button with-icons

Create a primary "View Project" button with an arrow icon at the end.
Search for a valid arrow icon with:
- uv run labb icons search "arrow"

Use only valid LABB props. Do not guess icon names.
```

Expected style of output:

```django
<c-lb.button variant="primary" icon.end="rmx.arrow-right">
    View Project
</c-lb.button>
```

### 7.2 Card Component

```text
Use docs/labb-llms-reference.md.
Inspect the LABB card component before writing code:
- uv run labb components inspect card
- uv run labb components ex card

Create a project preview card for portfolio/templates/portfolio/projects.html.
The card should include an image, title, short description, status badge, and action buttons.
Use LABB card sub-components where appropriate.
Do not invent props. Use only props from inspection.
```

### 7.3 Theme-Aware Alert

```text
Use docs/labb-llms-reference.md.
Inspect alert before writing code:
- uv run labb components inspect alert
- uv run labb components ex alert

Create a success alert that says "Message sent successfully."
It must use DaisyUI/LABB theme colors and should not include custom inline styles.
```

### 7.4 Reactive Component

```text
Use docs/labb-llms-reference.md.
I need a reactive LABB button using Alpine.
Inspect button and read the reactivity section first:
- uv run labb components inspect button
- uv run labb components ex button reactive

Create a button that starts as primary and changes to success after click.
Use the .x variant only if the inspected docs/examples support it.
Keep JavaScript minimal and use lbProps correctly.
```

### 7.5 Icon Search Prompt

```text
I need a LABB icon for a delivery route.
Do not guess the icon name.
Run:
- uv run labb icons search "route"
- uv run labb icons search "truck"

Choose the closest valid component name from the search results and use it in a LABB button or direct <c-lbi> icon.
```

### 7.6 Existing Template Refactor

```text
Refactor portfolio/templates/portfolio/contact.html to use LABB form/input/button components.
Before editing:
- Read docs/labb-llms-reference.md.
- Inspect input, textarea, button, fieldset, and label components.
- View examples for those components.

Rules:
- Preserve the current form action, method, field names, and CSRF behavior.
- Do not change backend view logic.
- Rebuild CSS and run Django checks after edits.
```

## 8. Common LABB Patterns for AI-Generated Code

### 8.1 Basic Component

```django
<c-lb.button variant="primary" size="md">
    Save
</c-lb.button>
```

### 8.2 Component with Extra Classes

```django
<c-lb.button variant="primary" class="shadow-lg shadow-primary/20">
    Discuss a Project
</c-lb.button>
```

Use `class` for Tailwind utilities that are not covered by LABB props.

### 8.3 Component with Icon

```django
<c-lb.button icon="rmx.mail" variant="primary">
    Contact
</c-lb.button>
```

### 8.4 Icon at End

```django
<c-lb.button icon.end="rmx.arrow-right" variant="primary">
    Continue
</c-lb.button>
```

### 8.5 Filled Icon

```django
<c-lb.button icon.fill="rmx.heart" variant="error">
    Like
</c-lb.button>
```

### 8.6 Direct Icon

```django
<c-lbi n="rmx.check" w="1rem" h="1rem" class="text-success" />
```

### 8.7 Card Composition

```django
<c-lb.card class="overflow-hidden">
    <c-lb.card.figure>
        <img src="{{ image_url }}" alt="{{ title }}" class="w-full object-cover">
    </c-lb.card.figure>
    <c-lb.card.body>
        <c-lb.card.title>{{ title }}</c-lb.card.title>
        <p>{{ description }}</p>
        <c-lb.card.actions justify="end">
            <c-lb.button variant="primary" size="sm">View</c-lb.button>
        </c-lb.card.actions>
    </c-lb.card.body>
</c-lb.card>
```

Always inspect `card`, `card.figure`, `card.body`, `card.title`, and `card.actions` before using new props.

### 8.8 Local Cotton Wrapper Around LABB

Use a local component when the same LABB pattern appears repeatedly.

```django
<c-vars
    title=""
    icon="rmx.check"
    variant="primary"
/>

<div class="flex items-start gap-3">
    <c-lbi n="{{ icon }}" w="1rem" h="1rem" class="text-{{ variant }}" />
    <div>
        <p class="font-semibold">{{ title }}</p>
        <div>{{ slot }}</div>
    </div>
</div>
```

Prompt AI to keep reusable wrappers small and explicit.

## 9. Best Practices for AI-Assisted LABB Development

### 9.1 Prefer Existing LABB Primitives

Ask AI to use LABB components first for:

- Buttons
- Cards
- Badges
- Alerts
- Dropdowns
- Modals
- Tabs
- Tables
- Inputs
- Toggles
- Menus
- Stats
- Timelines
- Charts

Use plain HTML only when:

- The UI is project-specific.
- LABB does not have a suitable primitive.
- The existing app already uses a custom pattern.

### 9.2 Keep Design Tokens Theme-Aware

Use DaisyUI/LABB color names:

```text
primary
secondary
accent
neutral
info
success
warning
error
base-100
base-200
base-300
base-content
```

Prefer:

```django
<c-lb.badge variant="success">Active</c-lb.badge>
```

Over:

```html
<span style="background: #22c55e">Active</span>
```

### 9.3 Keep CSS in the Right Place

Use:

```text
static_src/input.css
```

For:

- Custom themes.
- Custom components.
- Animations.
- Project-specific utility classes.

Then build:

```powershell
uv run labb build
```

Do not ask AI to place large custom CSS blocks inside Django templates unless the project specifically needs inline critical CSS.

### 9.4 Keep Props and Tailwind Classes Separate

Use component props for component behavior and DaisyUI variants:

```django
<c-lb.button variant="primary" size="sm" btnStyle="outline">
    Save
</c-lb.button>
```

Use `class` for layout and one-off styling:

```django
<c-lb.button variant="primary" class="w-full md:w-auto">
    Save
</c-lb.button>
```

### 9.5 Ask AI to Preserve Backend Contracts

For Django forms and links, prompts should say:

```text
Preserve field names, form method, action URL, CSRF token, view names, and context variables.
Only refactor the presentation layer.
```

This prevents frontend cleanup from breaking backend behavior.

## 10. Common Mistakes and How to Avoid Them

### Mistake: Guessing Parameter Names

Bad:

```django
<c-lb.button style="ghost" color="primary">
    Click
</c-lb.button>
```

Good:

```django
<c-lb.button btnStyle="ghost" variant="primary">
    Click
</c-lb.button>
```

Prevention:

```powershell
uv run labb components inspect button
```

### Mistake: Guessing Icon Names

Bad:

```django
<c-lb.button icon="rmx.rocket-2-line">
    Launch
</c-lb.button>
```

Good:

```powershell
uv run labb icons search "rocket"
```

Then use the exact returned component, for example:

```django
<c-lb.button icon="rmx.rocket-2">
    Launch
</c-lb.button>
```

### Mistake: Forgetting to Rebuild CSS

Symptom:

- Component appears unstyled.
- New classes are missing.
- Production does not show the latest UI.

Fix:

```powershell
uv run labb scan
uv run labb build
uv run python manage.py check
```

### Mistake: Forgetting Theme Dependencies

Theme switching requires:

```django
{% load lb_tags %}
{% labb_theme as labb_theme_attr %}
<html {{ labb_theme_attr|safe }}>
<c-lb.m.dependencies setThemeEndpoint="{% url 'set_theme' %}" />
{% csrf_token %}
```

And a URL:

```python
from labb.shortcuts import set_theme_view
path("set-theme/", set_theme_view, name="set_theme")
```

### Mistake: Using Reactive Props Without `.x`

If you need runtime prop changes, use a reactive variant when supported:

```django
<c-lb.button.x x-model="btn" variant="primary">
    Save
</c-lb.button.x>
```

Static components are server-rendered and do not update their props at runtime.

### Mistake: Asking AI for "Any Nice UI"

This often produces invalid props or manual HTML that ignores LABB.

Better:

```text
Use LABB components only where they fit.
For every LABB component used, first inspect it with the CLI and use exact props.
If LABB has no matching primitive, use plain Django/Tailwind markup and explain why.
```

## 11. Troubleshooting AI-Generated LABB Code

### 11.1 Component Does Not Render

Check:

```powershell
uv run python manage.py check
```

Then confirm:

- `django_cotton` is in `INSTALLED_APPS`.
- `labb` is in `INSTALLED_APPS`.
- The template file is in a Django-discovered template folder.
- The component name exists.
- You did not mistype a sub-component.

### 11.2 Icon Error

Error pattern:

```text
TypeError: cannot unpack non-iterable NoneType object
```

Likely cause:

- Invalid or guessed icon name.

Fix:

```powershell
uv run labb icons search "<keyword>"
uv run labb icons info <exact.icon-name>
```

### 11.3 Styles Missing

Run:

```powershell
uv run labb scan
uv run labb build
```

Confirm base template loads:

```django
<link rel="stylesheet" href="{% static 'css/output.css' %}">
```

### 11.4 AI Used Wrong Boolean Syntax

LABB supports implicit booleans:

```django
<c-lb.button disabled>
    Disabled
</c-lb.button>
```

Do not force strings unless the component docs/examples show that pattern:

```django
<c-lb.button disabled="true">
    Disabled
</c-lb.button>
```

### 11.5 AI Used Wrong Reactive Prop Format

Reactive prop objects use camelCase keys:

```js
{ variant: '', btnStyle: '', size: 'md' }
```

If the component uses `btnStyle`, do not use `btn_style`, `style`, or `buttonStyle`.

## 12. Prompt Patterns by Task Type

### Add a New LABB Section

```text
Read docs/labb-llms-reference.md.
I need a new section in portfolio/templates/portfolio/home.html using LABB components.
Inspect hero, card, button, badge, and stat before writing code.
Use exact LABB props only.
Keep layout classes in class attributes.
After editing, run uv run labb scan, uv run labb build, and uv run python manage.py check.
```

### Refactor Existing HTML to LABB

```text
Refactor this Django template section to LABB components where appropriate.
Before editing, inspect the matching LABB components and examples.
Do not change context variable names, URLs, forms, or view logic.
If a plain HTML element is clearer than a LABB component, keep it and explain why.
```

### Create a Reusable Cotton Component

```text
Create a local Django Cotton component using LABB primitives.
Use c-vars for defaults.
Keep the component small and reusable.
Inspect all LABB primitives before using them.
Place the file under portfolio/templates/cotton/.
Show an example usage snippet.
```

### Debug a LABB Error

```text
Use docs/labb-llms-reference.md.
Diagnose this LABB/Django Cotton error.
First check for invalid prop names, invalid icon names, missing INSTALLED_APPS, and missing CSS build.
Run the relevant labb components inspect or labb icons search command before suggesting fixes.
```

### Prepare for Deployment

```text
Before deployment, verify the LABB frontend:
1. uv run labb scan
2. uv run labb build
3. uv run python manage.py check
4. confirm static/css/output.css changed if CSS/templates changed
5. deploy with Vercel
6. verify the public /static/css/output.css URL
```

## 13. AI Review Checklist for LABB Pull Requests

Ask an AI assistant to review LABB changes with this checklist:

```text
Review this LABB/Django frontend change.
Check:
- Every LABB component name exists in docs/labb-llms-reference.md.
- Every prop name matches labb components inspect output.
- Every icon name is valid according to labb icons search/info.
- The template preserves Django context variables and URLs.
- Theme colors use DaisyUI/LABB tokens instead of hardcoded colors where practical.
- Custom CSS is in static_src/input.css.
- CSS was rebuilt to static/css/output.css.
- labb scan, labb build, and manage.py check were run.
Return findings first, with file paths and line references.
```

## 14. Suggested Project Instructions for AI Tools

Add this to a project instruction file for tools like Cursor, Cline, Windsurf, or Copilot:

```text
This Django project uses LABB, Django Cotton, Tailwind CSS 4, DaisyUI 5, and labbicons.

Before writing LABB component code:
- Read docs/labb-llms-reference.md.
- Use uv run labb components inspect <component>.
- Use uv run labb components ex <component>.
- Use uv run labb icons search "<keyword>" before choosing icons.

Rules:
- Do not guess LABB parameter names.
- Do not guess icon names.
- Do not create manual SVG icons when labbicons has an equivalent.
- Use c-lb.* components where appropriate.
- Use c-lbi.* or <c-lbi n="..."> for icons.
- Keep custom CSS in static_src/input.css.
- Rebuild with uv run labb scan and uv run labb build after frontend changes.
- Verify with uv run python manage.py check.
```

## 15. Minimal AI Context Block

When you need a short prompt prefix, use this:

```text
LABB context:
- Read docs/labb-llms-reference.md first.
- Inspect components with uv run labb components inspect <name>.
- View examples with uv run labb components ex <name>.
- Search icons with uv run labb icons search "<term>".
- Use exact prop names only.
- Rebuild CSS with uv run labb scan and uv run labb build.
- Verify Django with uv run python manage.py check.
```

## 16. Final Verification Commands

After AI-generated LABB changes:

```powershell
uv run labb scan
uv run labb build
uv run python manage.py check
git diff --check
```

For Vercel deployment:

```powershell
& 'C:\nvm4w\nodejs\npx.cmd' vercel deploy --prod --debug
& 'C:\nvm4w\nodejs\npx.cmd' vercel inspect gerlanportfolio.vercel.app --debug
& 'C:\nvm4w\nodejs\npx.cmd' vercel logs gerlanportfolio.vercel.app --no-follow --level error --since 1h --environment production --no-branch
```

For public CSS verification:

```powershell
$css='https://gerlanportfolio.vercel.app/static/css/output.css'
$r=Invoke-WebRequest -Uri $css -UseBasicParsing
$r.StatusCode
```

## 17. Summary

AI assistants work well with LABB when they are forced to use the same source-of-truth workflow a developer should use:

- Read `docs/labb-llms-reference.md`.
- Inspect components.
- Copy examples.
- Search icons.
- Avoid guessed props.
- Build and verify.

The best prompts are specific, command-driven, and explicit about what must not be guessed. Treat the LABB CLI as the authority, and treat AI as the implementation helper that applies the inspected component contract.

