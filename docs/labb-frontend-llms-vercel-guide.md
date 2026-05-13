# LABB Frontend, LLMs, and Vercel Guide for the Django Portfolio

Project root: `C:\Users\gerla\mywork\myproject`  
Primary Django app: `portfolio`  
LABB config: `labb.yaml`  
LLM reference file: `llms`  
Production platform: Vercel  
Production project: `gerlan.portfolio`

## 1. What LABB Is in This Project

LABB is the frontend component layer used with this Django portfolio project. It combines:

- Django server-rendered templates.
- Django Cotton component syntax, such as `<c-lb.button>` and local `<c-component-name>` components.
- Tailwind CSS 4.
- DaisyUI 5 themes.
- LABB component helpers and theme utilities.
- Optional `labbicons` icon components.
- Optional Alpine.js-powered reactivity for `.x` component variants.

In this portfolio, LABB is used in two ways:

- The base integration is active in `portfolio/templates/portfolio/base.html` through `{% load lb_tags %}`, `{% labb_theme %}`, and `<c-lb.m.dependencies ... />`.
- Several reusable Cotton components exist under `portfolio/templates/cotton/`, including component examples for navbar, footer, project cards, service cards, skill badges, and timeline items.

The project also uses hand-authored Tailwind/DaisyUI markup in `portfolio/templates/portfolio/*.html`. This is valid. LABB does not require every piece of UI to be a component. A practical project can mix LABB components, local Cotton components, and normal Django templates.

## 2. Required Python Dependencies

This project declares LABB-related Python dependencies in `pyproject.toml`:

```toml
[project]
requires-python = ">=3.10,<4"
dependencies = [
    "django~=5.1",
    "labbicons>=0.4.0",
    "labbui>=0.4.0",
    "pillow>=12.2.0",
]
```

For a new or existing Django project using `uv`, install the same family of dependencies with:

```powershell
uv add labbui labbicons django
```

If you are using pip:

```powershell
pip install labbui labbicons django
```

If you are using Poetry:

```powershell
poetry add labbui labbicons django
```

`labbui` provides the `labb` CLI and component library. `labbicons` provides icon packs and `<c-lbi...>` icon components.

## 3. Required Node Dependencies

This project uses Tailwind CSS 4 and DaisyUI 5 through `package.json`:

```json
{
  "devDependencies": {
    "@tailwindcss/cli": "4.2",
    "daisyui": "5.5",
    "tailwindcss": "4.2"
  }
}
```

Install the locked Node dependencies:

```powershell
npm ci
```

For a new project, you can let LABB install the expected dependencies:

```powershell
uv run labb setup --install-deps
```

Or install manually:

```powershell
npm install -D tailwindcss@4 @tailwindcss/cli@4 daisyui@5
```

## 4. Django Settings Integration

### 4.1 Installed Apps

