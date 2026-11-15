from pathlib import Path
import re

path = Path('index.html')
html = path.read_text(encoding='utf-8')
start = html.index('<section id="publications">')
end = html.index('</section>', start) + len('</section>')
old = html[start:end]
blocks = []
for match in re.finditer(r'<div class="pub">', old):
    depth = 0
    for tag in re.finditer(r'</?div\b[^>]*>', old[match.start():]):
        depth += -1 if tag.group().startswith('</') else 1
        if depth == 0:
            blocks.append(old[match.start():match.start()+tag.end()])
            break
assert len(blocks) == 8, 'Unexpected publication structure; refusing to overwrite.'
recuq, carr, centre, order, recomb, going, marie, esg = blocks
assert 'Towards Realistic Evaluation' in recuq
assert 'CENTRE:' in centre
assert 'Opening-oriented Cost' in order
assert 'Wanzhou Li, Haonan Chen' in recomb and 'Third author' in recomb
recuq = recuq.replace('ind-review', 'ind-pub').replace('badge-review', 'badge-pub')
recuq = recuq.replace('TMLR · 2026 · Major revision completed', 'TMLR · 2026 · Accepted')
recuq = recuq.replace('TMLR · 2026 · 大修已完成，仍在审', 'TMLR · 2026 · 已接收')
recuq = recuq.replace('>Under Review<', '>Accepted<').replace('>审稿中<', '>已接收<')
order = order.replace('ORDER · TACL · 2026 · Submitted', 'ORDER · TACL · 2026 · Under review')
order = order.replace('ORDER · TACL · 2026 · 已投稿', 'ORDER · TACL · 2026 · 审稿中')
order = order.replace('>Submitted<', '>Under Review<').replace('>已投稿<', '>审稿中<')
centre = centre.replace('ind-review', 'ind-revision').replace('badge-review', 'badge-revision')
centre = centre.replace('EACL 2027 · Under review', '2026 · Preparing journal submission')
centre = centre.replace('EACL 2027 · 审稿中', '2026 · 修改并准备期刊投稿')
centre = centre.replace('>Under Review<', '>In Revision<').replace('>审稿中<', '>修改中<')
header = old[:old.index('  <div class="pub-group">')]
groups = [
    ('Accepted and Published Work', '已接收及已发表', [recuq, esg]),
    ('Submitted and Under Review', '已投稿及审稿中', [carr, order, recomb]),
    ('Manuscripts in Revision and Preparation', '修改及准备中的手稿', [centre, going, marie]),
]
parts = [header]
for en, zh, entries in groups:
    parts.append('  <div class="pub-group">\n')
    parts.append(f'    <div class="pub-group-label en">{en}</div><div class="pub-group-label zh">{zh}</div>\n')
    parts.extend('    ' + entry + '\n' for entry in entries)
    parts.append('  </div>\n')
parts.append('</section>')
updated = html[:start] + ''.join(parts) + html[end:]
updated = updated.replace('href="Hao_Wu_CV.pdf"', 'href="Hao_Wu_CV.pdf?v=20261115"')
assert 'EACL 2027' not in updated
assert updated.count('<div class="pub">') == 8
assert 'TMLR · 2026 · Accepted' in updated
assert 'ORDER · TACL · 2026 · Under review' in updated
assert 'RECOMB 2027 · Submitted' in updated
assert '2026 · Preparing journal submission' in updated
path.write_text(updated, encoding='utf-8')
