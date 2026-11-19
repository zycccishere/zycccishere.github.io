#!/usr/bin/env bash
# Build the CV from the CV/ submodule and copy the PDF into the site.
# Requires pdfLaTeX with the noto-serif / noto-sans packages.
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
out="$root/assets/Yicheng_Zhang_CV.pdf"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

if [ ! -f "$root/CV/main.tex" ]; then
  echo "CV/main.tex not found. Run: git submodule update --init" >&2
  exit 1
fi

cd "$root/CV"
# \cvpublic hides private contact details (phone) in the published PDF.
if ! latexmk -pdf -usepretex='\def\cvpublic{}' -interaction=nonstopmode -halt-on-error -outdir="$tmp" main.tex >"$tmp/build.log" 2>&1; then
  grep -E "^!" -A4 "$tmp/build.log" >&2 || tail -40 "$tmp/build.log" >&2
  exit 1
fi

cp "$tmp/main.pdf" "$out"
echo "Built $(basename "$out") from CV@$(git rev-parse --short HEAD)"
