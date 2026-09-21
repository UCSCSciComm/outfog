cat > /tmp/strip_comments.py <<'EOF'
#!/usr/bin/env python3
import re, sys, pathlib
apply = '--apply' in sys.argv
open_re = re.compile(r'<div\b[^>]*(?<![-\w])id="(?:comments|respond)"[^>]*>')
tok_re = re.compile(r'<div\b|</div>')
files = blocks = comment_items = 0
problems = []
for p in sorted(pathlib.Path('.').rglob('*.html')):
    if '.git' in p.parts:
        continue
    with open(p, encoding='utf-8', newline='') as fh:
        s = fh.read()
    orig, pos, n = s, 0, 0
    while True:
        m = open_re.search(s, pos)
        if not m:
            break
        depth, end = 1, None
        for t in tok_re.finditer(s, m.end()):
            depth += -1 if t.group().startswith('</') else 1
            if depth == 0:
                end = t.end()
                break
        if end is None:
            problems.append(str(p))
            break
        comment_items += s[m.start():end].count('id="comment-')
        s = s[:m.start()] + s[end:]
        pos = m.start()
        n += 1
    if n:
        files += 1
        blocks += n
        if apply:
            with open(p, 'w', encoding='utf-8', newline='') as fh:
                fh.write(s)
print(('APPLIED' if apply else 'PREVIEW') + f": {blocks} blocks in {files} files, {comment_items} comment items removed")
print('unbalanced (skipped):', problems if problems else 'none')
EOF
python3 /tmp/strip_comments.py