#!/usr/bin/env python3
"""Assemble sections/*.html (in ORDER) into index.html using index_template.html."""
import os
HERE=os.path.dirname(os.path.abspath(__file__)); SEC=os.path.join(HERE,"sections")
ORDER=["00_nav","01_hero","02_about","03_marquee","04_services","09_testimonials",
       "05_spots","06_gallery","07_pricing","09f_faq","10_booking","08_merch","11_footer"]
def read(p):
    return open(p,encoding="utf-8").read() if os.path.exists(p) else ""
# Assemble: nav stays outside <main>; everything from hero..merch sits inside the
# #main landmark; footer stays outside. Robust to missing sections (e.g. 09f_faq).
parts=[]; opened=False
for n in ORDER:
    if n=="11_footer" and opened:
        parts.append("</main>"); opened=False
    parts.append(f"<!-- {n} -->\n"+read(os.path.join(SEC,n+".html")))
    if n=="00_nav" and not opened:
        parts.append('<main id="main">'); opened=True
if opened:
    parts.append("</main>")
main="\n".join(parts)
head=read(os.path.join(SEC,"_head.html"))
tpl=read(os.path.join(HERE,"index_template.html"))
out=tpl.replace("<!--HEAD_EXTRA-->",head).replace("<!--MAIN-->",main)
open(os.path.join(HERE,"index.html"),"w",encoding="utf-8").write(out)
present=[n for n in ORDER if os.path.exists(os.path.join(SEC,n+".html"))]
print(f"built index.html — {len(present)}/{len(ORDER)} sections: {', '.join(present)}")
