
"""""
Nick Mangerian
word Frequency: computes,displays, and plots the frequencies of the words of the data
"""""
from word_count import*
from hashmap import *
import argparse
import matplotlib.pyplot as plt
from matplotlib.text import TextPath

def read_commands():
    """
    precondition:commands must be valid with correct number of arguments
    postcondition: returns the filename and desired word
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", help="display the top ranked words",action="store_true")
    parser.add_argument("-p", "--plot", help="plot the data of the word count",action="store_true")
    parser.add_argument("word", help="Name of word that the data is requested of")
    parser.add_argument("filename", help="Name of file that is is being used")
    return parser.parse_args()
def word_frequency(theTable):
    """
    precondition:given table must be valid hashmap
    poscondition: returns table of words with their freqenices
    """
    for word in keys(theTable):
        word_num = count_words(theTable, word)
        put(theTable, word,word_num)
    return theTable


def output(table,word):
    """
    precondition: table and word msut be valid
    poscondition: displays the top ranked words and their frequencies
    """
    sorted_word, sorted_count = sort(table)
    print(word,"is ranked", "#"+str(sorted_word.index(word)+1))
    count= 1
    if len(sorted_word)<20:
        num=len(sorted_word)
    else:
        num=20
    for i in range(num):
       print("#"+str(count),":",sorted_word[i],"->",sorted_count[i])
       count=count+1
def plot(table,word, filename):
    """
    precondition: the table and word must be valid
    poscondition: plots the words and their frequencies
    """
    sorted_word, sorted_count = sort(table)
    plt.ylabel('Frequency')
    plt.xlabel("Rank of Word"+" ("+str(word)+" is"+" rank "+str(sorted_word.index(word)+1)+")")
    plt.title('Word Frequencies: '+str(filename))
    plt.loglog(sorted_word, sorted_count)
    plt.xscale('symlog')
    label=TextPath((-20,10),str(word),linewidth=50)
    plt.plot(word, get(table,word), marker=label, markersize=40, color="red")
    plt.plot(word, get(table, word), marker='*', markersize=10, color="red")
    plt.show()

def sort(table):
    """
    precondition:given table must be valid hashmap
    postcondition: sorts and returns the table into two lists
    """
    sorted_words=[]
    sorted_count=[]
    word_data=namedtuple("word_data",("word","word_count"))
    words=[]
    for word in keys(table):
        words.append(word_data(word, get(table,word)))
    sorted=quick_sort(words)
    sorted=sorted[::-1]
    for i in range(len(sorted)):
        sorted_words.append(sorted[i].word)
        sorted_count.append(int(sorted[i].word_count))
    return sorted_words,sorted_count
def quick_sort(data):
    """
    precondition:given table must be valid hashmap
    postcondition: returns the sored list of the data
    """
    if len(data) == 0:
        return []
    else:
        pivot = 0
        less, equal, greater = partition(data, pivot)
        return quick_sort(less) + equal + quick_sort(greater)

def partition(data, pivot: int) :
    """
    precondition:given data must be valid
    poscondition: partitions the list into less, eqaul, or greater
    """
    less, equal, greater = [], [], []
    for element in data:
        if element.word_count < data[pivot].word_count:
            less.append(element)
        elif element.word_count > data[pivot].word_count :
            greater.append(element)
        else:
            equal.append(element)
    return less, equal, greater
def main( ):
    """
    precondition: the needed methods are provided
    poscondition:the file preforms correctly
    """
    args=read_commands()
    filename = args.filename
    filename_error(filename)
    word=args.word
    wordTable = read_file( filename)
    word_error(word,wordTable)
    letter_table=word_frequency(wordTable)
    sort(letter_table)
    # print the output and plot the data if either or both desired
    if(args.output==True):
        output(letter_table,word)
    if(args.plot==True):
        plot(wordTable,word,filename)

if __name__ == "__main__":
   main( )


