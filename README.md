# Out of the Fog

Archive of **Out of the Fog: Emerging Science from California's Central Coast**, the blog written by students in the Science Communication graduate program at UC Santa Cruz.

**Live site:** <https://outfog.com>

## Overview

This is a static copy of the original WordPress site. There is no build step and no server-side code: the files in this repository are served exactly as they are by GitHub Pages.

It holds about 343 posts from 2010 to 2018 and a few site pages (about, contact), plus the author, tag and archive pages, for 1,131 HTML pages in all. Each post keeps its original WordPress address (`/YYYY/MM/DD/post-name/`), so links from around the web still work.

## Layout

```         
/                         home page and the paginated post archive
YYYY/MM/DD/post-name/     one folder per post, each with an index.html
author/, tag/, ...        author and tag archive pages
about-us/, contact/       site pages
wp-content/uploads/       images, audio and video, in year/month folders
wp-content/themes/        theme CSS and JavaScript
wp-content/plugins/       plugin CSS
CNAME                     custom domain for GitHub Pages (do not delete)
```

## Hosting

- **GitHub Pages**, deployed from the `main` branch, root folder.
- **Custom domain:** `outfog.com`, set under Settings → Pages (this is what the `CNAME` file records). HTTPS is enforced, and GitHub renews the certificate automatically as long as the DNS records stay as they are.
- **DNS** is managed in the Bluehost account that holds the domain:
  - four `A` records for the root (`@`): `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
  - a `CNAME` for `www` pointing to `ucscscicomm.github.io`
- The domain registration must be kept renewed, or the site goes offline.

## Editing this site

- **Links are relative**, so how many `../` a link needs depends on how deep the page sits. A post (`YYYY/MM/DD/post-name/index.html`) is four folders deep, so it reaches shared files with `../../../../wp-content/...`.
- **Theme and plugin files have `?ver=` in their file names**, for example `general.min.js?ver=7.1`, and pages link to them with `%3F`. Don't rename them.
- **Site-wide changes** (a menu link, for example) mean editing every page, since each one carries its own copy of the header and menu. Preview with `grep -rIl 'text' --include='*.html' .`, commit before you change anything, apply with `sed` or `perl`, then review `git diff --stat` before pushing.
- **Size:** GitHub recommends keeping a Pages site under 1 GB. It is currently under that, so avoid adding large media.

## Changes from the original WordPress site (September 2026)

- Moved from WordPress hosting at Bluehost to GitHub Pages; `outfog.com` now points here.
- Removed the Subscribe page and its menu link.
- Updated menu links: **Science Notes** now goes to <https://ucsc-sciencenotes.org> and **About the Authors** goes to <https://scicom.ucsc.edu/students-and-alumni/scicom-students-and-alumni/>.
- Removed the archived reader comments (327 comments in 382 comment and reply blocks on 364 pages), together with the "Comments Feed" links in every page's head.
- Fixed broken image links in six December 2017 posts.
- Removed about duplicate image files (roughly 210 MB) whose names contained `?w=...`, and pointed the pages at the plain image files, to keep the site under 1 GB.

## Known limitations

- Anything that needed WordPress no longer works: the menu's search box, the subscribe form, comments.
- Pages still load some scripts from other sites: WordPress's CDN (`c0.wp.com`, for jQuery and similar), Jetpack Stats (`stats.wp.com`), and Google Tag Manager / Analytics snippets from the original site. If any of those shut down, pages still display, but the scripts stop loading.
- Links inside articles to other websites may have gone dead since the articles were published.

## Original WordPress site and backups

A full backup of the original site (files and database) was taken on 2026-09-19, before it was taken down. It is **not** in this repository.

If the original ever has to be restored, it needs PHP 7.4 or older (the Canvas theme and one plugin break on PHP 8).

## Related links

- Science Notes (the program's student feature-writing site): <https://ucsc-sciencenotes.org>
- UC Santa Cruz Science Communication Program: <https://scicom.ucsc.edu>

## Credits

Written by SciCom students, classes of 2011 to 2018. Thomas Sumner built the original WordPress site.

Site migrated and maintained by Peter Aldhous, continuing lecturer, UCSC Science Communication program, paldhous\@ucsc.edu
