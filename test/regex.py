import re

s = "Test {{id}} dfdfd"
x = re.sub(pattern="{{\s*([a-zA-Z0-9_]+)\s*}}",repl="*",string=s)
print(x)