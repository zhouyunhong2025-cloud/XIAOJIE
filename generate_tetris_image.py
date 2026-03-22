#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont

# Create image with gradient-like background
width, height = 400, 500
image = Image.new('RGB', (width, height), color='#0f0f1e')
draw = ImageDraw.Draw(image, 'RGBA')

# Fill with dark blue gradient effect
for y in range(height):
    # Gradient from #1a1a2e (top) to #0f0f1e (bottom)
    r = int(26 + (15 - 26) * (y / height))
    g = int(26 + (15 - 26) * (y / height))
    b = int(46 + (30 - 46) * (y / height))
    draw.line([(0, y), (width, y)], fill=(r, g, b))

# Game container
draw.rectangle([50, 60, 350, 440], outline='#3498db', width=2)

# Grid background
grid_color = '#333333'
for x in range(50, 351, 30):
    draw.line([(x, 60), (x, 440)], fill=grid_color, width=1)
for y in range(60, 441, 30):
    draw.line([(50, y), (350, y)], fill=grid_color, width=1)

# Falling cyan I-piece
colors = {
    'cyan': '#1abc9c',
    'orange': '#e67e22',
    'blue': '#3498db',
    'purple': '#9b59b6',
    'green': '#2ecc71',
    'red': '#e74c3c'
}

# Draw falling piece (cyan I-piece vertical)
for i in range(3):
    x = 155
    y = 80 + i * 30
    draw.rectangle([x, y, x + 30, y + 30], fill=colors['cyan'], outline='#ffffff', width=1)

# Draw stacked blocks at bottom
# Memory (orange)
for i in range(3):
    x, y = 80, 370 - i * 30
    draw.rectangle([x, y, x + 30, y + 30], fill=colors['orange'], outline='#ffffff', width=1)

# Skill (blue)
for i in range(2):
    x, y = 110, 370 - i * 30
    draw.rectangle([x, y, x + 30, y + 30], fill=colors['blue'], outline='#ffffff', width=1)

# Alignment (purple)
for i in range(2):
    x, y = 140, 370 - i * 30
    draw.rectangle([x, y, x + 30, y + 30], fill=colors['purple'], outline='#ffffff', width=1)

# Rule (green)
for i in range(2):
    x, y = 260, 370 - i * 30
    draw.rectangle([x, y, x + 30, y + 30], fill=colors['green'], outline='#ffffff', width=1)

# Other (red)
x, y = 230, 370
draw.rectangle([x, y, x + 30, y + 30], fill=colors['red'], outline='#ffffff', width=1)

# Status bar
draw.rectangle([50, 450, 350, 490], outline='#3498db', width=1, fill='#0a0a14')

# Draw status text
status_text = "Score: 1240  |  Level: 3  |  Lines: 5"
text_color = '#2ecc71'
# Simple text rendering
draw.text((60, 465), status_text, fill=text_color)

# Save
image.save('/workspaces/XIAOJIE/docs/tetris-demo.png')
print("✅ Tetris demo image created: /workspaces/XIAOJIE/docs/tetris-demo.png")
