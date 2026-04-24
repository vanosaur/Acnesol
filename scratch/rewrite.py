import re
with open('app/app.py', 'r') as f:
    content = f.read()

# 1. Change layout configuration
content = content.replace('layout="centered"', 'layout="wide", initial_sidebar_state="expanded"')

# 2. Extract sections to put in sidebar
sidebar_start = content.find('# ================================================================\n#            SECTION 1: IMAGE UPLOAD')
analyze_end = content.find('# ================================================================\n#            AGENT PIPELINE EXECUTION')

sections_text = content[sidebar_start:analyze_end]

# Modify the sections_text to be under `with st.sidebar:`
sidebar_code = """# ================================================================
#            SIDEBAR INPUTS
# ================================================================
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>Configure Analysis</h2>", unsafe_allow_html=True)
"""
# Indent the old sections
for line in sections_text.split('\\n'):
    if line.strip():
        sidebar_code += "    " + line + '\\n'
    else:
        sidebar_code += '\\n'

# 3. Create TABS layout around results and chat
results_start = content.find('# ================================================================\n#            RESULTS DISPLAY')

# Extract everything from results to the end (before footer)
footer_start = content.find('# ================================================================\n#                        FOOTER')

results_chat_text = content[results_start:footer_start]

tabs_code = """# ================================================================
#            DASHBOARD TABS
# ================================================================
if st.session_state.last_analysis is not None:
    tab1, tab2, tab3 = st.tabs(["📊 Overview", "🧴 Routines & Products", "💬 Ask AI Coach"])
    
    with tab1:
        # We will render the combined result and cards here
"""

# We can selectively pipe things into tabs.
# Or simpler: rewrite the file directly. I'll just rewrite app.py entirely.
