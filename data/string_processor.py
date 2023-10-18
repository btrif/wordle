#  Created by Bogdan Trif on 2023.10.18 , 9:34 PM ; btrif

import re

def process_file_text(file_in, file_out):

    with open(file_in, "r") as f_in:
        M = [ line.split('/')[-1].rstrip('\n') for line in f_in.readlines() ]
        M .sort()
        for line in f_in.readlines() :
            print(line.split('/')[-1] )
    print(M)

    with open(file_out, "w") as f_out:
        for line in M :
            f_out.write(line+'\n')





process_file_text('movies_in.txt', 'movies_az.txt')