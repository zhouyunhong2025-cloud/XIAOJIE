#!/usr/bin/env python3
from PIL import Image, ImageDraw

# Create image with light background
width, height = 1200, 700
image = Image.new('RGB', (width, height), color='#f8f9fa')
draw = ImageDraw.Draw(image)

# Define colors (inspired by user's Cartridge design)
colors = {
    'light_blue': '#b3d9ff',
    'dark_blue': '#5ba3ff',
    'light_purple': '#e6b3ff',
    'dark_purple': '#cc66ff',
    'light_green': '#b3ffcc',
    'dark_green': '#66ff99',
    'light_orange': '#ffe6b3',
    'dark_orange': '#ffcc66',
    'light_red': '#ffb3b3',
    'dark_red': '#ff6666',
    'light_yellow': '#ffff99',
    'dark_yellow': '#ffdd00',
    'dark_text': '#333333',
    'light_text': '#999999',
}

# ===== LEFT: I Tetromino (vertical long block) =====
logo_x, logo_y = 120, 180
block_size = 70

# I block (4 blocks vertically)
draw.rectangle([logo_x, logo_y, logo_x + block_size, logo_y + block_size],
              fill=colors['light_blue'], outline=colors['dark_text'], width=2)
draw.rectangle([logo_x, logo_y + block_size, logo_x + block_size, logo_y + 2*block_size],
              fill=colors['light_purple'], outline=colors['dark_text'], width=2)
draw.rectangle([logo_x, logo_y + 2*block_size, logo_x + block_size, logo_y + 3*block_size],
              fill=colors['light_green'], outline=colors['dark_text'], width=2)
draw.rectangle([logo_x, logo_y + 3*block_size, logo_x + block_size, logo_y + 4*block_size],
              fill=colors['light_orange'], outline=colors['dark_text'], width=2)

# QUEUE blocks (2x2 square)
queue_x = logo_x + 110
queue_y = logo_y + 35

# Top-left
draw.rectangle([queue_x, queue_y, queue_x + block_size, queue_y + block_size],
              fill=colors['light_red'], outline=colors['dark_text'], width=2)
# Top-right
draw.rectangle([queue_x + block_size + 5, queue_y, queue_x + 2*block_size + 5, queue_y + block_size],
              fill=colors['light_yellow'], outline=colors['dark_text'], width=2)
# Bottom-left
draw.rectangle([queue_x, queue_y + block_size + 5, queue_x + block_size, queue_y + 2*block_size + 5],
              fill=colors['light_green'], outline=colors['dark_text'], width=2)
# Bottom-right
draw.rectangle([queue_x + block_size + 5, queue_y + block_size + 5, queue_x + 2*block_size + 5, queue_y + 2*block_size + 5],
              fill=colors['light_purple'], outline=colors['dark_text'], width=2)

# ===== CENTER: Brand name and tagline =====
brand_x = 450
brand_y = 200

# Draw "I.QUEUE" text
draw.text((brand_x, brand_y), "I.QUEUE", fill=colors['dark_text'], 
         font=None)

# Key concepts with colored blocks
# Intelligence
draw.rectangle([brand_x, brand_y + 120, brand_x + 30, brand_y + 150],
              fill=colors['light_blue'], outline=colors['dark_text'], width=1)
draw.text((brand_x + 45, brand_y + 125), "Intelligence", fill=colors['dark_text'])

# Order
draw.rectangle([brand_x, brand_y + 170, brand_x + 30, brand_y + 200],
              fill=colors['light_purple'], outline=colors['dark_text'], width=1)
draw.text((brand_x + 45, brand_y + 175), "Order", fill=colors['dark_text'])

# Tagline
draw.text((brand_x, brand_y + 280), "A gift for you and your AI agent",
         fill=colors['light_text'])

# ===== RIGHT: Core features =====
features_x = 950
features_y = 200
feature_block_size = 35
line_height = 100

# Feature 1: Memory Rod
draw.rectangle([features_x, features_y, features_x + feature_block_size, features_y + feature_block_size],
              fill=colors['light_blue'], outline=colors['dark_text'], width=1)
draw.text((features_x + 50, features_y + 8), "Memory Rod", fill=colors['dark_text'])

# Feature 2: Skill Block
draw.rectangle([features_x, features_y + line_height, features_x + feature_block_size, features_y + line_height + feature_block_size],
              fill=colors['light_purple'], outline=colors['dark_text'], width=1)
draw.text((features_x + 50, features_y + line_height + 8), "Skill Block", fill=colors['dark_text'])

# Feature 3: Alignment
draw.rectangle([features_x, features_y + 2*line_height, features_x + feature_block_size, features_y + 2*line_height + feature_block_size],
              fill=colors['light_green'], outline=colors['dark_text'], width=1)
draw.text((features_x + 50, features_y + 2*line_height + 8), "Alignment", fill=colors['dark_text'])

# Feature 4: Pipeline
draw.rectangle([features_x, features_y + 3*line_height, features_x + feature_block_size, features_y + 3*line_height + feature_block_size],
              fill=colors['light_orange'], outline=colors['dark_text'], width=1)
draw.text((features_x + 50, features_y + 3*line_height + 8), "Pipeline", fill=colors['dark_text'])

# ===== DIVIDER LINES =====
draw.line([(400, 150), (400, 650)], fill=colors['light_text'], width=1)
draw.line([(900, 150), (900, 650)], fill=colors['light_text'], width=1)

# Save
image.save('/workspaces/XIAOJIE/docs/i-queue-logo.png')
print("✅ I.QUEUE Logo image created (all English)")
