# URL Shortener CLI

A simple persistent command-line URL shortener written in Python using **only the Python standard library**.

## Features

- Shorten a long HTTP/HTTPS URL into a short code such as `aB3xY7`
- Resolve a short code back to its original URL
- List all shortened URLs
- Persistent storage across program runs
- Detects duplicate URLs and returns the existing short code
- Graceful handling of invalid URLs and missing short codes
- Optional custom aliases
- Tracks how many times each short code has been resolved

## Requirements

- Python 3.8 or newer
- No third-party packages are required
- No external URL-shortening API is used

## Project structure

```text
url-shortener/
├── main.py
├── README.md
└── urls.json
```

`urls.json` is created automatically the first time a URL is shortened. It stores the mappings so that they remain available after the program exits.

## How to run

Open a terminal in the project directory and run:

```bash
python main.py <command>
```

On some systems you may need:

```bash
python3 main.py <command>
```

No installation command is necessary because the program uses only Python's standard library.

---

## Commands

### 1. Shorten a URL

Syntax:

```bash
python main.py shorten "<url>"
```

Example:

```bash
python main.py shorten "https://www.example.com/a/very/long/path"
```

Example output:

```text
Short code: k7F2aQ
```

The mapping is saved to `urls.json`.

### 2. Resolve a short code

Syntax:

```bash
python main.py resolve <code>
```

Example:

```bash
python main.py resolve k7F2aQ
```

Output:

```text
https://www.example.com/a/very/long/path
```

Every successful `resolve` increments that code's click count.

### 3. List all shortened URLs

Syntax:

```bash
python main.py list
```

Example output:

```text
Shortened URLs:
aB91xZ -> https://www.google.com (clicks: 2)
k7F2aQ -> https://www.example.com/a/very/long/path (clicks: 1)
```

---

## Bonus: Custom aliases

You can choose your own short code using `--alias`.

Syntax:

```bash
python main.py shorten "<url>" --alias <alias>
```

Example:

```bash
python main.py shorten "https://www.example.com" --alias mycode
```

Output:

```text
Short code: mycode
```

The alias must:

- contain only letters and numbers
- be between 1 and 32 characters
- not already be in use

If an alias is already taken, the program prints an error instead of overwriting the existing mapping.

---

## Duplicate URLs

If you shorten exactly the same URL again, the program does not create another mapping.

Example:

```bash
python main.py shorten "https://www.google.com"
```

Output:

```text
Short code: aB91xZ
```

Running the same command again might produce:

```text
Short code: aB91xZ
This URL is already shortened.
```

This prevents unnecessary duplicate entries.

---

## Error handling

### Invalid URL

The program accepts HTTP and HTTPS URLs with a hostname.

For example:

```bash
python main.py shorten "not-a-url"
```

Output:

```text
Error: invalid URL. Use a full HTTP/HTTPS URL.
```

### Missing short code

```bash
python main.py resolve doesnotexist
```

Output:

```text
Error: short code 'doesnotexist' was not found.
```

### Alias already exists

```bash
python main.py shorten "https://example.org" --alias mycode
```

If `mycode` is already being used:

```text
Error: short code 'mycode' is already in use.
```

---

## Persistent storage

The program stores its data in:

```text
urls.json
```

An example file looks like:

```json
{
  "k7F2aQ": {
    "url": "https://www.example.com/a/very/long/path",
    "clicks": 1
  },
  "mycode": {
    "url": "https://www.google.com",
    "clicks": 2
  }
}
```

Because this file is saved on disk, the mappings are available when the program is started again.

The program also writes updates using a temporary file followed by replacement, which helps avoid leaving a partially written JSON file if a write is interrupted.

---

## Complete example

### Shorten two URLs

```bash
python main.py shorten "https://www.google.com"
```

```text
Short code: aB91xZ
```

```bash
python main.py shorten "https://www.example.com/some/long/page"
```

```text
Short code: k7F2aQ
```

### Resolve a URL

```bash
python main.py resolve aB91xZ
```

```text
https://www.google.com
```

### Resolve it again

```bash
python main.py resolve aB91xZ
```

```text
https://www.google.com
```

The click count for `aB91xZ` is now `2`.

### List everything

```bash
python main.py list
```

```text
Shortened URLs:
aB91xZ -> https://www.google.com (clicks: 2)
k7F2aQ -> https://www.example.com/some/long/page (clicks: 0)
```

---

## Implementation details

The project uses these standard-library modules:

- `argparse` — command-line argument parsing
- `json` — persistent data storage
- `pathlib` — file and path handling
- `secrets` — secure random short-code generation
- `string` — letters and digits used in generated codes
- `tempfile` — safe temporary-file creation
- `urllib.parse` — basic URL validation

No external libraries or URL-shortening services are used.

## Requirements checklist

| Requirement | Implemented |
|---|---|
| Accept long URL and generate short code | Yes |
| Store long URL ↔ short code persistently | Yes |
| Resolve short code to original URL | Yes |
| List all shortened URLs | Yes |
| No external shortening API | Yes |
| Python standard library only | Yes |
| Invalid URL handling | Yes |
| Duplicate URL handling | Yes |
| Missing code handling | Yes |
| Custom aliases | Bonus |
| Click-count tracking | Bonus |
