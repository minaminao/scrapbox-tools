# WIP

with open("scrapbox.txt") as f:
    lines = f.readlines()

indent = []

def convert(s):
    new_s = ""
    backquote = False
    link = False
    bracket_i = -1
    
    for c in s:
        nc = None
        if c == "`":
            backquote = not backquote
            nc = c
        else:
            if not backquote:
                if c == "<" and bracket_i == -1:
                    nc = "&lt;"
                elif c == ">" and bracket_i == -1:
                    nc = "&gt;"
                elif c == "[" and bracket_i == -1:
                    nc = ""
                    bracket_i = 0
                elif c in "$" and bracket_i == 1: # [012..n]
                    nc = ""
                elif c == " " and bracket_i == 2 and not link:
                    nc = ""
                elif bracket_i == 0:
                    link = True
                    nc = c
                elif c == "]" and bracket_i != -1:
                    bracket_i = -1
                    link = False
                    nc = ""
                else:
                    nc = c
                if bracket_i != -1:
                    bracket_i += 1
            else:
                nc = c

        assert nc is not None
        new_s += nc
        
    return new_s

for line in lines:
    line_indent = 0
    for i in range(len(line)):
        if line[i] in [" ", "\t"]:
            line_indent += 1
        else:
            break
    indent.append(line_indent)

code_block = False
code_block_indent = 0
new_lines = []
for line_i, line in enumerate(lines):
    new_line = ""

    if line_i == 0:
        new_line = "# " + convert(line)
    else:
        if code_block:
            if indent[line_i] == 0:
                new_lines.append("```\n")
                code_block = False
            else:
                new_line = line[code_block_indent:]
                new_lines.append(new_line)
                continue

        if line.startswith(">"):
            if line[1] != " ":
                new_line = "> " + convert(line[1:-1]) + "  \n"
            else:
                new_line = convert(line)
        elif line.startswith("code:"):
            code_block = True
            code_block_indent = indent[line_i + 1]
            if line == "code:txt\n":
                new_line = "```\n"
            else:
                new_line = line.replace("code:", "```")
        else:
            new_line = convert(line)

    new_lines.append(new_line)
    

with open("result.md", "w") as f:
    f.writelines(new_lines)
        
    