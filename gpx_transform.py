import sys
# triggers = ['</trkseg>', '</trk>', '<trk>', 'pass', '<trkseg>']
triggers = ['</trk>', '<trk>', 'pass']

def condition_line(line, trigger):
    line = line.lstrip()
    bool = (line != '</gpx>'  and (trigger == 'pass' or line == trigger))
    return bool

def get_image_directory_and_name(path):
    last_slash_index = 0
    last_dot_index = 0
    n = len(path)
    for i in range(n):
        if path[i]=='/':
            last_slash_index = i
    for i in range(last_slash_index,n):
        if path[i]=='.':
            last_dot_index = i
    if last_dot_index==0:
        return path[:last_slash_index],path
    else :
        return path[:last_slash_index],path[last_slash_index+1:last_dot_index]

def file_transform(file): #adds \n between all <smthg>, apply .split('\n'), removes empty lines, replaces name attributes on one line
    oneline = ''
    for char in file:
        if char == '<':
            oneline += '\n'+char
        elif  char == '>':
            oneline += char+'\n'
        else:
            oneline += char
    lines = [line for line in oneline.split('\n') if line != '']
    lines_with_name_fixed = []
    n = len(lines)
    i = 0
    while i<n:
        line = lines[i]
        if line == '<name>':
            for k in range(2):
                i += 1
                line += lines[i]
        lines_with_name_fixed.append(line)
        i += 1
    lines_with_coos_fixed = []
    n = len(lines_with_name_fixed)
    i = 0
    while i<n:
        line = lines_with_name_fixed[i]
        if line[:7] == '<trkpt ':
            for k in range(3):
                i += 1
                line += lines_with_name_fixed[i]
        lines_with_coos_fixed.append(line)
        i += 1
    return lines_with_coos_fixed

def remove_seg(lines, new_filename):
    name_has_changed = False
    output = []
    offset = 0
    for i,line in enumerate(lines):
        if not name_has_changed:
            if line.lstrip()[:6] == '<name>':
                output.append('<name>'+new_filename+'</name>')
                name_has_changed = True
            else:
                output.append(line)
        else:
            if offset:
                offset -=1
            else:
                line = lines[i].lstrip()
                j = 0
                cond = True
                while j<len(triggers) and cond:
                    cond = condition_line(lines[i+j], triggers[j])
                    j+=1
                if cond:
                    offset = len(triggers)-1
                if not cond:
                    output.append(line)
    return '\n'.join(output)

def main():
    input_filename = sys.argv[1]
    new_filename = sys.argv[2]
    dir,name = get_image_directory_and_name(input_filename)
    output_filename = dir+'/output-'+name+'.gpx'

    with open(input_filename, "r") as f:
        lines = f.read()
    lines = file_transform(lines) 
    output = remove_seg(lines, new_filename)
    with open(output_filename, 'w') as f:
        f.write(output)

if __name__ == '__main__':
    main()