import re

# get arguments through command line
def nlgrep(flag, file):
    # get regex from stdin
    pattern = input("Search for words or regular expression:\n")
    if flag == '-s':
        # if a whitespace is preceded by .,! or ?, it splits the file on the space.
        sentences = re.split(r"(?<=[.?!])\s", file)
        # debug print: see the sentences gotten after splitting
        print(sentences)
        # for each sentence, search the pattern. If there are any positive results, the sentence is printed to the ouput.
        for s in sentences:
            res = re.search(pattern, s)
            if res is not None:
                print(s)
    elif flag == '-p':
        # paragraph: \n or \n\n ?
        paragraphs = re.split(r"\n", file)
        # debug print: see the paragraphs gotter after splitting
        print(paragraphs)
        # for each paragraph, search the pattern. If there are any positive results, the paragraph is printed to the ouput.
        for p in paragraphs:
            res = re.search(pattern, p)
            if res is not None:
                print(p)
