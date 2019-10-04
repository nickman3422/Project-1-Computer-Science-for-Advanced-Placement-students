"""""
Nick Mangerian
Letter Frequency: computes,displays, and plots the frequencies of the letters of the data
"""""
from word_count import*
from hashmap import *
import argparse
import matplotlib.pyplot as plt

def read_commands():
    """
    precondition:commands must be valid arguments with correct number of arguments
    postcondition: returns the filename and desired word
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", help="display the top ranked words",action="store_true")
    parser.add_argument("-p", "--plot", help="plot the data of the word freqency",action="store_true")
    parser.add_argument("filename", help="Name of file that is is being used")
    return parser.parse_args()

def letter_frequency(theTable):
    """
    precondition: given table must be valid hashmap
    postcondition: returns a hashmap of the letters and their frequencies
    """
    letter_Table=HashMap(10)
    total_words=0
    for i in range(26):
       put(letter_Table,chr(i+97),0)
    for word in keys(theTable):
       word_num=count_words(theTable, word)
       word=list(word)
       for letter in word:
           # make a variable of the nubmer of total letters
           total_words = total_words+word_num
           if contains( letter_Table, letter ):
               prev=get(letter_Table, letter)
               put(letter_Table, letter, (int)(word_num)+(int)(prev))
           else:
               put(letter_Table, letter, word_num)
    for letters in keys(letter_Table):
       count=get(letter_Table, letters)
       # put the freqency of the letter at postion of the letter in table
       put(letter_Table, letters, ((int)(count)/(int)(total_words)))
    return letter_Table

def output(table):
    """
    precondition:given table must be valid hashmap
    poscondition:prints the letters and their frequencies
    """
    sorted_letters,sorted_freq=sort(table)
    #for each letter, print its frequencies
    for i in range(26):
        print(sorted_letters[i],":",sorted_freq[i])
def plot(table,filename):
    """
    precondition:given table must be valid hashmap
    poscondition:plot the letters and their frequencies
    """
    sorted_letters,sorted_freq = sort(table)
    plt.ylabel('Frequency')
    plt.xlabel("Letters")
    plt.title('Letter Frequencies: '+str(filename))
    plt.bar(sorted_letters,sorted_freq, align="center")
    plt.show()
def sort(table):
    """
    precondition: given table must be valid hashmap
    poscondition:sorts the hashmap into two lists and returns lists
    """
    sorted_letters = list(keys(table))
    sorted_letters.sort()
    sorted_freq=[]
    for i in range(len(sorted_letters)):
        sorted_freq.append(get(table,sorted_letters[i]))
    return sorted_letters,sorted_freq
def main( ):
    """
    precondition: the needed methods are provided
    poscondition:the file preforms correctly
    """
    args=read_commands()
    filename = args.filename
    filename_error(filename)
    wordTable = read_file(filename)
    table=letter_frequency(wordTable)
    # print the output and plot the data if either or both desired
    if (args.output == True):
        output(table)
    if (args.plot == True):
        plot(table,filename)
if __name__ == "__main__":
   main( )


