# zycccishere.github.io

Personal academic homepage of Yicheng Zhang.

- Live (Cloudflare Pages): <https://yicheng-zhang.pages.dev/>
- GitHub Pages (<https://zycccishere.github.io/>) is set up via `.github/workflows/pages.yml`
  but currently blocked: Actions reports the account as locked for a billing issue.

Plain HTML + CSS with no build step, no external fonts and no JavaScript.

```
index.html                    the whole page
assets/css/style.css          styles (light + dark mode)
assets/Yicheng_Zhang_CV.pdf   compiled CV (generated, see below)
assets/favicon.svg
CV/                           git submodule -> zycccishere/CV (private)
scripts/build-cv.sh           compiles CV/main.tex into assets/
scripts/deploy-cloudflare.sh  uploads the site to Cloudflare Pages
.github/workflows/pages.yml   deploys to GitHub Pages on push to main
```

## Clone

```sh
git clone --recurse-submodules git@github.com:zycccishere/zycccishere.github.io.git
```

## Editing the page

Edit `index.html` and open it directly in a browser to preview. Then:

```sh
git commit -am "..." && git push   # version history (+ GitHub Pages once unblocked)
./scripts/deploy-cloudflare.sh     # publish to Cloudflare Pages
```

Cloudflare deploys are direct uploads from this machine (no Git integration),
so pushing alone does not update the Cloudflare site. First time only:
`npx wrangler@4 login`.

## Updating the CV

The CV lives in its own repo and is tracked here as a submodule.

```sh
# 1. edit and commit inside the submodule
cd CV
# ... edit main.tex ...
git commit -am "Update CV" && git push
cd ..

# 2. rebuild the PDF (needs LuaLaTeX + Noto fonts) and record the new submodule commit
./scripts/build-cv.sh
git add CV assets/Yicheng_Zhang_CV.pdf
git commit -m "Update CV" && git push
./scripts/deploy-cloudflare.sh
```

To pull CV changes made elsewhere (e.g. on Overleaf): `git submodule update --remote CV`,
then run step 2.

Because the CV repo is private, the deploy workflow does not check out the
submodule; it publishes the PDF committed in `assets/`.
