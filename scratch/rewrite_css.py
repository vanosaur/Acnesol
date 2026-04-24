import re

with open('app/app.py', 'r') as f:
    content = f.read()

replacements = [
    (r'rgba\(212,\s*165,\s*154,', r'rgba(146, 191, 232,'), # The main tint
    (r'rgba\(212,165,154,', r'rgba(146,191,232,'), # Underspaced
    (r'rgba\(180,140,120,', r'rgba(140,160,180,'), # Box shadows
    (r'#d4a59a', r'#92bfe8'), # Primary accent (peach to icy blue)
    (r'#c89b90', r'#74a4cf'), # Secondary accent button gradient
    (r'#c4b5d0', r'#b5c4d0'), # Icon gradient
    (r'#b08a7a', r'#7a9eb0'), # Highlight text
    (r'#c4a89e', r'#a8bbcc'), # Muted text
    (r'#3d3530', r'#1a2a3a'), # Headers
    (r'#5a4a44', r'#3a4a5a'), # Body text
    (r'#8a7a74', r'#607d8b'), # Muted subtext
    (r'badge-mild \{ background: rgba\(134,188,120,0.18\); color: #5a9a4e; border: 1px solid rgba\(134,188,120,0.35\); \}',
     r'badge-mild { background: rgba(146,191,232,0.18); color: #4a8abb; border: 1px solid rgba(146,191,232,0.35); }'),
    (r'badge-moderate \{ background: rgba\(230,180,80,0.18\); color: #b8912e; border: 1px solid rgba\(230,180,80,0.35\); \}',
     r'badge-moderate { background: rgba(170,180,210,0.18); color: #6e7da1; border: 1px solid rgba(170,180,210,0.35); }'),
    (r'badge-severe \{ background: rgba\(210,110,100,0.18\); color: #b85a50; border: 1px solid rgba\(210,110,100,0.35\); \}',
     r'badge-severe { background: rgba(220,130,140,0.18); color: #c46473; border: 1px solid rgba(220,130,140,0.35); }'),
    (r'background:rgba\(255,200,140,0.3\)', r'background:rgba(180,210,240,0.3)'), # Routine icon backgrounds
    (r'style="color:#b08a7a;"', r'style="color:#7a9eb0;"'),
    (r'color:#888', r'color:#8a9ba8')
]

for old, new in replacements:
    content = re.sub(old, new, content)

with open('app/app.py', 'w') as f:
    f.write(content)

print("CSS Theme replaced successfully.")