The current project has these LABB-related apps in `myproject/settings.py`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "labb",
    "labbicons",
    "django_cotton",
    "portfolio",
]
```

For another Django project, include at least:

```python
INSTALLED_APPS = [
    # Django contrib apps...
    "django.contrib.staticfiles",
    "django_cotton",
    "labb",
    "labbicons",  # optional, but recommended if you use icons
    "your_app",
]
```

If you see template component errors, confirm that `django_cotton`, `labb`, and the app containing your templates are all installed.

### 4.2 Template Settings

The project uses app template discovery:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

`APP_DIRS = True` is important because LABB, Django Cotton, and your Django apps expose templates from app-level template folders.

### 4.3 LABB Settings

This project sets the default theme:

```python
LABB_SETTINGS = {
    "DEFAULT_THEME": "cyber-signal",
}
```

`cyber-signal` is a custom DaisyUI theme defined in `static_src/input.css`.

Reusable pattern:

```python
LABB_SETTINGS = {
    "DEFAULT_THEME": "labb-light",
    "ALPINE_JS_PATH": "labb/js/alpine/alpine.min.js",
    "STACK_HELPERS": {
        "components": ["labb/js/alpine/labb-component.js", "alpine"],
    },
}
```

Use:

- `DEFAULT_THEME`: a DaisyUI theme name defined in your CSS.
- `"__system__"`: defers to OS preference.
- `ALPINE_JS_PATH`: bundled Alpine path or a CDN URL.
- `STACK_HELPERS`: helper script stacks for reactive components.

### 4.4 Static Files

The current project uses:

```python
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "static",
    ("media", BASE_DIR / "media"),
]

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"
```

For LABB and Tailwind/DaisyUI:

- `static_src/input.css` is the source CSS.
- `static/css/output.css` is the compiled CSS served by Django.
- `STATICFILES_DIRS` must include `BASE_DIR / "static"` so Django can collect and serve `static/css/output.css`.
- Vercel runs `collectstatic`, placing assets under `STATIC_ROOT`.

## 5. Base Template Integration

The current base template `portfolio/templates/portfolio/base.html` includes the required LABB theme setup:

```django
{% load static lb_tags %}
{% labb_theme as labb_theme_attr %}
<!DOCTYPE html>
<html lang="en" {{ labb_theme_attr|safe }}>
```

It loads the compiled CSS:

```django
<link rel="stylesheet" href="{% static 'css/output.css' %}">
```

It loads LABB dependencies:

```django
<c-lb.m.dependencies noGlobalCSS setThemeEndpoint="{% url 'portfolio:set_theme' %}" alpine />
```

Important details:

- `noGlobalCSS` is used because this project loads its own compiled CSS file with `<link rel="stylesheet" href="{% static 'css/output.css' %}">`.
- `setThemeEndpoint` points to the theme endpoint in `portfolio/urls.py`.
- `alpine` force-loads Alpine.js, useful because the navbar and theme UI use Alpine-style behavior.
- `{% csrf_token %}` is included in the body, which LABB needs for POST-based theme switching.

The body contains:

```django
<body class="page-shell min-h-screen bg-base-100 antialiased">
    {% csrf_token %}
```

Do not remove the CSRF token if you keep LABB theme controllers.

## 6. Theme Switching URL

The portfolio app exposes LABB's theme switching view in `portfolio/urls.py`:

```python
from django.urls import path
from labb.shortcuts import set_theme_view

urlpatterns = [
    path("set-theme/", set_theme_view, name="set_theme"),
]
```

Because the app uses `app_name = "portfolio"`, the template references it as:

```django
{% url 'portfolio:set_theme' %}
```

For another project, add the same view in your app-level or root URL config:

```python
from labb.shortcuts import set_theme_view

path("set-theme/", set_theme_view, name="set_theme")
```

Then in your base template:

```django
<c-lb.m.dependencies setThemeEndpoint="{% url 'set_theme' %}" />
```

Use the namespaced form if your URL is inside an app namespace.

## 7. `labb.yaml` Configuration

The current `labb.yaml` is:

```yaml
css:
  build:
    input: static_src/input.css
    minify: true
    output: static/css/output.css
  scan:
    apps: {}
    output: static_src/labb-classes.txt
    templates:
    - templates/**/*.html
    - '*/templates/**/*.html'
    - '**/templates/**/*.html'
```

### 7.1 Build Section

The build section tells LABB where to read and write CSS:

- `input`: Tailwind/DaisyUI source CSS.
- `output`: compiled CSS served by Django.
- `minify`: production-friendly CSS output.

Equivalent CLI build:

```powershell
uv run labb build
```

Or the Tailwind CLI command used in this project:

```powershell
& 'C:\nvm4w\nodejs\npx.cmd' @tailwindcss/cli -i static_src\input.css -o static\css\output.css --minify
```

### 7.2 Scan Section

The scan section tells LABB which templates to inspect:

- `templates/**/*.html`
- `*/templates/**/*.html`
- `**/templates/**/*.html`

This broad pattern works well for Django projects with app-level templates, nested Cotton components, and shared template folders.

Run:

```powershell
uv run labb scan
```

Verified output in this project:

```text
Found 19 files
Components: 8
Classes: 11
Output: static_src/labb-classes.txt
```

The generated `static_src/labb-classes.txt` helps Tailwind preserve classes that appear through LABB/Cotton components and template scanning.

## 8. CSS Source Setup

The current `static_src/input.css` starts with:

```css
/* labb CSS Setup for Tailwind CSS 4 + DaisyUI 5 */

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@100..900&family=JetBrains+Mono:ital,wght@0,100..800;1,100..800&display=swap');

