import sys
triggers = ['</trkseg>', '</trk>', '<trk>', 'pass', '<trkseg>']

def condition_line(line, trigger):
    line = line.lstrip()
    bool = (line != '</gpx>'  and (trigger == 'pass' or line == trigger))
    return bool

def main():
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
    with open(input_filename, "r") as f:
        lines = f.read().split("\n")
    output = []
    offset = 0

    for i,line in enumerate(lines):
        if offset:
            offset -=1
        else:
            line = lines[i].lstrip()
            j = 0
            cond = True
            while j<5 and cond:
                cond = condition_line(lines[i+j], triggers[j])
                j+=1
            if cond:
                offset = 4
            if not cond:
                output.append(line)

    output = '\n'.join(output)
    with open(output_filename, 'w') as f:
        f.write(output)

if __name__ == '__main__':
    main()