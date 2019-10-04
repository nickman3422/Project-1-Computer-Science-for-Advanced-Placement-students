"""""
Nick Mangerian
word length: computes the average length of all words for each year within range and plots data
"""""
from letter_freq import*
from hashmap import *
import argparse
import matplotlib.pyplot as plt


def read_commands():
    """
    precondition:commands must be valid with correct number of arguments
    postcondition: returns the filename and desired word
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", help="display the top ranked words",action="store_true")
    parser.add_argument("-p", "--plot", help="plot the data of the word count",action="store_true")
    parser.add_argument("start", help="start of the range of years")
    parser.add_argument("end", help="end of the range of years")
    parser.add_argument("filename", help="Name of file that is is being used")
    return parser.parse_args()

def word_length(theTable,start,end):
    """
    precondition:given table must be valid hashmap
    poscondition: returns a table of years and their average word length
    """
    year_data=namedtuple("year_data",("letter_count","word_count"))
    year_Table=HashMap(10)
    for word in keys(theTable):
        for years in keys(get(theTable,word)):
            if (years >= start and years <=end):
                count_word=(int)(get(get(theTable, word), years))
                if contains( year_Table, years ):
                   prev=get(year_Table, years)
                   prev_letter_count=int(prev.letter_count)
                   total_letters=(int(count_word)*int(len(word)))+prev_letter_count
                   total_words=count_word + prev.word_count
                   put(year_Table, years,year_data(total_letters,total_words))
                else:
                   put(year_Table, years, year_data((int(count_word)*int(len(word))),count_word))
    for year in keys(year_Table):
        data=get(year_Table,year)
        letter_count=(data.letter_count)
        word_count = (data.word_count)
        avg_length= (letter_count) / (word_count)
        # put the avgerage legnth at the postion of year in the table
        put(year_Table, year,  avg_length )
    return year_Table

def output(table):
    """
    precondition:given table must be valid hashmap
    postcondition: prints the letters and their frequencies
    """
    letters = list(keys(table))
    letters.sort()
    for i in range(len(letters)):
       print(letters[i],":",get(table,letters[i]))
def plot(table,filename,start,end):
    """
    precondition:given table must be valid hashmap
    poscondition:plots the data of the program
    """
    fig, ax = plt.subplots()
    sorted_years, sorted_length = sort(table)
    plt.ylabel('Average Word Length')
    plt.xlabel("Year")
    plt.title("Average word lengths from " + str(start)+" to "+str(end)+": "+filename)
    plt.plot(sorted_years, sorted_length)
    every_nth = int(len(sorted_years)/5)
    if every_nth <=0:
        every_nth=1
    for n, label in enumerate(ax.xaxis.get_ticklabels()):
        if n % every_nth != 0:
            label.set_visible(False)
    plt.show()

def main( ):
    """
    precondition: the needed methods are provided
    poscondition:the file preforms correctly
    """
    args=read_commands()
    filename = args.filename
    filename_error(filename)
    start=args.start
    end=args.end
    #if the start year is greater than end year end the program
    #if the start is greater than end, end the program
    if(start>end):
        sys.stderr.write("Error: start year must be less than or equal to end year!")
        sys.exit()
    wordTable = read_file(filename)
    year_Table=word_length(wordTable,start,end)
    # print the output and plot the data if either or both desired
    if (args.output == True):
       output(year_Table)
    if (args.plot == True):
       plot(year_Table, filename,start,end)

if __name__ == "__main__":
   main( )


