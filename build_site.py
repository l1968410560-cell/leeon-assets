# -*- coding: utf-8 -*-
"""LEEON 素材库网站生成器

扫描 素材库/ 与 模板库/，同步资源到 assets/，生成自包含 index.html。
新增素材后重新运行本脚本即可。
"""
import base64
import html
import re
import shutil
from pathlib import Path

ROOT = Path(r"D:\AI\codex\projects\leeon账号运营\leeon")
MAT = ROOT / "素材库"
TPL = ROOT / "模板库"
OUT = ROOT / "素材库网站"
ASSETS = OUT / "assets"


def sync(src: Path, dst: Path):
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def read_svg(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def clean_svg(svg: str) -> str:
    svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S)
    return re.sub(r"\s+", " ", svg).strip()


def png_uri(p: Path) -> str:
    return "data:image/png;base64," + base64.b64encode(p.read_bytes()).decode("ascii")


def svg_box_cell(rel_path: str, name: str, data_f: str, cat: str = ""):
    svg = clean_svg(read_svg(ROOT / rel_path))
    tag = f' data-tag="{esc(cat)}"' if cat else ""
    return (
        f'<div class="cell img-cell" data-name="{esc(name)}"{tag} data-f="{data_f}">'
        f'<div class="svgbox">{svg}</div>'
        f'<div class="nm">{esc(name)}</div></div>'
    )


def png_cell(item, photo: bool = False, data_f: str = "tmpl"):
    cls = " photo" if photo else ""
    uri = png_uri(ROOT / item["rel"])
    return (
        f'<div class="cell img-cell{cls}" data-name="{esc(item["name"])}" data-f="{data_f}">'
        f'<img src="{uri}" alt="{esc(item["name"])}">'
        f'<div class="nm">{esc(item["name"])}</div></div>'
    )


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def motion_cell(item):
    poster = MAT / "动效" / "video-shotcraft" / "poster" / (item["name"] + ".jpg")
    poster_attr = (
        f' poster="assets/动效/video-shotcraft/poster/{item["name"]}.jpg"'
        if poster.exists()
        else ""
    )
    return (
        f'<div class="cell vid-cell" data-name="{esc(item["name"])}" data-f="motion">'
        f'<video controls preload="none"{poster_attr}><source src="assets/{item["rel"]}" type="video/mp4"></video>'
        f'<div class="nm">{esc(item["name"])}</div></div>'
    )


def collect_icons(sub: str):
    items = []
    folder = MAT / "图标库" / sub
    if folder.exists():
        for p in sorted(folder.glob("*.svg")):
            items.append({"name": p.stem, "svg": read_svg(p)})
    return items


def collect_images(folder: Path, tag: str = ""):
    items = []
    if folder.exists():
        for p in sorted(folder.glob("*.png")):
            items.append({"name": p.stem, "rel": p.relative_to(ROOT).as_posix(), "tag": tag})
    return items


