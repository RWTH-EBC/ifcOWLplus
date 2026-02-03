import re
from pathlib import Path

def extract_block(text, block_name):
    pattern = rf"{block_name}\s*\{{(.*?)\}}"
    match = re.search(pattern, text, re.S)
    return match.group(1).strip() if match else ""

text1 = Path("builtin_owl2-rl-optimized.pie").read_text(encoding="utf-8")
text2 = Path("ifcPlus.pie").read_text(encoding="utf-8")

prefices = extract_block(text1, "Prefices") + "\n" + extract_block(text2, "Prefices")
axioms   = extract_block(text1, "Axioms")   + "\n" + extract_block(text2, "Axioms")
rules    = extract_block(text1, "Rules")    + "\n" + extract_block(text2, "Rules")

combined = f"""Prefices
{{
{prefices}
}}

Axioms
{{
{axioms}
}}

Rules
{{
{rules}
}}
"""

Path("ifcPlus_and_owl2-rl-optimized.pie").write_text(combined, encoding="utf-8")
print("Merged rulesets into combined.pie")