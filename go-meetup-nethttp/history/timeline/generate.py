"""Generate the timeline backgrounds. Requires Pillow and Arial fonts on macOS."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

out = Path(__file__).parent
regular = '/System/Library/Fonts/Supplemental/Arial.ttf'
bold = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
font = lambda size: ImageFont.truetype(regular, size)
strong = lambda size: ImageFont.truetype(bold, size)
W, H = 1920, 1080
left, right, axis = 120, 1800, 560
step = (right-left)/17
items = [
    (2012, 1, 'Go 1', 'net/http'),
    (2014, 2, 'Context', 'patterns'),
    (2016, 3, 'Go 1.6', 'HTTP/2'),
    (2017, 4, 'Go 1.8', 'shutdown'),
    (2022, 5, 'Go 1.18', 'fuzzing'),
    (2024, 6, 'Go 1.22', 'ServeMux'),
    (2025, 7, 'Go 1.24–25', 'protocols / CSRF'),
    (2026, 7, 'Go 1.27', 'HTTP/2 move'),
]
for stage in range(8):
    img = Image.new('RGB', (W, H), '#0c1723')
    d = ImageDraw.Draw(img)
    d.text((100, 80), 'THE GO HTTP TIMELINE', font=strong(62), fill='#f5fafc')
    subtitle = '2009–2026  |  Follow the releases, then run the code' if stage == 0 else 'A new stop on the timeline  |  Then: how it works and a live demo'
    d.text((102, 170), subtitle, font=font(32), fill='#a8c7d2')
    d.line((left, axis, right, axis), fill='#547783', width=5)
    for year in range(2009, 2027):
        x = round(left + (year-2009)*step)
        d.line((x, axis-12, x, axis+12), fill='#8dafb9', width=3)
        d.text((x, axis+38), str(year), font=font(25), fill='#d2e7eb', anchor='ma')
    for year, unlocked, name, detail in items:
        if stage < unlocked:
            continue
        x = round(left + (year-2009)*step)
        # Adjacent 2025/2026 milestones use opposite sides to avoid collisions.
        above = year not in (2014, 2017, 2024, 2026)
        end = axis - 100 if above else axis + 118
        color = '#58d3bc' if stage == unlocked else '#7599a1'
        d.line((x, axis, x, end), fill=color, width=3)
        d.ellipse((x-9, axis-9, x+9, axis+9), fill=color)
        anchor = 'mb' if above else 'mt'
        ty = end-16 if above else end+16
        d.text((x, ty - 28 if above else ty), name, font=strong(22), fill=color, anchor=anchor)
        d.text((x, ty if above else ty + 28), detail, font=strong(22), fill=color, anchor=anchor)
    d.text((100, 985), 'net/http  ·  Go meetup  ·  research through October 2026', font=font(23), fill='#7596a0')
    img.save(out / f'timeline-{stage}.png', optimize=True)
