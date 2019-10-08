import re
import sys


# check if a string contains a pattern or word
def string_found(pattern, sentence):
    # escape: Return string with all non-alphanumerics backslashed
    if re.search(pattern, sentence) is not None:
        return True
    else:
        return False


# general function that splits the input given the flag and gets the output
def nlgrep(flag, file, pattern):
    # check if flag is sentence-level
    if flag == '-s':
        # if a whitespace is preceded by .,!, ? or newline, it splits the file on the space.
        sentences = re.split(r"(?<=[.?!])\s|\n(?=[A-Z])", file)
        if len(sys.argv) == 3: print("------- Output: -------")
        # for each sentence, search the pattern. If there are any positive results, the sentence is printed to the ouput.
        for s in sentences:
            if (string_found(pattern, s)) is True:
                # remove \n's if there are any in the middle of the sentences
                print(s.replace('\n', ' '))
    # check if flag is paragraph-level
    elif flag == '-p':
        paragraphs = re.split(r"\n\n", file)
        if len(sys.argv) == 3: print("------- Output: -------")
        # for each paragraph, search the pattern. If there are any positive results, the paragraph is printed to the ouput.
        for p in paragraphs:
            if (string_found(pattern, p)) is True:
                # remove \n's if there are any in the middle of the paragraphs
                print(p.replace('\n', ' '))


# SCRIPT:
# get arguments through command line
flag = sys.argv[1]
pattern = sys.argv[2]
# if there are 3 args get input from stdin
if len(sys.argv) == 3:
    file = sys.stdin.readlines()
    file = ''.join(file)
    nlgrep(flag, file, pattern)
# if there are more than 3 args, read the files given as arguments
elif len(sys.argv) > 3:
    for i in range(3, len(sys.argv)):
        file = open(sys.argv[i], 'r').read()
        print("------- " + sys.argv[i] + " -------")
        nlgrep(flag, file, pattern)
