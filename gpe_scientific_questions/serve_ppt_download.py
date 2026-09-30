#!/usr/bin/env python3
"""A same-origin download page exposing only four intended slide deliverables.

This server never serves the repository as a directory. It accepts preview
hosts, is iframe-friendly, and uses only relative browser-facing URLs. Run via
Arena's background process tool, not a timeout-limited shell command.
"""
from __future__ import annotations

import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

HERE = Path(__file__).resolve().parent
STEM = "Traditional_GPE_Common_Problems_Editable"
FILES = {
    f"/files/{STEM}.pptx": (HERE / f"{STEM}.pptx",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation", True),
    f"/files/{STEM}.svg": (HERE / f"{STEM}.svg", "image/svg+xml", True),
    f"/files/{STEM}.png": (HERE / f"{STEM}.png", "image/png", True),
    f"/files/{STEM}_Files.zip": (HERE / f"{STEM}_Files.zip", "application/zip", True),
    "/preview.png": (HERE / f"{STEM}.png", "image/png", False),
}
PAGE = f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>传统凝胶共性问题｜完全可编辑PPT</title>
<style>
*{{box-sizing:border-box}} body{{margin:0;background:#f3f6fa;color:#172b46;font-family:'Microsoft YaHei','Noto Sans SC',Arial,sans-serif}}
main{{max-width:1250px;margin:0 auto;padding:40px 24px 28px}}
.badge{{font-size:12px;letter-spacing:.12em;font-weight:700;color:#286b9f;margin-bottom:12px}}
h1{{font-size:clamp(24px,3vw,36px);line-height:1.35;margin:0 0 14px}}
p{{line-height:1.75;color:#586e84;margin:0 0 22px}}
.actions{{display:flex;flex-wrap:wrap;gap:12px;margin-bottom:24px}}
a.button{{display:inline-flex;align-items:center;justify-content:center;text-decoration:none;font-weight:700;padding:14px 20px;border-radius:10px;border:1px solid #cfddea;background:white;color:#245b89}}
a.button.primary{{color:white;background:#266fa6;border-color:#266fa6}} a.button:hover{{filter:brightness(.94)}}
.preview{{background:white;border-radius:14px;box-shadow:0 8px 36px #172b460e;border:1px solid #dde5ee;overflow:hidden}}
.preview img{{display:block;width:100%;height:auto}}
.details{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:22px}}
.detail{{padding:18px 20px;background:white;border:1px solid #dde5ee;border-radius:12px}}
.detail strong{{display:block;margin-bottom:8px;color:#225a8c}} .detail span{{font-size:14px;line-height:1.7;color:#61758a}}
footer{{font-size:12px;color:#6d7f92;margin-top:22px;line-height:1.8}}
@media(max-width:700px){{main{{padding:26px 16px}}.details{{grid-template-columns:1fr}}.actions a{{width:100%}}}}
</style></head>
<body><main>
<div class="badge">NATIVE EDITABLE POWERPOINT · SINGLE SLIDE</div>
<h1>传统凝胶电解质的两大共性挑战</h1>
<p>已经单独重画为16:9单页PPT。206个原生对象，没有嵌入整页图片；文字、骨架、离子、箭头、电极和膜层均可单独修改。</p>
<div class="actions">
<a class="button primary" href="/files/{STEM}.pptx" download>下载单页 PPT · 全部元素可编辑</a>
<a class="button" href="/files/{STEM}_Files.zip" download>打包下载 · PPT / SVG / PNG</a>
<a class="button" href="/files/{STEM}.svg" download>下载 SVG 矢量源</a>
</div>
<div class="preview"><img src="/preview.png" alt="传统凝胶的体相离子传输受限与电极界面失稳，两图对比科学问题页"></div>
<div class="details">
<div class="detail"><strong>01 · 体相离子传输</strong><span>连续液相与网络限域对比：路径曲折、局部配位滞留和有效通道不连续。</span></div>
<div class="detail"><strong>02 · 电极 / 凝胶界面</strong><span>局部接触空隙、非均匀SEI/CEI、膜层破裂重构及局部通量不均。</span></div>
<div class="detail"><strong>逐个编辑</strong><span>PowerPoint：开始 → 选择 → 选择窗格。按“问题一-”“问题二-”对象名定位；曲线可右键编辑顶点。</span></div>
</div>
<footer>上方图片仅供预览；下载的PPT不是这张图片。图示为常见挑战的定性示意，不表示所有传统凝胶必然失效，也不包含具体研究配方。单页PPT备注附讲稿和科学边界。</footer>
</main></body></html>"""


def response_for(url):
    """Return bytes and headers for a fixed allowed route; no path joining."""
    path = urlsplit(url).path
    if path == "/":
        return 200, PAGE.encode("utf-8"), {"Content-Type": "text/html; charset=utf-8"}
    if path == "/health":
        return 200, b"ok", {"Content-Type": "text/plain; charset=utf-8"}
    item = FILES.get(path)
    if item is None:
        return 404, b"Not found", {"Content-Type": "text/plain; charset=utf-8"}
    file, mime, attachment = item
    if not file.is_file():
        return 404, b"File not found", {"Content-Type": "text/plain; charset=utf-8"}
    headers = {"Content-Type": mime}
    if attachment:
        headers["Content-Disposition"] = f'attachment; filename="{file.name}"'
    return 200, file.read_bytes(), headers


class Handler(BaseHTTPRequestHandler):
    def respond(self, head=False):
        status, body, headers = response_for(self.path)
        self.send_response(status)
        for key, value in headers.items():
            self.send_header(key, value)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        if not head:
            self.wfile.write(body)

    def do_GET(self):
        self.respond()

    def do_HEAD(self):
        self.respond(head=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    for path, _, _ in FILES.values():
        if not path.is_file():
            raise SystemExit(f"Build the slide before starting this server: {path.name}")
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"Editable PPT download page listening on {args.host}:{args.port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