@property --tw-shadow-color {
  syntax: "*";
  inherits: true;
}

@import "tailwindcss";
@plugin "daisyui" {
  themes: cyber-signal --default, labb-light, labb-dark, light, dark;
}
```

Key points:

- Tailwind CSS 4 uses `@import "tailwindcss";`.
- DaisyUI 5 is loaded with `@plugin "daisyui"`.
- The app defines a custom default theme named `cyber-signal`.
- The built-in `labb-light`, `labb-dark`, `light`, and `dark` themes are also available.
- Custom project styles live below the LABB/Tailwind/DaisyUI setup.

After editing `static_src/input.css`, rebuild:

```powershell
uv run labb build
```

Or:

```powershell
& 'C:\nvm4w\nodejs\npx.cmd' @tailwindcss/cli -i static_src\input.css -o static\css\output.css --minify
```

Then verify:

```powershell
uv run python manage.py check
```

## 9. Django Cotton Component Patterns

### 9.1 LABB Components

LABB components use the `c-lb` namespace:

```django
<c-lb.button variant="primary" size="sm">
    Save
</c-lb.button>
```

Sub-components use dot notation:

```django
<c-lb.card>
    <c-lb.card.body>
        <c-lb.card.title>Project</c-lb.card.title>
        <p>Project content.</p>
    </c-lb.card.body>
</c-lb.card>
```

### 9.2 Local Cotton Components

Local components live in app template folders such as:

```text
portfolio/templates/cotton/info_item.html
portfolio/templates/cotton/logo.html
portfolio/templates/cotton/component/project_card.html
```

Example local component definition from `portfolio/templates/cotton/info_item.html`:

```django
<c-vars
    icon="rmx.check"
    iconSize="1.25rem"
/>

<div class="flex items-start gap-3">
    <c-lbi n="{{ icon }}" w="{{ iconSize }}" h="{{ iconSize }}" class="text-primary/70" />
    <div>{{ slot }}</div>
</div>
```

Usage pattern:

```django
<c-info_item icon="rmx.code">
    Build reliable Django interfaces.
</c-info_item>
```

For nested folders, component names generally mirror the folder structure. For example, a component under `templates/cotton/component/project_card.html` is used as:

```django
<c-component.project_card project="{{ project }}" />
```

If uncertain, inspect the rendered template behavior and use Django Cotton's naming conventions consistently.

### 9.3 Parameter Defaults with `c-vars`

Use `<c-vars>` at the top of custom Cotton components to define defaults:

```django
<c-vars
    title=""
    icon="rmx.check"
    variant="primary"
/>
```

Then consume those variables in the template:

```django
<c-lb.badge variant="{{ variant }}" icon="{{ icon }}">
    {{ title }}
</c-lb.badge>
```

This makes components safer for AI-assisted editing because defaults are visible and predictable.

## 10. LLM-Specific Configuration and Usage

This project includes a file named `llms`, generated from LABB's LLM guidance. It is meant to be read by AI/LLM tools before they modify LABB components.

Refresh or display LABB's LLM reference with:

```powershell
uv run labb llms
```

If you want to regenerate the local file:

```powershell
uv run labb llms > llms
```

### 10.1 CLI-First Rule for AI Work

Before adding or modifying LABB components, use the CLI:

```powershell
uv run labb components inspect button
```

Verified output for `button` in this project showed:

- `variant`: `neutral`, `primary`, `secondary`, `accent`, `info`, `success`, `warning`, `error`
- `btnStyle`: `outline`, `dash`, `soft`, `ghost`, `link`, `bare`
- `behavior`: `active`, `disabled`
- `size`: `xs`, `sm`, `md`, `lg`, `xl`
- `modifier`: `wide`, `block`, `square`, `circle`
- `icon`, `icon.fill`, `icon.end`, `icon.class`

This matters because parameter names must be exact. For example, LABB uses `btnStyle`, not a guessed `style` prop for buttons.

### 10.2 View Examples Before Writing Components

List examples:

```powershell
uv run labb components ex button
```

View a specific example:

```powershell
uv run labb components ex button with-icons
```

Browse all examples:

```powershell
uv run labb components ex --tree
```

Use examples as the source of truth when an LLM needs to produce syntax.

### 10.3 Parameter Naming Rules

Use the exact variable names from `labb components inspect`.

Patterns:

- Use camelCase where LABB defines camelCase: `btnStyle`, `pinRows`, `bgVariant`.
- Use boolean attributes directly where appropriate: `<c-lb.button disabled>`.
- For dynamic boolean values in Django templates, use Django/Cotton-compatible binding syntax only when confirmed by examples.
- For reactive props, use camelCase keys in JavaScript objects.

Examples:

```django
<c-lb.button variant="primary" btnStyle="outline" size="sm">
    Contact
