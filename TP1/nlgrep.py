import re
import sys

# check if a string contains a whole word
def string_found(pat, sen):
    # escape: Return string with all non-alphanumerics backslashed
    if re.search(r"\b" + re.escape(pat) + r"\b", sen):
        return True
    return False

def pattern_sentence(file):
    # if a whitespace is preceded by .,!, ? or newline, it splits the file on the space.
    sentences = re.split(r"(?<=[.?!\n])\s(?=[A-Z])", file)
    # for each sentence, search the pattern. If there are any positive results, the sentence is printed to the ouput.
    for s in sentences:
        if (string_found(pattern,s)) is True:
            # remove \n's if there are any in the middle of the sentences
            print(s.replace('\n', ' '))

def pattern_paragraph(file):
    paragraphs = re.split(r"\n\n", file)
    # for each paragraph, search the pattern. If there are any positive results, the paragraph is printed to the ouput.
    for p in paragraphs:
        if (string_found(pattern,p)) is True:
            # remove \n's if there are any in the middle of the paragraphs
            print(p.replace('\n', ' '))

# get arguments through command line
flag = sys.argv[1]
pattern = sys.argv[2]
# if there are 4 args (script name included), read the file given as argument
if len(sys.argv) == 3:
    file = sys.stdin.readlines()
    file = ''.join(file)
# else get it from stdin
else:
    files = []
    for i in range(3, len(sys.argv)):
        files.append(sys.argv[i])

# check if flag is sentence-level
if flag == '-s':
    for x in files:
        file = open(x, 'r').read()
        pattern_sentence(file)

# check if flag is paragraph-level
elif flag == '-p':
    for x in files:
        file = open(x, 'r').read()
        pattern_paragraph(file)
