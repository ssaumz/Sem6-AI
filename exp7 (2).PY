class BayesianNetwork:
    def __init__(self):
        self.prob_b = 0.002
        self.prob_no_b = 0.998
        self.prob_e = 0.001
        self.prob_no_e = 0.999
        # Conditional probability tables
        self.prob_alarm = {
            (True, True): 0.95,
            (True, False): 0.94,
            (False, True): 0.29,
            (False, False): 0.001
        }
        self.prob_john = {
            True: 0.90,
            False: 0.05
        }
        self.prob_mary = {
            True: 0.70,
            False: 0.01
        }
    def print_conditional_tables(self):
            print("Conditional probability table for Alarm A:")
            print("B\tE\tP(A=True)\tP(A=False)")
            for b in [True, False]:
                for e in [True, False]:
                    prob_a_true = self.prob_alarm[(b, e)]
                    print(f"{b}\t{e}\t{prob_a_true:.3f}\t\t{1 - prob_a_true:.3f}")
            print("\nConditional probability table for John Calls:")
            print("A\tP(J=True)\tP(J=False)")
            for a, prob_j_true in self.prob_john.items():
                print(f"{a}\t{prob_j_true:.3f}\t\t{1 - prob_j_true:.3f}")
            print("\nConditional probability table for Mary Calls:")
            print("A\tP(M=True)\tP(M=False)")
            for a, prob_m_true in self.prob_mary.items():
                print(f"{a}\t{prob_m_true:.3f}\t\t{1 - prob_m_true:.3f}")

            print("\nProbability table for Burglary:")
            print("B\tP(B=True)\tP(B=False)")
            print(f"True\t{self.prob_b:.3f}\t\t{self.prob_no_b:.3f}")

            print("\nProbability table for Earthquake:")
            print("E\tP(E=True)\tP(E=False)")
            print(f"True\t{self.prob_e:.3f}\t\t{self.prob_no_e:.3f}")
            
    def calculate_probabilities(self):
        # Calculate joint probability
        probability1 = self.prob_mary[True] * self.prob_john[True] * self.prob_alarm[False,False]*  self.prob_no_b * self.prob_no_e
        probability2 = (1-self.prob_mary[True]) * (1-self.prob_john[True]) * self.prob_alarm[False,False]*  self.prob_no_b * self.prob_no_e
        probability3 = self.prob_mary[True] * self.prob_john[True] * self.prob_alarm[False,True]*  self.prob_no_b * self.prob_e
        probability4 = self.prob_mary[True] * self.prob_john[True] * self.prob_alarm[True,True]*  self.prob_b * self.prob_e
        probability5 = self.prob_mary[False] * self.prob_john[False] * (1-self.prob_alarm[False,False])*  self.prob_no_b * self.prob_no_e
        return probability1, probability2, probability3, probability4, probability5

if __name__ == "__main__":
    bayesian_network = BayesianNetwork()
    bayesian_network.print_conditional_tables()
    probabilities = bayesian_network.calculate_probabilities()

    queries = [
        ("P(M, J, A, ~B, ~E)", "P (M|A) *P (J|A)*P (A|~B ^ ~E) *P (~B) *P (~E)"),
        ("P(~M, ~J, A, ~B, ~E)", "P (~M|A) *P (~J|A)*P (A|~B ^ ~E) *P (~B) *P (~E)"),
        ("P(M, J, A, ~B, E)", "P (M|A) *P (J|A)*P (A|~B ^ E) *P (~B) *P (E)"),
        ("P(M, J, A, B, E)", "P (M|A) *P (J|A)*P (A|B ^ E) *P (B) *P (E)"),
        ("P(M, J, ~A, ~B, ~E)", "P (M|~A) *P (J|~A)*P (~A|~B ^ ~E) *P (~B) *P (~E)")]

    for query, expansion in queries:
        index = queries.index((query, expansion))
        probability = probabilities[index]
        print(f"\nProbability for the query {query} = {expansion} = {probability:.10f}")