</c-lb.button>
```

```django
<c-lb.table zebra pinRows size="sm">
    ...
</c-lb.table>
```

Avoid:

```django
<c-lb.button style="outline">
    Wrong
</c-lb.button>
```

Use:

```django
<c-lb.button btnStyle="outline">
    Correct
</c-lb.button>
```

### 10.4 Icon Usage with `labbicons`

Search before using an icon:

```powershell
uv run labb icons search "rocket"
```

Verified output:

```text
rmx.rocket
rmx.rocket-2
```

Get icon details:

```powershell
uv run labb icons info rmx.rocket
```

Use icons inside LABB components:

```django
<c-lb.button icon="rmx.home">
    Home
</c-lb.button>
```

Use modifiers:

```django
<c-lb.button icon.fill="rmx.heart" variant="error">
    Like
</c-lb.button>

<c-lb.button icon.end="rmx.arrow-right" variant="primary">
    Continue
</c-lb.button>

<c-lb.button icon.fill.end="rmx.check" variant="success">
    Done
</c-lb.button>

<c-lb.button icon.fill="rmx.star" icon.class="text-warning">
    Favorite
</c-lb.button>
```

Direct icon usage:

```django
<c-lbi n="rmx.check" w="1em" h="1em" />
```

Or:

```django
<c-lbi.rmx.check w="1rem" h="1rem" class="text-primary" />
```

Avoid guessing icon names. A common failure is:

```text
TypeError: cannot unpack non-iterable NoneType object
```

This is often caused by an invalid icon name, such as guessing `rmx.rocket-2-line` when the actual component name is `rmx.rocket-2`.

### 10.5 AI-Assisted Development Checklist

When using an LLM with LABB:

1. Give the LLM the local `llms` file.
2. Ask it to run or reference `labb components inspect <component>`.
3. Ask it to run or reference `labb components ex <component>`.
4. Require exact prop names from the CLI.
5. Require exact icon names from `labb icons search`.
6. Keep custom CSS in `static_src/input.css`.
7. Rebuild `static/css/output.css` after CSS or class changes.
8. Run `uv run python manage.py check`.
9. If deploying, verify the public CSS URL after deployment.

## 11. Reactive LABB Components

LABB components are zero-JS by default. Reactivity is opt-in with `.x` variants:

```django
<c-lb.button.x variant="primary" size="lg">
    Save
</c-lb.button.x>
```

Example with Alpine state:

```django
<div x-data="{ btn: { variant: 'primary', size: 'md' } }">
    <c-lb.button.x x-model="btn" variant="primary" size="md">
        Click me
    </c-lb.button.x>

    <select x-model="btn.variant">
        <option value="primary">Primary</option>
        <option value="error">Error</option>
    </select>
</div>
```

Rules:

- Props marked with `*` in `llms` are reactive.
- JavaScript reactive prop names use camelCase.
- Empty string means no value.
- Sub-components use dot notation, for example `<c-lb.stat.group.x>`.

Force Alpine to load:

```django
<c-lb.m.dependencies alpine />
```

This project already uses:

```django
<c-lb.m.dependencies noGlobalCSS setThemeEndpoint="{% url 'portfolio:set_theme' %}" alpine />
```

## 12. Charts

LABB includes Chart.js-based components:

```django
<c-lb.chart.bar data='{
    "labels": ["Jan", "Feb", "Mar"],
    "datasets": [{ "label": "Revenue", "data": [10, 20, 30] }]
}' />
```

Use DaisyUI color names in chart data:

```json
{
  "backgroundColor": ["primary", "secondary", "accent"],
  "borderColor": "primary"
}
```

Add a page-level chart provider if you need global chart defaults:

```django
<c-lb.chart color="base-content" :grid="False" animation updateAnimation
            fontSize="12" tooltips legend lightAlpha="0.4" />
