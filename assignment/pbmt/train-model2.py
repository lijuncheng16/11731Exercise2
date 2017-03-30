#-*- encoding: utf-8 -*-
'''
  Alignment: P( E | F) = Σ_θ P( θ, F | E) (Equation 98)
  IBM model 1: P( θ, F | E)
  (1) Initialize θ[i,j] = 1 / (|E| + 1) (i for E and j for F) (Equation 100) 
  (2) Expectation-Maximization (EM)
    [E] C[i,j] =  θ[i,j] / Σ_i θ[i,j] (Equation 110)
    [M] θ[i,j] =  C[i,j] / Σ_j C[i,j] (Equation 107)
  (3) Calculate data likelihood (Equation 106)
'''
import sys
from collections import defaultdict, Counter
import math
from itertools import count, chain 
import IBMModel2
from nltk.translate import AlignedSent

def read_bitext(source_filename, target_filename):
    """Output format: [ ( ['with', 'vibrant', ..], ['mit', 'hilfe',..] ), ([], []) , ..]"""
    output = []
    src_lines = open(source_filename).readlines()
    tgt_lines = open(target_filename).readlines()
    for src_line, tgt_line in zip(src_lines, tgt_lines):
	#print 'src_line: ', src_line
	#print 'tgt_line: ', tgt_line
        src_words = src_line.split()
	#print 'src_words: ', src_words
        tgt_words = tgt_line.split()
        output.append(AlignedSent(src_words, tgt_words))
    return output

if __name__ == "__main__":
    source_file = "/home/billyli/Documents/11731Exercise2/en-de/train.en-de.low.filt.de"
    target_file = "/home/billyli/Documents/11731Exercise2/en-de/train.en-de.low.filt.en"
    output_file = "/home/billyli/Documents/11731Exercise2/output/alignment-model2.txt"

    bitext = read_bitext(source_file, target_file)
    ibm2 = IBMModel2.IBMModel2(bitext, output_file, 3)
    print('translation score buch-book: {0:.3f}'.format(ibm2.translation_table['buch']['book']))

