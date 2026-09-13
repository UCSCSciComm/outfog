#!/usr/bin/env python3
"""
fix_internal_links.py

Fixes absolute https://outfog.com/... links (WITH a path) that wget's
--convert-links failed to rewrite to relative local paths.

Run this from the directory ABOVE your export (the one that contains the
"outfog.com" folder, assuming you did NOT use --no-host-directories with
wget). If your files sit directly in the current directory instead, it
will detect that automatically.

What it does:
1. Walks every local *.html file to build a map of
   "site path" -> "local file path" (e.g. "/2011/10/18/theres-flouride-in-my-water/"
   -> "outfog.com/2011/10/18/theres-flouride-in-my-water/index.html").
2. Scans every local html file for absolute links to outfog.com WITH a
   path (bare-domain links are left alone).
3. For each match, looks up the target in the map. If found, rewrites
   it to a relative link computed from the *linking* file's own location.
4. If NOT found (page wasn't downloaded, or it's a tag/author/pagination
   page never included in the sitemap crawl), leaves the link untouched
   and reports it so you can review.

Note: this only processes *.html files. RSS/XML files (e.g. "rss",
wp-json oembed responses) are intentionally left alone -- they aren't
browsable pages and their URLs are URL-encoded, not plain hrefs.

Usage:
    python3 fix_internal_links.py
"""

import re
import os
import glob

DOMAIN_RE = re.compile(r'https?://(?:www\.)?outfog\.com(/[^"\'\s)>&<]*)?')


def find_site_root():
    """Detect whether files live under an 'outfog.com/' host directory
    (no --no-host-directories was used) or directly in cwd."""
    if os.path.isdir('outfog.com'):
        return 'outfog.com'
    return '.'


def build_url_map(root):
    """Map site-path (e.g. '/2011/10/18/some-post/') -> local file path."""
    url_map = {}
    for fp in glob.glob(os.path.join(root, '**', '*.html'), recursive=True):
        rel = os.path.relpath(fp, root)
        rel_url = '/' + rel.replace(os.sep, '/')
        if rel_url.endswith('/index.html'):
            site_path = rel_url[: -len('index.html')]  # keep trailing slash
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
            if path in ('/', ''):
                # bare domain -- leave untouched
                return m.group(0)

            # Split off a #fragment (e.g. #comment-212) so lookup matches
            # the underlying page; reattach the fragment afterward.
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
        print('\nThese are typically tag/author/pagination pages never included in the')
        print('sitemap crawl, or pre-existing malformed links in the original content.')
    else:
        print('Every outfog.com link with a path resolved to a local file.')


if __name__ == '__main__':
    main()