```

For large dashboards or PDFs, disable animation:

```django
<c-lb.chart :animation="False" />
```

## 13. Using LABB in Other Django Projects

### 13.1 Fast Scaffolding with `labbstart`

For a new project, use `labbstart`:

```powershell
uv add labbstart
uv run labbstart new
```

Non-interactive example:

```powershell
uv run labbstart new myproject --django-version 5 --package-manager uv --kit welcome --app-name starter
```

`labbstart` creates:

- Django project structure.
- LABB dependencies.
- LABB icons.
- Starter app.
- `labb.yaml`.
- CSS source/output setup.
- `.gitignore`.
- README guidance.

After scaffolding:

```powershell
uv run labb dev
uv run python manage.py runserver
```

Use two terminals: one for LABB CSS watching, one for Django.

### 13.2 Adding LABB to an Existing Project

Recommended migration sequence:

1. Install dependencies:

```powershell
uv add labbui labbicons
npm install -D tailwindcss@4 @tailwindcss/cli@4 daisyui@5
```

2. Add apps:

```python
"django_cotton",
"labb",
"labbicons",
```

3. Initialize LABB:

```powershell
uv run labb init --defaults
```

4. Confirm `labb.yaml`.
5. Add `static_src/input.css`.
6. Add `static/css/output.css` to your base template.
7. Add `{% load lb_tags %}` and `{% labb_theme %}` to the root HTML template.
8. Add `<c-lb.m.dependencies ... />`.
9. Add a theme endpoint if using theme switching.
10. Run:

```powershell
uv run labb scan
uv run labb build
uv run python manage.py check
```

### 13.3 Migration Strategy from Existing Frontends

Use incremental migration. Do not rewrite everything at once.

Good order:

1. Base template and theme setup.
2. Buttons, badges, alerts, and cards.
3. Navbar/footer.
4. Forms and inputs.
5. Tables, stats, timelines, tabs, modals.
6. Reactive components only where needed.
7. Charts last, because they require careful JSON data and optional Alpine state.

For each converted component:

```powershell
uv run labb components inspect <component>
uv run labb components ex <component>
```

Then implement, scan, build, and verify.

### 13.4 Custom Component Extension

Use local Cotton components for project-specific patterns:

```text
your_app/templates/cotton/project_card.html
your_app/templates/cotton/dashboard/stat_card.html
your_app/templates/cotton/forms/contact_field.html
```

Good custom component rules:

- Use `c-vars` for defaults.
- Keep components small and composable.
- Use LABB primitives inside local components.
- Use Tailwind/DaisyUI classes for layout and custom visual treatment.
- Avoid hiding too much logic in templates; keep data shaping in views/models.

## 14. Development Workflow for This Portfolio

Use this flow when editing the frontend:

```powershell
cd C:\Users\gerla\mywork\myproject
npm ci
uv run labb scan
uv run labb build
uv run python manage.py check
uv run python manage.py runserver 127.0.0.1:8000 --noreload
```

Alternative build command already used successfully:

```powershell
& 'C:\nvm4w\nodejs\npx.cmd' @tailwindcss/cli -i static_src\input.css -o static\css\output.css --minify
```

When adding LABB components, inspect first:

```powershell
uv run labb components inspect card
uv run labb components ex card
```

When adding icons, search first:

```powershell
uv run labb icons search "mail"
```

## 15. Vercel Deployment for LABB + Django

This project deploys successfully to Vercel using Vercel's Django framework detection. No custom `vercel.json` is required for the current setup.

### 15.1 Vercel-Important Django Settings

The project uses:

```python
default_debug = "False" if os.getenv("VERCEL") else "True"
DEBUG = os.getenv("DJANGO_DEBUG", default_debug).lower() == "true"

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    ".vercel.app",
]

