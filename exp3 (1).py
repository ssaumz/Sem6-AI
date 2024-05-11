class VacuumCleaner:
    def __init__(self, location, state_A,state_B):
        self.location = location
        self.state_A = state_A
        self.state_B=state_B
    def clean_environment(self):
        score=0
        if self.location=='A':
            print("Location: {}".format(self.location))
            if self.state_A==1:
                self.state_A=0
                print("A is dirty.\n Sucking dirt at A")
                print("A is clean")
            else:
                print('A is clean')
                
            print("Moving to B")
            self.location='B'
            score+=1
            print("Location:{}".format(self.location))
            if self.state_B==1:
                self.state_B=0
                print("B is dirty.\n Sucking dirt at B.")
                print("B is clean")
            else:
                print('B is clean')
            score+=1
        else:
            print("Location:{}".format(self.location))
            if self.state_B==1:
                self.state_B=0
                print("B is dirty.\n Sucking dirt at B.")
                print("B is clean")
            else:
                print('B is clean')

            print("Moving to A")
            self.location='A'
            score+=1
            print("Location: {}".format(self.location))
            if self.state_A==1:
                self.state_A=0
                print("A is dirty.\n Sucking dirt at A")
                print('A is clean')
            else:
                print('A is clean')

            score+=1

        if self.state_A==0 and self.state_B==0:
            print("The enivironmemt is clean ")
            print("Score is:",score)



# Take user input for initial location and state
initial_location = input("Enter initial location (A or B): ").upper()
state_A = int(input("Enter state for A (0 for clean, 1 for dirty): "))
state_B = int(input("Enter state for B (0 for clean, 1 for dirty): "))


vacuum = VacuumCleaner(initial_location,state_A,state_B)
vacuum.clean_environment()

