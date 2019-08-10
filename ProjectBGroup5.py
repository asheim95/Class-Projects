# ProjectBGroup5.py
# This program is to read in lottery data (pandas) and display the frequencies of the winning numbers (matplotlib)
# Andrew Heim, Benjamin Terry, Matthew Richesin, Will Chollman
# 29-July-2019


import pandas
import matplotlib.pyplot as plt
import operator

#aheim & bterry7
# Finds the most frequent number given a dictionary where the numbers are the keys and the values are their counts
# Specifically here, finds the most frequent lotto number among all the lotto numbers
def find_most_frequent(dictionary_of_numbers_and_frequencies):
    most_frequent = 0
    frequency = 0
    for key, val in dictionary_of_numbers_and_frequencies.items():
        if val > frequency:
            most_frequent = key
            frequency = val
    return most_frequent
#bterry7 & aheim
def main():
    # Testing or using?
    test_or_run = int(input("1. Run Normally\n2. Test Cases\nEnter choice (1 or 2): "))
    
    while True:
        if test_or_run == 1:

            # Define seperate option for reading in data, for debugging plotting if reading from url is not working
            '''
            # prompt the user to enter a choice
            choice = int(input("1. File\n2. Url\nEnter choice (1 or 2): "))
            # if the choice is not one of the 2 options
            while choice != 1 and choice != 2:
                print("Invalid choice")
            choice = int(input("1. Enter file\n2.Enter url:\n"))
            '''

            # Matches with commented debugging option
            choice = 2
            # if data is file
            if choice == 1:
                source = input("Enter filename: ")
            # else if data is url
            else:
                source = input("Enter url: ")
            break
        elif test_or_run == 2:
            while True:
                test = int(input('Please Select Test Case (enter 1, 2, or 3) \n 1: Correct URL, expected data/no errors \n 2: Incorrect URL \n 3: Correct URL, unexpected data/with errors \n Choice: '))
                if test == 1:
                    source = "http://web.eecs.utk.edu/~cosc505/data/lottonums.csv"
                    break
                elif test == 2:
                    source = 'asdfadsf'
                    break
                elif test == 3:
                    source = "http://web.eecs.utk.edu/~cosc505/data/lottonums_large.csv"
                    break
                else:
                    print('Incorrect Input, please select test case 1, 2, or 3 \n')
            break
        else:
            print('Incorrect Input, please select test case 1 or 2 \n')

#aheim & wchollma
    # load the data into the dataframe
    try:
        lotto_data_frame = pandas.read_csv(source)
    # else if some error occurred notify user with message
    except Exception as e:
        print("Error: ", e)
        print("Terminating the program.")
        quit()

    # dictionary to store all the lotto numbers and frequencies
    lotto_numbers = {}
    # dictionary to store all the megaball numbers and frequencies
    megaball = {}
  
    # iterate through each row of the data frame
    for index, row in lotto_data_frame.iterrows():
        # assign all the lotto numbers to numbers
        numbers = [int(x) for x in row['Winning Numbers'].strip().split()]
        # add all the lotto numbers to the dictionary
        for num in numbers:
            lotto_numbers[num] = 1 + lotto_numbers.get(num, 0)
        megaball_num = int(row['Mega Ball'])
        # add the megaball number to the dictionary
        megaball[megaball_num] = 1 + megaball.get(megaball_num, 0)
    
          
# mrichesi & bterry7
# plot
# sort lotto numbers in order of ball number for graphing
    plt_lotto = dict(sorted(lotto_numbers.items()))
    plt_mega = dict(sorted(megaball.items()))

# separate keys and values from megaball   
    m_keys = list(plt_mega.keys())
    m_vals = list(plt_mega.values())
# separate keys and values from lotto_numbers  
    l_keys = list(plt_lotto.keys()) 
    l_vals = list(plt_lotto.values())
# plot lotto numbers and megaball
    plt.plot(l_keys, l_vals, label="Lotto Numbers")
    plt.plot(m_keys, m_vals, label="Megaball")
# set limits of y axis relative to max values on each axis
    plt.xlim (0 * .05,max(l_keys) + max(l_keys) * .05)
    # More responsive for larger data sets; ymin of 0 for "small" frequencies
    if (max(l_vals) + (max(l_vals) * .1) < 200):
        plt.ylim(0, max(l_vals) + (max(l_vals) * .1))
    else:
        plt.ylim(max(m_vals) - (max(m_vals) * .1), max(l_vals) + (max(l_vals) * .1))
# Title graph, x axis, y axis, and add legend
    plt.title("Winning Lotto Numbers Frequency", fontsize=10)
    plt.ylabel ('Frequency')
    plt.xlabel ('Ball Number')
    plt.legend (loc = "upper right", fontsize = 'xx-small')
# Red line  
# sort frequency values with highest frequency first and turn to string
    lne = sorted(lotto_numbers.items(),key=operator.itemgetter(1),reverse=True)
    lne = str(lne)
    lne_xval = ','.join(lne).split(',')
# turn ballnumber relative to highest frequency into string for label
    lne_xval_str = (lne_xval[2] + lne_xval[3])
#turn ballnumber relative to highest frequency into integer for x value of line
    lne_xval = int(lne_xval_str)
#plot line and text for red line
    plt.axvline(x= lne_xval , color = 'r')
    plt.text(lne_xval + 1 ,max(l_vals),"Most Frequent = "+ lne_xval_str)

#wchollma & bterry7
#draw arrow for megaball    
    most_freq_mega = find_most_frequent(megaball)
    mega_txt = "Megaball = " + str(most_freq_mega)
    mega_offset_x = most_freq_mega * 0.4
    mega_offset_y = megaball[most_freq_mega] * 0.4
    # Text Annotation
    plt.annotate(mega_txt, xy = (most_freq_mega, megaball[most_freq_mega]), 
                    xycoords = 'data', xytext= (most_freq_mega + mega_offset_x, megaball[most_freq_mega]  + mega_offset_y), 
                    textcoords='data', horizontalalignment='left', verticalalignment='bottom', fontsize = 8)
    # Arrow; attaching the arrow to the same annotation with formatting was causing to allign with the bottom middle of the text. This corrects that issue
    plt.annotate('',xy = (most_freq_mega, megaball[most_freq_mega]), 
                    xycoords = 'data', xytext= (most_freq_mega + mega_offset_x, megaball[most_freq_mega]  + mega_offset_y),
                    arrowprops = dict(
                        facecolor='black',
                        arrowstyle = 'simple, head_width=0.8,tail_width=0.1, head_length=0.7'))

    plt.show()
if __name__ == '__main__':
    main()