extra_allowed_hosts = os.getenv("DJANGO_ALLOWED_HOSTS")
if extra_allowed_hosts:
    ALLOWED_HOSTS.extend(host.strip() for host in extra_allowed_hosts.split(",") if host.strip())

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
```

These settings:

- Disable debug by default on Vercel.
- Allow `.vercel.app` deployment URLs.
- Support custom hosts through `DJANGO_ALLOWED_HOSTS`.
- Respect Vercel's HTTPS proxy.
- Enable secure cookies in production.

### 15.2 Environment Variables

Recommended production variables:

```text
DJANGO_SECRET_KEY=<strong secret key>
DJANGO_DEBUG=false
DJANGO_ALLOWED_HOSTS=gerlanportfolio.vercel.app
```

Set them:

```powershell
& 'C:\nvm4w\nodejs\npx.cmd' vercel env add DJANGO_SECRET_KEY production
& 'C:\nvm4w\nodejs\npx.cmd' vercel env add DJANGO_DEBUG production
& 'C:\nvm4w\nodejs\npx.cmd' vercel env add DJANGO_ALLOWED_HOSTS production
```

For other LABB projects, no special LABB-only env vars are usually required. LABB theme behavior is mostly Django session/template based. Use env vars only for Django security, hosts, database, and external services.

### 15.3 Static Files on Vercel

Vercel detected Django and ran:

```text
Running collectstatic...
```

Before deploy, ensure:

- `static/css/output.css` exists.
- It includes the latest Tailwind/DaisyUI/LABB classes.
- `STATICFILES_DIRS` includes `BASE_DIR / "static"`.
- `STATIC_ROOT` is set.

Build locally before deploy:

```powershell
uv run labb scan
uv run labb build
uv run python manage.py check
```

Or use the direct Tailwind command:

```powershell
& 'C:\nvm4w\nodejs\npx.cmd' @tailwindcss/cli -i static_src\input.css -o static\css\output.css --minify
```

### 15.4 Vercel Deployment Workflow

From project root:

```powershell
cd C:\Users\gerla\mywork\myproject
npm ci
uv run labb scan
uv run labb build
uv run python manage.py check
& 'C:\nvm4w\nodejs\npx.cmd' vercel deploy --prod --debug
```

Inspect:

```powershell
& 'C:\nvm4w\nodejs\npx.cmd' vercel inspect gerlanportfolio.vercel.app --debug
```

Check production errors:

```powershell
& 'C:\nvm4w\nodejs\npx.cmd' vercel logs gerlanportfolio.vercel.app --no-follow --level error --since 1h --environment production --no-branch
```

Verify CSS:

```powershell
$css='https://gerlanportfolio.vercel.app/static/css/output.css'
$r=Invoke-WebRequest -Uri $css -UseBasicParsing
[pscustomobject]@{
  Status=$r.StatusCode
  Length=$r.Content.Length
} | Format-List
```

### 15.5 Vercel Framework Detection

This project deployed through Vercel's Django framework detection. The deployment logs showed:

```text
Using Python 3.13 from .python-version
Using uv 0.10.11
Installing required dependencies from uv.lock...
Django 5.2.14 detected
Running collectstatic...
Build Completed in /vercel/output
Deployment state changed to READY
Aliased: https://gerlanportfolio.vercel.app
```

For other projects:

- Include `.python-version`.
- Include `pyproject.toml` and lock file.
- Keep `manage.py` at the project root.
- Keep Django settings importable.
- Confirm `STATIC_ROOT` is configured.
- Let Vercel detect Django unless you have a nonstandard structure.

## 16. Vercel Troubleshooting Patterns

### 16.1 CSS Looks Old or Missing

Cause:

- `static_src/input.css` changed but `static/css/output.css` was not rebuilt.
- LABB scan was not run after adding new components/classes.

Fix:

```powershell
uv run labb scan
uv run labb build
uv run python manage.py check
& 'C:\nvm4w\nodejs\npx.cmd' vercel deploy --prod --debug
```

### 16.2 LABB Component Renders Without Styling

Checklist:

- Is `static/css/output.css` linked in the base template?
- Does `STATICFILES_DIRS` include `BASE_DIR / "static"`?
- Did you run `uv run labb scan`?
- Did you run `uv run labb build`?
- Did Vercel run `collectstatic`?

### 16.3 Cotton Component Not Found

Checklist:

- Is `django_cotton` in `INSTALLED_APPS`?
- Is the component under a valid `templates/cotton/` folder?
- Is the app containing that folder in `INSTALLED_APPS`?
- Are you using the correct Cotton component name?

### 16.4 Invalid Icon Name

Symptom:

```text
TypeError: cannot unpack non-iterable NoneType object
```

Fix:

```powershell
uv run labb icons search "keyword"
uv run labb icons info rmx.icon-name
```

Use the exact component name returned by the CLI.

### 16.5 `Invalid HTTP_HOST header`

Cause:

Host is missing from `ALLOWED_HOSTS`.

Fix:

```powershell
& 'C:\nvm4w\nodejs\npx.cmd' vercel env add DJANGO_ALLOWED_HOSTS production
```

Example:

```text
gerlanportfolio.vercel.app,mycustomdomain.com,www.mycustomdomain.com
```

### 16.6 Theme Switching Does Not Work

Checklist:

- Base template has `{% load lb_tags %}`.
- `<html>` has `{% labb_theme %}` output.
- `<c-lb.m.dependencies setThemeEndpoint="...">` is present.
- `{% csrf_token %}` exists in the body.
- URL route uses `set_theme_view`.
- Browser console has no JavaScript errors.

### 16.7 Vercel Build Fails

Run locally first:

```powershell
uv run python manage.py check
uv run labb scan
uv run labb build
```

Then redeploy:

```powershell
& 'C:\nvm4w\nodejs\npx.cmd' vercel deploy --prod --debug
```

Inspect logs:

```powershell
& 'C:\nvm4w\nodejs\npx.cmd' vercel logs gerlanportfolio.vercel.app --no-follow --level error --since 1h --environment production --no-branch
```

## 17. Recommended Reusable Template for Future Projects

### `settings.py`

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_cotton",
    "labb",
    "labbicons",
    "your_app",
]

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

LABB_SETTINGS = {
    "DEFAULT_THEME": "labb-light",
}
```

