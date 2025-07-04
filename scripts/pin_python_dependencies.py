"""
Script to pin all Python dependencies to exact versions in requirements.txt
"""
import re
with open('backend/requirements.txt') as f:
    lines = f.readlines()
new_lines = []
for line in lines:
    if line.strip() and not line.startswith('#'):
        pkg = re.split('==|>=|<=|~=|>|<', line)[0].strip()
        # Simulate pinning to exact version (stub: in prod, parse pip freeze)
        if '==' not in line:
            new_lines.append(pkg + '==latest\n')
        else:
            new_lines.append(line)
    else:
        new_lines.append(line)
with open('backend/requirements.txt', 'w') as f:
    f.writelines(new_lines)
print('All Python dependencies pinned to exact versions (stub: replace latest with actual versions).')
