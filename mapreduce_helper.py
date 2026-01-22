# mapreduce_helper.py

def mapper(text_line):
    """
    This function is the MAP phase.
    It takes one line of text and breaks it into words.
    For each word, it returns (word, 1).
    """
    words = text_line.strip().lower().split()
    return [(word, 1) for word in words]

def reducer(word, counts):
    """
    This function is the REDUCE phase.
    It takes a word and a list of numbers (counts).
    It adds all the numbers together.
    """
    return (word, sum(counts))
