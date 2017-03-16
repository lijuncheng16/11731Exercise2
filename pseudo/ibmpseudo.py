# -*- encoding: utf-8 -*-
'''
  Alignment: P( E | F) = Σ_θ P( θ, F | E) (Equation 98)
  IBM model 1: P( θ, F | E)
  (1) Initialize θ[i,j] = 1 / (|E| + 1) (i for E and j for F) (Equation 100) 
  (2) Expectation-Maximization (EM)
    [E] C[i,j] =  θ[i,j] / Σ_i θ[i,j] (Equation 110)
    [M] θ[i,j] =  C[i,j] / Σ_j C[i,j] (Equation 107)
  (3) Calculate data likelihood (Equation 106)
'''

class IBM():
  def __init__(self, bitext, max_iter = 7):
    self.bitext = bitext
    self.max_iter = max_iter

  def train(self):
    # (1) Initialize θ[i,j] = 1 / (|E| + 1) (Equation 100)
    self.theta[ e[i], f[j] ] = TODO
    for iter in range(self.max_iter):
      # (2) [E] C[i,j] = θ[i,j] / Σ_i θ[i,j] (Equation 110)
      count[e[i], f[j]] = TODO
      # (2) [M] θ[i,j] =  C[i,j] / Σ_j C[i,j] (Equation 107)
      self.theta[ e[i], f[j] ] = TODO 
      # (3) Calculate log data likelihood (Equation 106)
      ll = TODO
    # (Optional) save/load model parameters for efficiency
		[0] Log Likelihood : -5.232084
		[1] Log Likelihood : -4.542094
		[2] Log Likelihood : -4.321830
		[3] Log Likelihood : -4.244019
		[4] Log Likelihood : -4.209469
		[5] Log Likelihood : -4.191590
		[6] Log Likelihood : -4.181324

  def align(self):
    for idx, (e, f) in enumerate(self.bitext):
      for i in range(len(e)):
        # ARGMAX_j θ[i,j] or other alignment in Section 11.6 (e.g., Intersection, Union, etc)
        max_j, max_prob = argmax_j(f, e[i])
      self.plot_alignment((max_j, max_prob), e, f)
    return alignments

def main():

  bitext = read_bitext_file(args.train_source, args.train_target )
  # bitext = [ ( ['with', 'vibrant', ..], ['mit', 'hilfe',..] ), ([], []) , ..]
  ibm = IBM(bitext, max_iter = args.max_iter)
  ibm.train()
  ibm.align()

if __name__ == '__main__': main()