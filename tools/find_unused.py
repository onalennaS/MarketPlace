import os
import re
from pathlib import Path

root = Path(__file__).resolve().parent.parent
ignore_dirs = {'.git', '__pycache__', 'migrations', 'venv', '.venv', 'env', '.env'}
py_files = []
for p in root.rglob('*.py'):
    # skip hidden/git dirs or virtualenvs
    if any(part in ignore_dirs for part in p.parts):
        continue
    py_files.append(p)

modules = {}
for p in py_files:
    rel = p.relative_to(root)
    mod = '.'.join(rel.with_suffix('').parts)
    modules[mod] = p

# Read contents once
contents = {str(p): p.read_text(encoding='utf-8', errors='ignore') for p in py_files}

results = []
for mod, path in modules.items():
    src = contents[str(path)]
    # build search tokens: full module, module root, filename
    tokens = [mod]
    root_mod = mod.split('.')[0]
    if root_mod != mod:
        tokens.append(root_mod)
    filename = Path(mod).name
    tokens.append(filename)

    found = False
    occurrences = 0
    for other_path, other_src in contents.items():
        if other_path == str(path):
            continue
        for t in tokens:
            # search for import patterns or attribute access
            if re.search(rf"\b(import|from)\s+{re.escape(t)}\b", other_src):
                found = True
                occurrences += len(re.findall(rf"\b(import|from)\s+{re.escape(t)}\b", other_src))
            # also search dotted references like user.views or .views used in templates etc
            if re.search(re.escape(t) + r"\.", other_src):
                found = True
    if not found:
        # heuristic: if module is within a Django app and its filename is standard, lower confidence
        in_app = len(mod.split('.')) >= 2
        fname = Path(path).name
        standard_names = {'models.py','views.py','admin.py','apps.py','urls.py','tests.py','migrations'}
        is_standard = fname in standard_names
        confidence = 'medium'
        if not in_app and not is_standard:
            confidence = 'high'
        elif not found and in_app and not is_standard:
            confidence = 'low'
        results.append({
            'module': mod,
            'path': str(path.relative_to(root)),
            'confidence': confidence,
        })

# Also report top-level non-python candidates
extras = ['data.json','data1.json','.credentials1.json','db.sqlite3.url','script.py','ww','staticfiles']
extras_report = []
for e in extras:
    p = root / e
    if p.exists():
        # search references
        ref_found = False
        for other_path, s in contents.items():
            # ignore this analysis script itself when checking
            if other_path.endswith('tools{}find_unused.py'.format(os.sep)):
                continue
            if e in s:
                ref_found = True
                break
        extras_report.append({'name': e, 'exists': True, 'referenced': ref_found})

print('\n=== Likely-unused Python modules (heuristic) ===')
for r in results:
    print(f"{r['module']:60} {r['path']:40} confidence={r['confidence']}")
print('\n=== Extras report ===')
for e in extras_report:
    print(f"{e['name']:20} referenced={e['referenced']}")

print('\nSummary: modules listed above had no import-like references elsewhere (heuristic).')
print('Files in Django apps with standard names (models/views/admin) were given lower confidence and may still be used by Django.')
