from Bio import pairwise2
import sys
import difflib
import tokenizer # Reynir tokenizer for Icelandic

"""
    Script for tokenizing a small error corpus. Reads a text file and returns a tokenized version. 

    Arguments:
    1. Original or reviewed text file. One sentence per line.

"""

def open_file(filename):
    ''' Returns a file stream if filename found, otherwise None '''
    try:
        file_stream = open(filename, "r")
        return file_stream
    except FileNotFoundError:
        return None

def read_sentences(file_object):
    ''' Reads the sentences as a list '''
    sentences = []
    for line in file_object:
        # One sentence per line, added to a list
        sentence = line.strip()
        sentences.append(sentence)
    return sentences

def get_tokens(sentences):

    for sentence in sentences:
        for token in tokenizer.tokenize(sentence):
            kind, txt, val = token
            #if kind == tokenizer.TOK.WORD:
            if txt: # everything that is not None
                print(txt)
            elif kind == tokenizer.TOK.S_END:
                print("") # adds a single newline at the end of sentences
            elif kind == tokenizer.TOK.S_BEGIN:
                pass # ignoring starts of sentences

                

def main():

    corpus_filename = sys.argv[1]
    #reviewed_text_filename = sys.argv[2]
 
    file_object = open_file(corpus_filename)

    sentences = read_sentences(file_object)

    get_tokens(sentences)

    
if __name__ == '__main__':
  main()

