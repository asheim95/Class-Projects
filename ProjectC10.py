# Project C10.py
#This program parses a url containing dna information and information on diseases people have in a .json 
#and shows which may be correlated in an output file  
#to get the information from a url use -u followed by the url
# Group members:
#   Will Chollman (wchollman)
#   Andrew Heim (aheim)
#   Matthew Richesin (mrichesi)
#   Mitchell Sutton (msutto11)
#   09-August-2019
# Responsibilities:
#   wchollman - get people with disease and opening url from command 
#   aheim - line outputting the correlated sequences
#   mrichesi - dictionary set up and calculate matching pattern
#   msutto11 - runtime analysis and commenting

import json 
from collections import Counter 
import argparse 
import sys
import urllib.request

# create a dictionary for the given diseases with keys corresponding
#   to the letter in the original data 
disease_list = { 
    'a': 'Pancreatic cancer',
    'b': 'Breast cancer',
    'c': 'Lung cancer',
    'd': 'Lymphoma',
    'e': 'Leukemia',
    'A': 'Gastro-reflux',
    'B': 'Hyperlipidemia',
    'C': 'High blood pressure',
    'D': 'Macular degeneration (any degree)'
}

#a= DNA string 1
#b = DNA string 2
#item frequqnce item of previous calculation
#p1 person 1 metadata
#p2 person 2 metadata

# nested while and for loops
# while loop is O(N)
# for loop is O(N)
# all other operations are constant
# total timing is O(N^2)
def calculate_matching_pattern(a, b, item, p1, p2): 
    n = len(a)
    i = 0 
    max_string = "" 
    while(i <= n-3): #N ops
        max_string = "" 
        for j in range(i+3, n): #N ops
            if a[i:j] == b[i:j]: 
                max_string = a[i:j] 
            else:
                if(max_string): 
                    key_string = str(i)+"#*#"+str(j) 
                    if not max_string in item: 
                        d = {} 
                        d[key_string] = [p1, p2] 
                        item[max_string] = d 
                    else: 
                        alread_exiting_post = item[max_string]  
                        if key_string in alread_exiting_post: 
                            if not p1 in alread_exiting_post[key_string]:
                                alread_exiting_post[key_string].append(p1) 
                            if not p2 in alread_exiting_post[key_string]: 
                                alread_exiting_post[key_string].append(p2) 
                        else:
                            alread_exiting_post[key_string] = [p1, p2] 
                    i = j 
                    break 
        i = i+1        
#Takes a disese letter, emr data and, list of people and returns the people who have the disease as string
#dis_letter - disease letter
#emr_data - EMR data 
#people - List people that have the DNA match
        
# single for loop
# K operations in the for loop
# all other operations are constant order
# total timing is O(K)
def get_people_with_disease(dis_letter, emr_data, people_list):
    res = [] 
    for people in people_list: 
        if dis_letter in emr_data[people]: 
            res.append(people) 
    return ",".join(res) 
# opens file from cmd
if __name__ == '__main__':
    parser = argparse.ArgumentParser() 
    parser.add_argument('-d', action='store', dest='is_debug', 
        help='Enable debug', default=False) 
    parser.add_argument('-ot', action='store', dest='output_type', 
        help='Output type - for console', default="file") 
    parser.add_argument('-u', action= 'store', dest= 'url', type= str, 
        help='Json url') 
    results = parser.parse_args() 
    is_debug=results.is_debug 
    if not results.url: 
        print("Please enter a valid url with -u in your arguments") 
        sys.exit(0) 
    with urllib.request.urlopen(results.url) as f:
        content = f.read() 
# gets dna and emr data from json file
    data = json.loads(content) 
    item = (data['dna']) 
    emr_data = data['emr'] 
# lists dna sequence and position
    freq_item = {} 
# lists all meta data keys and adds keys to list
    key_list = [] 
    times = 0 
    
    # the following series of for loops (one nested set) is
    # O(M) and O(L^2) respectively. 
    for i in item: #M ops
        key_list.append(i) 
    key_list_size = len(key_list) #
# iterates through dna to find matches or prints debug message 
    for i in range(0, key_list_size): #L ops
        if is_debug: 
            print("Running iteration "+str(i+1)+" of "+str(key_list_size)) 
        for j in range(0, key_list_size): #L ops
            if(i != j): 
                calculate_matching_pattern(item[key_list[i]], item[key_list[j]],freq_item, key_list[i], key_list[j]) 
# outputs the diseases that are correlated and tells which people they were correlated for
    output_string=" " 
    if is_debug: 
        print("Comparing DNA matches please wait...") 
    # the following segment has a series of nested for loops
    # each of the for loops runs over a different number items
    # at the worst, if P is the maximum number of items,
    # the segement is O(P^3)
    for freq in freq_item:
        pos_with_disease = freq_item[freq] 
        for ite in pos_with_disease: 
            disease_string = "" 
            size = len(pos_with_disease[ite])
            for val in pos_with_disease[ite]: 
                disease_string = disease_string+emr_data[val]
            print(freq,disease_string)
            disease_counter = Counter(disease_string) 
            output_string+=freq+":\n" 
            for c in disease_counter:  
                percentage = (disease_counter[c]/size)*100 
                people_list_string = get_people_with_disease(
                    c, emr_data, pos_with_disease[ite]) 
                if(percentage >= 40 and percentage < 60): 
                    output_string+="\t"+disease_list[c]+': Slightly correlated\n'
                    output_string+="\t\t"+people_list_string+"\n"
                elif(percentage >= 60 and percentage < 80): 
                    output_string+="\t"+disease_list[c]+': Moderately correlated\n'
                    output_string+="\t\t"+people_list_string+"\n"
                elif(percentage > 80):
                    output_string+="\t"+disease_list[c]+': Significantly correlated\n'
                    output_string+="\t\t"+people_list_string+"\n"
                else:
                    pass
            output_string+="\tAll IDs with sequence:\n" 
            output_string+="\t\t"+",".join(pos_with_disease[ite])+"\n" 
        if results.output_type=='-': 
            print(output_string)
        else:
            with open('output.txt','w+') as f:
                f.write(output_string)
