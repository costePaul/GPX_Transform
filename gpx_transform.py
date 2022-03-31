import sys
triggers = ['</trkseg>', '</trk>', '<trk>', 'pass', '<trkseg>']

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

def main():
    input_filename = sys.argv[1]
    new_filename = sys.argv[2]
    dir,name = get_image_directory_and_name(input_filename)
    result_path = dir+'/output-'+name+'.gpx'
    output_filename = result_path

    name_has_changed = False

    with open(input_filename, "r") as f:
        lines = f.read().split("\n")
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