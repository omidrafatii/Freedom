import requests, re, base64, os, html

CHANNEL = "AR14N24B"  # اسم کانال بدون @
SUB_FILE = "sub.txt"
MAX_LINKS = 60
PAGES = 3  # چند صفحه قدیمی‌تر هم چک بشه

LINK_RE = re.compile(r'(?:vless|vmess|trojan|ss)://[^\s"<]+')

def fetch(before=None):
    url = f"https://t.me/s/{CHANNEL}" + (f"?before={before}" if before else "")
    r = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status()
    return r.text

def get_new_links():
    links, before = [], None
    for _ in range(PAGES):
        text = html.unescape(fetch(before))
        links.extend(LINK_RE.findall(text))
        ids = re.findall(r'data-post="[^"]+/(\d+)"', text)
        if not ids:
            break
        before = min(int(i) for i in ids)
    return links

def load_old_links():
    if not os.path.exists(SUB_FILE):
        return []
    content = open(SUB_FILE).read().strip()
    if not content:
        return []
    try:
        decoded = base64.b64decode(content).decode("utf-8", "ignore")
        return [l for l in decoded.splitlines() if l.strip()]
    except Exception:
        return []

def main():
    combined = get_new_links() + load_old_links()
    seen, unique = set(), []
    for l in combined:
        if l not in seen:
            seen.add(l)
            unique.append(l)
    final = unique[:MAX_LINKS]
    encoded = base64.b64encode("\n".join(final).encode()).decode()
    open(SUB_FILE, "w").write(encoded)
    print(f"{len(final)} لینک ذخیره شد.")

if __name__ == "__main__":
    main()
