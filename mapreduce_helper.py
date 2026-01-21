# mapreduce_helper.py

def mapper(text_line):
    """Breaks a line of text into (word, 1) pairs."""
    words = text_line.strip().lower().split()
    return [(word, 1) for word in words]

def reducer(word, counts):
    """Adds up all the 1s for a specific word."""
    return (word, sum(counts))