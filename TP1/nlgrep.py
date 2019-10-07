import re
import sys

# get arguments through command line
flag = sys.argv[1]
pattern = sys.argv[2]
# if there are 4 args (script name included), read the file given as argument
if len(sys.argv) == 4:
    file = open(sys.argv[3], 'r').read()
# else get it from stdin
else:
    path = input()
    file = open(path, 'r').read()
# check if flag is sentence-level
if flag == '-s':
    # if a whitespace is preceded by .,!, ? or newline, it splits the file on the space.
    sentences = re.split(r"(?<=[.?!\n])\s(?=[A-Z])", file)
    # for each sentence, search the pattern. If there are any positive results, the sentence is printed to the ouput.
    for s in sentences:
        res = re.search(pattern, s)
        if res is not None:
            # remove \n's if there are any in the middle of the sentences
            print(s.replace('\n', ' '))
# check if flag is paragraph-level
elif flag == '-p':
    paragraphs = re.split(r"\n\n", file)
    # for each paragraph, search the pattern. If there are any positive results, the paragraph is printed to the ouput.
    for p in paragraphs:
        res = re.search(pattern, p)
        if res is not None:
            # remove \n's if there are any in the middle of the paragraphs
            print(p.replace('\n', ' '))
