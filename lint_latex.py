import re
from pathlib import Path

lectures_dir = Path('docs/lectures')
issues_found = 0

for f in lectures_dir.glob('*_blueprint.md'):
    text = f.read_text(encoding='utf-8')
    
    # 1. Check for odd number of '$' (unmatched math delimiters)
    dollar_count = text.count('$')
    if dollar_count % 2 != 0:
        print(f'[Warning] Unmatched $ delimiters in: {f.name} (Count: {dollar_count})')
        issues_found += 1
        
    # 2. Check for suspicious concatenated control sequences
    suspicious_macros = re.findall(r'\\([a-zA-Z]+(?:ij|ik|jk|uv|xy|t|n|b))\b', text)
    valid_tex = {'max', 'min', 'sin', 'int', 'equiv', 'text', 'ln', 'tan', 'begin', 'end', 'in', 'notin'}
    bad_macros = [m for m in suspicious_macros if m not in valid_tex]
    
    if bad_macros:
        print(f'[Warning] Suspicious TeX macros {set(bad_macros)} found in: {f.name}')
        issues_found += 1

if issues_found == 0:
    print('✅ All 48 blueprints passed the LaTeX sanity check!')
else:
    print(f'❌ Found {issues_found} potential rendering issues. Please review the files above.')
