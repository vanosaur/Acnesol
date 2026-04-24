with open('app/app.py', 'r') as f:
    content = f.read()

injection = """/* SIDEBAR STYLING */
[data-testid="stSidebar"] {
    background-color: rgba(255,255,255,0.45) !important;
    backdrop-filter: blur(18px) !important;
    -webkit-backdrop-filter: blur(18px) !important;
    border-right: 1px solid rgba(146,191,232,0.3) !important;
}"""

content = content.replace("/* ========== ANIMATION KEYFRAMES ========== */", injection + "\n\n/* ========== ANIMATION KEYFRAMES ========== */")

with open('app/app.py', 'w') as f:
    f.write(content)

print("Sidebar CSS added")
