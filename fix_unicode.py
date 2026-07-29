import re

with open(r'C:\Users\Administrator\WorkBuddy\2026-07-28-18-14-29\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

def replace_unicode(match):
    try:
        code = int(match.group(1), 16)
        # Handle surrogate pairs - encode as UTF-16 then decode as UTF-8
        try:
            return chr(code)
        except ValueError:
            # Surrogate characters - return as-is
            return match.group(0)
    except:
        return match.group(0)

# Replace literal \uXXXX with actual Unicode characters
content = re.sub(r'\\u([0-9a-fA-F]{4})', replace_unicode, content)

# Write with surrogateescape to handle any remaining issues
with open(r'C:\Users\Administrator\WorkBuddy\2026-07-28-18-14-29\index.html', 'w', encoding='utf-8', errors='surrogateescape') as f:
    f.write(content)

print('Done')
