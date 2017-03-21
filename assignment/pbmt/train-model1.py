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

class IBM():
    def __init__(self, bitext, output_file, max_iter=20):
        self.bitext = bitext
        self.max_iter = max_iter
        self.theta = defaultdict(lambda: defaultdict(float))
        self.bi_count = defaultdict(lambda: defaultdict(float))
	self.e_count = defaultdict(float)
        self.e_counter = Counter(chain(*[pair[0] for pair in bitext]))
        self.e_vocab_size = len(self.e_counter.keys())*1.0
	#self.e_vocab_size = 10000.0
	print self.e_vocab_size
        self.epsilon = 1.0/ max ([len(line)for line in [pair[1] for pair in bitext]])
	print "epsilon:", self.epsilon
        self.output_file = output_file

    def train(self):
        # (1) Intitial theta[i][j] = 1/ e_vocab_size (Equation 100)
        for indx, (e, f) in enumerate(self.bitext):
            for i in range(len(e)):
                self.e_count[e[i]] += 1
                for j in range(len(f)):
                    self.theta[e[i]][f[j]] = 1/self.e_vocab_size

        # (2) [E] C[i,j] = theta[i,j] / sigma_i theta[i,j] (Equation 110)
        self.bi_count = defaultdict(lambda: defaultdict(float))
        self.e_count = defaultdict(float)
        for iter in range(self.max_iter):
            for indx, (e, f) in enumerate(self.bitext):
                if (indx+1)%1000==0:
                    print "iter, bitext_indx:", iter, indx
                for j in range(len(f)):
                    sum_theta = 0.0
                    for i in range(len(e)):
                        sum_theta += self.theta[e[i]][f[j]]
                    for i in range(len(e)):
                        self.bi_count[e[i]][f[j]] += (self.theta[e[i]][f[j]])/sum_theta
                        self.e_count[e[i]] += (self.theta[e[i]][f[j]])/sum_theta

            # (3) [M] theta[i,j] =  C[i,j] / sigma_j C[i,j] (Equation 107)
            for e_k, e_dict in self.theta.iteritems():
                for f_k in e_dict:
                    self.theta[e_k][f_k] = self.bi_count[e_k][f_k]/self.e_count[e_k]
            # (4) Calculate log data likelihood (Equation 106)
            ll = str(self.calculate_ll())
            print "iteration: {} log data likelihood : {}".format(iter, ll)
            print "sample theta:", self.theta["klein"]["small"]

    def calculate_ll(self):
        ll = 0.0
        for indx, (e, f) in enumerate(self.bitext):
            ll += math.log(self.epsilon)-float(len(f)) * math.log(float(len(e))+1)
            for j in range(len(f)):
                sum_theta = 0.0
                for i in range(len(e)):
                    sum_theta += self.theta[e[i]][f[j]]
                ll += math.log(sum_theta)
		#print ll
        ll /= (indx+1.0)
	print ll

    def align(self):
        output_file = open(self.output_file,"w")
        for indx, (e, f) in enumerate(self.bitext):
            results = []
            for i in range(len(e)):
                max_j, max_prob = -1, -1.0
                for j in range(len(f)):
                    if self.theta[e[i]][f[j]] > max_prob:
                        max_j = j
                        max_prob = self.theta[e[i]][f[j]]
                results.append("{}-{}".format(max_j,i))
            line = " ".join(results)
            output_file.write(line+"\n")

def read_bitext(source_filename, target_filename):
    """Output format: [ ( ['with', 'vibrant', ..], ['mit', 'hilfe',..] ), ([], []) , ..]"""
    output = []
    src_lines = open(source_filename).readlines()
    tgt_lines = open(target_filename).readlines()
    for src_line, tgt_line in zip(src_lines, tgt_lines):
        src_words = src_line.split()
        tgt_words = tgt_line.split()
        output.append((src_words, tgt_words))
    return output

if __name__ == "__main__":
    source_file = "/home/billyli/Documents/11731Exercise2/en-de/train.en-de.low.filt.de"
    target_file = "/home/billyli/Documents/11731Exercise2/en-de/train.en-de.low.filt.en"
    output_file = "/home/billyli/Documents/11731Exercise2/output/alignment.txt"

    bitext = read_bitext(source_file,target_file)
    model = IBM(bitext,output_file)
    model.train()
    model.align()
