#!/usr/bin/env bash
# Deploy the site to Cloudflare Pages by direct upload (no Git integration,
# so the private CV submodule is never needed). First time: npx wrangler login
set -euo pipefail

project="${CF_PAGES_PROJECT:-yicheng-zhang}"
root="$(cd "$(dirname "$0")/.." && pwd)"
site="$(mktemp -d)"
trap 'rm -rf "$site"' EXIT

cp -r "$root/index.html" "$root/assets" "$site/"
find "$site" -name .DS_Store -delete

cd "$root"
npx --yes wrangler@4 pages deploy "$site" \
  --project-name "$project" \
  --branch main \
  --commit-hash "$(git rev-parse HEAD)" \
  --commit-message "$(git log -1 --format=%s)" \
  --commit-dirty="$([ -n "$(git status --porcelain -- index.html assets)" ] && echo true || echo false)"
