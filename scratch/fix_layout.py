import re

with open('app/app.py', 'r') as f:
    content = f.read()

# 1. Change layout back to centered
content = content.replace('layout="wide"', 'layout="centered"')

# 2. Add header contrast so the hamburger/expand arrow is visible
if '[data-testid="stHeader"] {' in content:
    content = content.replace(
        '[data-testid="stHeader"] {\n    background: rgba(0,0,0,0) !important;\n}',
        '[data-testid="stHeader"] {\n    background: rgba(0,0,0,0) !important;\n}\n[data-testid="stHeader"] * {\n    color: #1a2a3a !important;\n}'
    )

# 3. Instead of spacer columns, just write directly if we are centered to avoid squeezing
content = content.replace('col_spacer1, col_main, col_spacer2 = st.columns([1, 8, 1])\n\nwith col_main:', 'if True:')

with open('app/app.py', 'w') as f:
    f.write(content)

print("Layout fixes applied.")
