# Converts the private dataset's .tsv.bz2 files into textfiles, removing anything but the 

import argparse
import bz2


parser = argparse.ArgumentParser(description='Script to convert a .tsv.bz2 file to a text file, by removing everything but the first column')
parser.add_argument('tsv', type=str, help='.tsv.bz2 file to convert')
parser.add_argument('txt', type=str, help='target file')
args = parser.parse_args()


with bz2.BZ2File(args.tsv, 'r') as f:
     with open(args.txt, 'w') as o:
             for line in f:
                     sentence = line.split('\t')[0]
                     o.write(sentence + '\n')