### `base.html`

```django
{% load static lb_tags %}
{% labb_theme as labb_theme_attr %}
<!DOCTYPE html>
<html lang="en" {{ labb_theme_attr|safe }}>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="{% static 'css/output.css' %}">
    <c-lb.m.dependencies noGlobalCSS setThemeEndpoint="{% url 'set_theme' %}" alpine />
</head>
<body>
    {% csrf_token %}
    {% block content %}{% endblock %}
</body>
</html>
```

### `urls.py`

```python
from django.urls import path
from labb.shortcuts import set_theme_view

urlpatterns = [
    path("set-theme/", set_theme_view, name="set_theme"),
]
```

### `labb.yaml`

```yaml
css:
  build:
    input: static_src/input.css
    output: static/css/output.css
    minify: true
  scan:
    output: static_src/labb-classes.txt
    templates:
      - templates/**/*.html
      - '*/templates/**/*.html'
      - '**/templates/**/*.html'
```

### `static_src/input.css`

```css
@import "tailwindcss";
@plugin "daisyui" {
  themes: labb-light --default, labb-dark, light, dark;
}
```

Then:

```powershell
uv run labb scan
uv run labb build
uv run python manage.py check
```

## 18. Practical Maintenance Rules

- Keep the `llms` file available for AI tools.
- Use `uv run labb components inspect` before using unfamiliar props.
- Use `uv run labb components ex` before writing unfamiliar component markup.
- Use `uv run labb icons search` before adding icons.
- Rebuild CSS after changing `static_src/input.css`, template classes, or LABB component usage.
- Keep LABB/DaisyUI theme names synchronized between `LABB_SETTINGS`, `<html data-theme>`, and `static_src/input.css`.
- Keep `static/css/output.css` deployed or configure Vercel to build it automatically before `collectstatic`.
- For Vercel, confirm production with `vercel inspect`, public page checks, public CSS checks, and `vercel logs`.

