lines = []
line = input('First line: ')
while line:
    lines.append(line)
    line = input('Next line: ')
for line in lines:
    line = line.split("\t")
    print(line[1], line[2])