def main():
    # ---- 同步资源到 assets/ ----
    pairs = [
        (MAT / "图标库", ASSETS / "图标库"),
        (MAT / "IP形象", ASSETS / "IP形象"),
        (MAT / "插画", ASSETS / "插画"),
        (MAT / "品牌图标", ASSETS / "品牌图标"),
        (MAT / "评论截图卡片", ASSETS / "评论截图卡片"),
        (MAT / "字体", ASSETS / "字体"),
        (MAT / "品牌资产", ASSETS / "品牌资产"),
        (TPL / "视频风格样板", ASSETS / "视频风格模板"),
        (MAT / "动效", ASSETS / "动效"),
    ]
    for src, dst in pairs:
        if src.exists():
            sync(src, dst)

    docs_src = [MAT / "README.md", MAT / "素材库扩充清单.md"]
    docs_dir = ASSETS / "文档"
    if docs_dir.exists():
        shutil.rmtree(docs_dir)
    docs_dir.mkdir(parents=True)
    for d in docs_src:
        if d.exists():
            shutil.copy2(d, docs_dir / d.name)

    # ---- 收集数据 ----
    common_icons = collect_icons("通用图标")
    brand_icons = collect_icons("品牌图标")
    bots = []
    bot_dir = MAT / "IP形象" / "Q版机器人-bottts"
    for p in sorted(bot_dir.glob("*.svg")):
        bots.append({"name": p.stem, "rel": p.relative_to(ROOT).as_posix()})

    illos = []
    illo_dir = MAT / "插画" / "科技风-unDraw"
    for p in sorted(illo_dir.rglob("*.svg")):
        cat = p.parent.name
        illos.append({"name": p.stem, "cat": cat, "rel": p.relative_to(ROOT).as_posix()})

    brand_pngs = collect_images(MAT / "品牌图标")
    comments = collect_images(MAT / "评论截图卡片")
    styles = collect_images(TPL / "视频风格样板")
    motions = []
    motion_media = MAT / "动效" / "video-shotcraft" / "media"
    if motion_media.exists():
        for p in sorted(motion_media.glob("*.mp4")):
            motions.append({"name": p.stem, "rel": p.relative_to(ROOT).as_posix()})

    fonts = []
    for d in sorted((MAT / "字体").iterdir()):
        if d.is_dir():
            otfs = sorted(d.glob("*.otf"))
            weights = [p.name.replace(d.name + "-", "").replace(".otf", "") for p in otfs]
            fonts.append({"dir": d.name, "rel": d.relative_to(ROOT).as_posix(), "weights": weights, "count": len(otfs)})

    def svg_card(item, color="currentColor"):
        svg = item["svg"]
        svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S)
        svg = re.sub(r"\s+", " ", svg).strip()
        return (
            f'<div class="cell ic" data-name="{esc(item["name"])}">'
            f'<div class="icon" style="color:{color}">{svg}</div>'
            f'<div class="nm">{esc(item["name"])}</div></div>'
        )

    # ---- 组装 HTML ----
    parts = []
    parts.append(f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>LEEON 素材库 · 仓库页</title>
<style>
@font-face {{ font-family:'SourceHanSans'; src:url('assets/字体/思源黑体-SourceHanSansCN/SourceHanSansCN-Regular.otf'); font-weight:400; }}
@font-face {{ font-family:'SourceHanSans'; src:url('assets/字体/思源黑体-SourceHanSansCN/SourceHanSansCN-Bold.otf'); font-weight:700; }}
@font-face {{ font-family:'SourceHanSerif'; src:url('assets/字体/思源宋体-SourceHanSerifCN/SourceHanSerifCN-Regular.otf'); font-weight:400; }}
* {{ box-sizing:border-box; margin:0; padding:0; }}
body {{ background:#05060B; color:#E8EAED; font-family:'SourceHanSans','Microsoft YaHei',sans-serif; }}
body::before {{ content:''; position:fixed; inset:0; pointer-events:none; z-index:0;
  background-image:linear-gradient(rgba(255,255,255,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.05) 1px,transparent 1px);
  background-size:36px 36px;
  -webkit-mask-image:radial-gradient(ellipse at 50% 0%,#000 0%,transparent 75%);
  mask-image:radial-gradient(ellipse at 50% 0%,#000 0%,transparent 75%); }}
.wrap {{ position:relative; z-index:1; max-width:1280px; margin:0 auto; padding:48px 32px 96px; }}
header {{ border-bottom:1px solid rgba(255,255,255,.1); padding-bottom:28px; margin-bottom:36px; }}
h1 {{ font-family:'SourceHanSans'; font-weight:700; font-size:42px; letter-spacing:3px; }}
h1 em {{ color:#22D3EE; font-style:normal; }}
.sub {{ color:#8A8F9C; font-size:14px; margin-top:10px; }}
.stats {{ display:flex; gap:10px; flex-wrap:wrap; margin-top:20px; }}
.stat {{ border:1px solid rgba(255,255,255,.12); border-radius:10px; padding:10px 16px; font-size:13px; background:rgba(255,255,255,.03); }}
.stat b {{ color:#22D3EE; font-family:'Consolas',monospace; font-size:18px; margin-right:6px; }}
.toolbar {{ display:flex; gap:12px; align-items:center; flex-wrap:wrap; margin:28px 0; }}
input[type=search] {{ flex:1; min-width:220px; background:rgba(255,255,255,.05); border:1px solid rgba(255,255,255,.15);
  color:#E8EAED; padding:12px 16px; border-radius:10px; font-size:14px; outline:none; }}
input[type=search]:focus {{ border-color:#22D3EE; }}
.chip {{ border:1px solid rgba(255,255,255,.15); background:transparent; color:#B9BEC9; padding:8px 14px;
  border-radius:999px; font-size:13px; cursor:pointer; }}
.chip.on {{ border-color:#22D3EE; color:#22D3EE; }}
section {{ margin-top:56px; }}
h2 {{ font-size:26px; font-weight:700; letter-spacing:1px; margin-bottom:6px; }}
h2 small {{ color:#8A8F9C; font-size:13px; font-weight:400; margin-left:8px; }}
.desc {{ color:#8A8F9C; font-size:13px; margin-bottom:20px; }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(120px,1fr)); gap:12px; }}
.cell {{ border:1px solid rgba(255,255,255,.1); border-radius:10px; padding:14px; background:rgba(255,255,255,.03); }}
.cell .nm {{ font-size:11px; color:#B9BEC9; margin-top:8px; word-break:break-all; }}
.ic .icon {{ display:flex; align-items:center; justify-content:center; height:48px; }}
.ic .icon svg {{ width:28px; height:28px; }}
.img-cell {{ padding:8px; }}
.img-cell img {{ width:100%; height:150px; object-fit:contain; display:block; background:#fff; border-radius:8px; }}
.img-cell.photo img {{ object-fit:cover; height:110px; }}
.vid-grid {{ grid-template-columns:repeat(auto-fill,minmax(300px,1fr)); }}
.vid-cell video {{ width:100%; height:180px; background:#000; border-radius:8px; display:block; }}
.svgbox {{ height:150px; background:#fff; border-radius:8px; display:flex; align-items:center; justify-content:center; overflow:hidden; padding:6px; }}
.svgbox svg {{ max-width:100%; max-height:100%; }}
.illo-grid {{ grid-template-columns:repeat(auto-fill,minmax(220px,1fr)); }}
.band-grid {{ grid-template-columns:repeat(auto-fill,minmax(260px,1fr)); }}
.swatches {{ display:flex; gap:14px; flex-wrap:wrap; }}
.swatch {{ width:150px; border-radius:10px; overflow:hidden; border:1px solid rgba(255,255,255,.12); }}
.swatch .bar {{ height:64px; }}
.swatch .info {{ padding:10px; font-size:12px; }}
.swatch .info b {{ display:block; font-size:13px; margin-bottom:2px; }}
.swatch .info span {{ color:#8A8F9C; font-family:Consolas,monospace; }}
.font-card {{ border:1px solid rgba(255,255,255,.12); border-radius:12px; padding:22px; background:rgba(255,255,255,.03); }}
.font-card h3 {{ font-size:16px; }}
.font-card .spec {{ font-size:26px; margin:16px 0 8px; line-height:1.5; }}
.font-card .meta {{ color:#8A8F9C; font-size:12px; }}
.font-card .w {{ display:inline-block; margin:3px 4px 0 0; padding:3px 8px; border:1px solid rgba(255,255,255,.15);
  border-radius:6px; font-size:11px; color:#B9BEC9; }}
.links a {{ color:#22D3EE; text-decoration:none; margin-right:16px; font-size:13px; }}
footer {{ margin-top:80px; border-top:1px solid rgba(255,255,255,.1); padding-top:24px; color:#8A8F9C; font-size:12px; line-height:1.8; }}
table {{ width:100%; border-collapse:collapse; font-size:13px; }}
td,th {{ border:1px solid rgba(255,255,255,.1); padding:8px 10px; text-align:left; }}
.hidden {{ display:none !important; }}
@media (max-width:640px) {{ h1 {{ font-size:30px; }} .wrap {{ padding:28px 16px 64px; }} }}
</style>
</head>
<body>
<div class="wrap">
<header>
  <h1>LEEON <em>素材库</em></h1>
  <div class="sub">数据党 leeon · 深空数据舱 · 全平台可复用资产仓库 &nbsp;|&nbsp; 更新于 {html.escape(__import__('datetime').date.today().isoformat())}</div>
  <div class="stats">
    <div class="stat"><b>{len(common_icons)}</b>通用图标</div>
    <div class="stat"><b>{len(brand_icons)}</b>品牌图标</div>
    <div class="stat"><b>{len(bots)}</b>IP 形象</div>
    <div class="stat"><b>{len(illos)}</b>科技插画</div>
    <div class="stat"><b>{sum(f['count'] for f in fonts)}</b>中文字体字重</div>
    <div class="stat"><b>{len(styles)}</b>视频风格模板</div>
    <div class="stat"><b>{len(comments)}</b>评论截图</div>
    <div class="stat"><b>{len(motions)}</b>动效</div>
  </div>
</header>

<div class="toolbar">
  <input type="search" id="q" placeholder="搜索素材名，如 robot / chart / leeon…">
  <button class="chip on" data-f="all">全部</button>
  <button class="chip" data-f="brand">品牌资产</button>
  <button class="chip" data-f="icon">图标</button>
  <button class="chip" data-f="ip">IP 形象</button>
  <button class="chip" data-f="illo">插画</button>
  <button class="chip" data-f="font">字体</button>
  <button class="chip" data-f="tmpl">视频模板</button>
  <button class="chip" data-f="motion">动效</button>
</div>
""")

    # 品牌资产
    swatches = [
        ("近黑底", "#05060B", "#05060B 主背景"),
        ("暖白", "#E8EAED", "#E8EAED 正文"),
        ("强调青", "#22D3EE", "#22D3EE 数字/结论"),
        ("灰阶", "#3A3F4A", "#3A3F4A 分隔线"),
        ("卡片底", "#0B1220", "#0B1220 面板"),
    ]
    sw_html = "".join(
        f'<div class="swatch"><div class="bar" style="background:{c}"></div>'
        f'<div class="info"><b>{n}</b><span>{c}</span><br>{u}</div></div>'
        for n, c, u in swatches
    )
    parts.append(f"""
<section id="brand" data-f="brand">
  <h2>品牌资产 <small>深空数据舱 · 全平台视觉基准</small></h2>
  <div class="desc">做图 / PPT / 视频前先读品牌卡；色板预览见 assets/品牌资产/。</div>
  <div class="swatches">{sw_html}</div>
  <div class="links" style="margin-top:16px">
    <a href="assets/品牌资产/品牌卡.md" target="_blank">品牌卡（色板+字体+质感+动效）</a>
    <a href="assets/品牌资产/色板-深空数据舱.html" target="_blank">色板预览</a>
    <a href="assets/品牌资产/头像与水印.md" target="_blank">头像与水印规范</a>
  </div>
</section>
""")

    # 图标
    icons_html = "".join(svg_card(i) for i in common_icons)
    brand_html = "".join(svg_card(i) for i in brand_icons)
    parts.append(f"""
<section id="icons" data-f="icon">
  <h2>图标库 · 通用 <small>{len(common_icons)} 枚 · Lucide ISC</small></h2>
  <div class="desc">线性图标，默认白灰；SVG 用 currentColor，按当期主色改外层 color（如 #22D3EE）。</div>
  <div class="grid">{icons_html}</div>
  <h2 style="margin-top:40px">图标库 · 品牌 <small>{len(brand_icons)} 枚 · Simple Icons CC0，保留官方色</small></h2>
  <div class="grid">{brand_html}</div>
</section>
""")

    brand_png_html = "".join(png_cell(i, data_f="icon") for i in brand_pngs)
    parts.append(f"""
<section data-f="icon">
  <h2>品牌图标 · PNG <small>{len(brand_pngs)} 张 · 透明底位图</small></h2>
  <div class="grid band-grid">{brand_png_html}</div>
</section>
""")

    # IP 形象
    bot_html = "".join(svg_box_cell(b["rel"], b["name"], "ip") for b in bots)
    parts.append(f"""
<section id="ip" data-f="ip">
  <h2>IP 形象 <small>{len(bots)} 个 · DiceBear bottts 免费商用</small></h2>
  <div class="desc">种子固定可复现；leeon-01~05 为主形象候选，另有数据/代码/实验/未来机器人。</div>
  <div class="grid">{bot_html}</div>
</section>
""")

    # 插画
    illo_html = "".join(svg_box_cell(i["rel"], i["name"], "illo", i["cat"]) for i in illos)
    parts.append(f"""
<section id="illo" data-f="illo">
  <h2>科技风插画 <small>{len(illos)} 张 · unDraw 免费商用免署名</small></h2>
  <div class="desc">原图主色 #6c63ff；做深空风时全局替换为 #22D3EE，附色压成灰阶（≤3 色）。</div>
  <div class="grid illo-grid">{illo_html}</div>
</section>
""")

    # 字体
    font_cards = ""
    for f in fonts:
        fam = "SourceHanSans" if "黑体" in f["dir"] else "SourceHanSerif"
        sample = "数据党 leeon · AI 真相拆解机" if "黑体" in f["dir"] else "引用一段有编辑感的话：先技术，后搞钱。"
        weights = "".join(f'<span class="w">{esc(w)}</span>' for w in f["weights"])
        font_cards += (
            f'<div class="font-card" data-f="font" data-name="{esc(f["dir"])}">'
            f'<h3>{esc(f["dir"])} <small style="color:#8A8F9C">· {f["count"]} 字重 · SIL OFL 免费商用</small></h3>'
            f'<div class="spec" style="font-family:\'{fam}\'">{sample}</div>'
            f'<div class="w">{weights}</div>'
            f'<div class="meta">位置：assets/{esc(f["rel"].replace(chr(92), "/"))}</div>'
            f'</div>'
        )
    parts.append(f"""
<section id="fonts" data-f="font">
  <h2>字体 <small>{sum(f['count'] for f in fonts)} 字重 · 思源黑体 / 宋体</small></h2>
  <div class="desc">标题得意黑（系统）、数据 JetBrains Mono（系统）、正文思源黑体 Light；规范见品牌卡。</div>
  <div class="grid" style="grid-template-columns:repeat(auto-fill,minmax(340px,1fr))">{font_cards}</div>
</section>
""")

    # 品牌 PNG / 评论截图 / 视频模板 / 动效
    motion_html = "".join(motion_cell(m) for m in motions)
    parts.append(f"""
<section id="tmpl" data-f="tmpl">
  <h2>视频风格模板 <small>{len(styles)} 套 · 见模板库/视频风格样板</small></h2>
  <div class="desc">默认深空数据舱；选型规则见 assets/视频风格模板 说明。</div>
  <div class="grid band-grid">{''.join(png_cell(s) for s in styles)}</div>
</section>

<section id="comments" data-f="tmpl">
  <h2>评论截图卡片 <small>{len(comments)} 张</small></h2>
  <div class="grid">{''.join(png_cell(c, photo=True) for c in comments)}</div>
</section>

<section id="motion" data-f="motion">
  <h2>动效 <small>{len(motions)} 条 · video-shotcraft · Apache-2.0</small></h2>
  <div class="desc">Remotion 镜头配方动效样片（每条 4–6s，可商用，需保留署名）；完整清单 / 配方文档 / 许可证见 assets/动效/video-shotcraft/</div>
  <div class="grid vid-grid">{motion_html}</div>
</section>

<section id="docs">
  <h2>文档</h2>
  <div class="links">
    <a href="assets/文档/README.md" target="_blank">素材库总索引</a>
    <a href="assets/文档/素材库扩充清单.md" target="_blank">扩充清单（待补项）</a>
    <a href="assets/图标库/README.md" target="_blank">图标库说明</a>
  </div>
</section>
""")

    parts.append(f"""
<footer>
  <b>许可证速查</b>
  <table>
    <tr><th>素材</th><th>来源</th><th>许可</th></tr>
    <tr><td>通用图标</td><td>Lucide</td><td>ISC，免费商用免署名</td></tr>
    <tr><td>品牌图标</td><td>Simple Icons</td><td>CC0；logo 本身为各公司商标，遵守品牌规范</td></tr>
    <tr><td>IP 形象</td><td>DiceBear bottts</td><td>免费商用</td></tr>
    <tr><td>科技插画</td><td>unDraw</td><td>免费商用免署名</td></tr>
    <tr><td>思源黑体/宋体</td><td>Adobe Fonts</td><td>SIL OFL 1.1</td></tr>
    <tr><td>得意黑 / JetBrains Mono</td><td>开源字体</td><td>SIL OFL</td></tr>
    <tr><td>动效</td><td>video-shotcraft（Vincentwei1021）</td><td>Apache-2.0，保留署名</td></tr>
  </table>
  <p style="margin-top:14px">本页由 build_site.py 自动生成：新增素材 → 运行脚本 → 提交推送。&copy; leeon</p>
</footer>
</div>
<script>
const q = document.getElementById('q');
let cur = 'all';
function apply(){{
  const kw = q.value.trim().toLowerCase();
  document.querySelectorAll('.cell').forEach(c => {{
    const name = (c.dataset.name||'').toLowerCase() + ' ' + (c.dataset.tag||'').toLowerCase();
    const hitF = cur==='all' || c.dataset.f===cur;
    const hitK = !kw || name.includes(kw);
    c.classList.toggle('hidden', !(hitF && hitK));
  }});
}}
q.addEventListener('input', apply);
document.querySelectorAll('.chip').forEach(ch => ch.addEventListener('click', () => {{
  document.querySelectorAll('.chip').forEach(x => x.classList.remove('on'));
  ch.classList.add('on'); cur = ch.dataset.f; apply();
}}));
</script>
</body>
</html>
""")

    OUT.mkdir(exist_ok=True)
    (OUT / "index.html").write_text("\n".join(parts), encoding="utf-8")
    print("OK: index.html generated")
    print(f"icons={len(common_icons)} brand={len(brand_icons)} bots={len(bots)} illos={len(illos)} fonts={len(fonts)} styles={len(styles)} comments={len(comments)} motions={len(motions)}")


if __name__ == "__main__":
    main()
