from __future__ import print_function
import sys
import math
from collections import defaultdict

import os, codecs

print(os.path)

def main(argv):
	ctxts1 = 0.0  # total word count
	ctxts2 = defaultdict(lambda: 0.0)  # bigram denominator count
	count1 = defaultdict(lambda: 0.0)  # unigram count
	count2 = defaultdict(lambda: 0.0)  # bigram count
	stateid = defaultdict(lambda: len(stateid))

	outfile = open(sys.argv[2], "w")

	with open(sys.argv[1], "r") as infile:
	    for line in infile:
		item = line.strip().split("\t")
		print (item)
		src = item[0].strip().split("\t")
		#print (src) 
		tgt = item[1].strip().split("\t")
		#print (tgt)
		logProb = item[2]

		vals = line.strip().split("\t") + ["</s>"]
		ctxt = "<s>"

		for idx, val in enumerate(src + tgt):
		    text = src + tgt
		    if idx > 0:
			prev_state = ctxt + " ".join(text[:idx])
		    else:
			prev_state = ctxt

		    next_state = ctxt + " ".join(text[:(idx + 1)])
		    if idx <= len(src):
			prev_label = False
		    else:
			prev_label = True
		    if idx <= (len(src) - 1):
			next_label = False
		    else:
			next_label = True

		    if prev_label:
			cut_position=len(src)
		    else:
			cut_position = 0
		    prev_state=(prev_state,prev_label,cut_position)

		    if next_label:
			cut_position=len(src)
		    else:
			cut_position = 0
		    next_state=(next_state,next_label,cut_position)

		    if not prev_state in stateid or not next_state in stateid:
			if idx < len(src):
			    print("%d %d %s <eps>" % (stateid[prev_state], stateid[next_state], val), file=outfile)
			else:
			    print("%d %d <eps> %s" % (stateid[prev_state], stateid[next_state], val), file=outfile)
		    last_stateid = stateid[next_state]
		    if not prev_state in stateid or not next_state in stateid:
			if idx < len(src):
			    print("%d %d %s <eps>" % (stateid[prev_state], stateid[next_state], val), file=outfile)
			else:
			    print("%d %d <eps> %s" % (stateid[prev_state], stateid[next_state], val), file=outfile)
		    last_stateid = stateid[next_state]


		print("%d 0 <eps> <eps> %s" % (last_stateid, logProb), file=outfile)

	    print("0 0 </s> </s>", file=outfile)
	    print("0 0 <unk> <unk>", file=outfile)
	    print("0", file=outfile)

if __name__ == "__main__":
	main(sys.argv)
