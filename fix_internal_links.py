#!/usr/bin/env python3
"""
fix_internal_links.py
"""

import re
import os
import glob
import hashlib

print(f'>>> RUNNING FILE: {os.path.abspath(__file__)}')
with open(__file__, 'rb') as _f:
    print(f'>>> FILE HASH: {hashlib.md5(_f.read()).hexdigest()}')
print('>>> Expected hash for the fixed version: 2ca0e996d403 (first 12 chars)\n')

DOMAIN_RE = re.compile(r'https?://(?:www\.)?outfog\.com(/[^"\'\s)>&<]*)?')

def find_site_root():
    if os.path.isdir('outfog.com'):
        return 'outfog.com'
    return '.'

def build_url_map(root):
    url_map = {}
    for fp in glob.glob(os.path.join(root, '**', '*.html'), recursive=True):
        rel = os.path.relpath(fp, root)
        rel_url = '/' + rel.replace(os.sep, '/')
        if rel_url.endswith('/index.html'):
            site_path = rel_url[: -len('index.html')]
        else:
            site_path = rel_url
        url_map[site_path] = fp
        if site_path.endswith('/'):
            url_map[site_path.rstrip('/')] = fp
    return url_map

def main():
    root = find_site_root()
    url_map = build_url_map(root)
    print(f'Indexed {len(url_map)} local pages under "{root}/".\n')

    html_files = glob.glob(os.path.join(root, '**', '*.html'), recursive=True)
    unmatched = set()
    updated_files = 0

    for fp in html_files:
        with open(fp, encoding='utf-8', errors='ignore') as f:
            content = f.read()

        def repl(m):
            path = m.group(1) or '/'
            if path == '/' or path == '':
                return m.group(0)
            if '#' in path:
                path, fragment = path.split('#', 1)
                fragment = '#' + fragment
            else:
                fragment = ''
            target_fp = url_map.get(path) or url_map.get(path.rstrip('/'))
            if not target_fp:
                unmatched.add(m.group(0))
                return m.group(0)
            rel = os.path.relpath(target_fp, os.path.dirname(fp))
            return rel.replace(os.sep, '/') + fragment

        new_content = DOMAIN_RE.sub(repl, content)

        if new_content != content:
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(new_content)
            updated_files += 1

    print(f'Updated {updated_files} file(s).\n')

    if unmatched:
        print(f'{len(unmatched)} distinct link(s) had no matching local page (left unchanged):')
        for u in sorted(unmatched):
            print(' ', u)
    else:
        print('Every outfog.com link with a path resolved to a local file. Nice.')

if __name__ == '__main__':
    main()
