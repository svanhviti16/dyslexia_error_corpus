import difflib
import sys
from itertools import groupby 

error_types = { '1': 'addition-context-independent',
                '2': 'addition-context-dependent',
                '3': 'omission-context-independent',
                '4': 'omission-context-dependent',
                '5': 'substitution-context-independent',
                '6': 'substitution-context-dependent',
                '7': 'swapping-context-independent',
                '8': 'swapping-context-dependent',
                '9': 'other-context-independent',
                '10': 'other-context-dependent',
                '11': 'ypsilon-context-independent',
                '12': 'ypsilon-context-dependent',
                '13': 'missing-word',
                '14': 'extra-word',
                '15': 'phonetic-context-independent',
                '16': 'phonetic-context-dependent',
                '17': 'grammar-dative',
                '18': 'grammar-gender',
                '19': 'grammar-number',
                '20': 'grammar-case',
                '21': 'grammar-subjunctive',
                '22': 'grammar-new-syntax',
                '23': 'grammar-tense',
                '24': 'idiom',
                '25': 'syntax',
                '26': 'punctuation',
                '27': 'style',
                '28': 'spacing',
                '29': 'casing',
                '30': 'word-order',
                '31': 'other',
                '32': 'grammar-family',
                '33': 'preposition',
                '34': 'no-error',
                '35': 'grammar-ir' }

def open_file(filename):
    """ Returns a file stream if filename found, otherwise None """
    try:
        file_stream = open(filename, "r")
        return file_stream
    except FileNotFoundError:
        return None

def read_sentences(file_object):
    """ Reads the sentences as a list """
    tokens = []

    for line in file_object:
        
        # One sentence per line, added to a list
        token = line.strip()
        tokens.append(token)

    # using groupby to divide list into sublists on deliminator
    sentence_lists = [list(sub) for ele, sub in groupby(tokens, key = bool) if ele] 

    return sentence_lists


def get_error_type():
    
    error_value = input("Hvaða villuflokkur? ")
    # if one of the predetermined categories
    if error_value in error_types.keys():
        return error_types.get(error_value)
    # if new category
    else:
        return error_value
    

def find_differences(original_sentences, reviewed_sentences):

    for idx, sentence in enumerate(original_sentences):
        for key, value in error_types.items():
            print(f"{key}: {value}")
        #print(sentence)
        original = sentence
        print(" ".join(original))

        corrected = reviewed_sentences[idx]
        print(" ".join(corrected))


        d = difflib.Differ()
        diff = list(d.compare(original, corrected))
        result = []

        for word in diff:
            print(word)
            if word[0] == '-':
                error_type = get_error_type()                
                result.append(f'<err type="{error_type}">{word[2:].strip()}</err>')
            elif word[0] == '+':
                try:
                    if not result[-1].startswith('<err'):
                        error_type = get_error_type()                
                        result.append(f'<err type="{error_type}"></err>')        
                    result.append(f'<corr type="{error_type}">{word[2:].strip()}</corr>')
                except:
                    print("babb í bátinn")
            elif word[0] == '?':
                pass
            else:
                result.append(word.strip())
        tagged_sentence = ' '.join(result)
        tagged_sentence.replace("</err> <corr", "</err><corr")

        with open('output/corpus_output.xml', 'a') as the_file:
            the_file.write(tagged_sentence + '\n')
        
        print(tagged_sentence)

 
def main():


    original_text_filename = sys.argv[1]
    reviewed_text_filename = sys.argv[2]
 
    original_file_object = open_file(original_text_filename)
    reviewed_file_object = open_file(reviewed_text_filename)

    original_sentences = read_sentences(original_file_object)
    reviewed_sentences = read_sentences(reviewed_file_object)

    find_differences(original_sentences, reviewed_sentences)


if __name__ == '__main__':
  main()



