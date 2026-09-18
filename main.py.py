import argparse
import json
import secrets
import string
import tempfile
from pathlib import Path
from urllib.parse import urlparse


DATA_FILE = Path(__file__).with_name("urls.json")
CODE_LENGTH = 6
ALPHABET = string.ascii_letters + string.digits


def load_data():
    if not DATA_FILE.exists():
        return {}

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError) as exc:
        print(f"Error: could not read {DATA_FILE.name}: {exc}")
        raise SystemExit(1)

    if not isinstance(data, dict):
        print(f"Error: {DATA_FILE.name} contains invalid data.")
        raise SystemExit(1)

    return data


def save_data(data):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    try:
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            dir=DATA_FILE.parent,
            delete=False,
        ) as temp_file:
            json.dump(data, temp_file, indent=2)
            temp_file.write("\n")
            temp_name = temp_file.name

        Path(temp_name).replace(DATA_FILE)
    except OSError as exc:
        print(f"Error: could not save data: {exc}")
        raise SystemExit(1)


def is_valid_url(url):
    try:
        parsed = urlparse(url)
    except ValueError:
        return False

    return (
        parsed.scheme.lower() in {"http", "https"}
        and bool(parsed.netloc)
        and bool(parsed.hostname)
    )


def generate_code(data):
    while True:
        code = "".join(secrets.choice(ALPHABET) for _ in range(CODE_LENGTH))
        if code not in data:
            return code


def find_code_for_url(data, url):
    for code, entry in data.items():
        if isinstance(entry, dict) and entry.get("url") == url:
            return code
    return None


def shorten_url(url, alias=None):
    if not is_valid_url(url):
        print("Error: invalid URL. Use a full HTTP/HTTPS URL.")
        return 1

    data = load_data()

    existing_code = find_code_for_url(data, url)
    if existing_code is not None:
        print(f"Short code: {existing_code}")
        print("This URL is already shortened.")
        return 0

    if alias:
        if not alias.isalnum():
            print("Error: alias must contain only letters and numbers.")
            return 1

        if len(alias) < 1 or len(alias) > 32:
            print("Error: alias must be between 1 and 32 characters.")
            return 1

        if alias in data:
            print(f"Error: short code '{alias}' is already in use.")
            return 1

        code = alias
    else:
        code = generate_code(data)

    data[code] = {
        "url": url,
        "clicks": 0,
    }

    save_data(data)
    print(f"Short code: {code}")
    return 0


def resolve_code(code):
    data = load_data()

    entry = data.get(code)
    if entry is None:
        print(f"Error: short code '{code}' was not found.")
        return 1

    if not isinstance(entry, dict) or "url" not in entry:
        print(f"Error: short code '{code}' contains invalid data.")
        return 1

    entry["clicks"] = int(entry.get("clicks", 0)) + 1
    save_data(data)

    print(entry["url"])
    return 0


def list_urls():
    data = load_data()

    if not data:
        print("No shortened URLs found.")
        return 0

    print("Shortened URLs:")
    for code in sorted(data):
        entry = data[code]
        url = entry.get("url", "<invalid>")
        clicks = entry.get("clicks", 0)
        print(f"{code} -> {url} (clicks: {clicks})")

    return 0


def build_parser():
    parser = argparse.ArgumentParser(
        description="A simple persistent command-line URL shortener."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    shorten_parser = subparsers.add_parser(
        "shorten",
        help="Create a short code for a URL.",
    )
    shorten_parser.add_argument(
        "url",
        help="Full HTTP/HTTPS URL to shorten.",
    )
    shorten_parser.add_argument(
        "--alias",
        help="Optional custom short code.",
    )

    resolve_parser = subparsers.add_parser(
        "resolve",
        help="Resolve a short code to its original URL.",
    )
    resolve_parser.add_argument(
        "code",
        help="Short code to resolve.",
    )

    subparsers.add_parser(
        "list",
        help="List all stored shortened URLs.",
    )

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "shorten":
        return shorten_url(args.url, args.alias)

    if args.command == "resolve":
        return resolve_code(args.code)

    if args.command == "list":
        return list_urls()

    parser.error("Unknown command.")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
