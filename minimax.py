from sys import maxsize

#   Tree

class Node: # THE GOAL TREE OF THIS ALGORITHM WILL BE MADE OF NODES
    def __init__(self, i_depth, i_playernum, i_sticksRemaining, i_value=0):
        self.i_depth = i_depth #    STORES THE DEPTH OF THE NODE INSIDE THE TREE
        self.i_playernum = i_playernum #    TAKES IN THE MINIMUM PLAYER OR THE MAXIMUM PLAYER
        self.i_sticksRemaining = i_sticksRemaining #    STORES THE STICKS REMAINING AT THIS NODE
        self.i_value = i_value #    IF IT IS A WINNING MOVE OF LOOSING MOVE THIS WILL STORE -INFINITY OR +INFINITY
        self.children = [] #    STORES THE TWO BRANCHES OF THIS NODE INCLUDING EACH AND EVERY SINGLE BRANCH OF THOSE NODES
        print("\t\t"*(abs(5-i_depth)), (i_depth, i_playernum, i_sticksRemaining, i_value))  # UNCOMMENT THIS TO SEE THE GOAL TREE 
        self.CreateChildren() # THIS CLASS FUNCTION WILL CREATE THE BRANCHES OF THIS NODE WHICH ARE AT THE LOWER DEPTHS


    def CreateChildren(self):
        if self.i_depth >= -2: # THIS FUNCTION WILL PROCEED ONLY TILL IT REACHES A NODE AT DEPTH -2
            for i in range(1, 3): # SINCE WE CAN REMOVE ONLY TWO STICKS THIS LOOP WILL ITERATE TWICE CREATING TWO BRANCHES IN THE GOAL TREE
                v = self.i_sticksRemaining - i #    THIS PASSES THE REMAINING STICKS AFTER THIS MOVE IS TAKEN TO THE CHILD
                self.children.append( Node( self.i_depth-1,
                                            -self.i_playernum, v, self.RealVal(v))) #   THE CHILD IS STORED IN A LIST

    def RealVal(self, value):
        if value == 0: 
            return maxsize * self.i_playernum # IF THE REMAINING STICKS IS ZERO THEN THIS IS THE WINNING MOVE FOR THIS PLAYER
        elif value < 0:
            return maxsize * -self.i_playernum # IF THE REMAINING STICKS IS LESS THAN ZERO THIS MOVE FAVOURS THE OPPONENT        
        return 0 #  IF THE STICKS REMAINING IS NON NEGATIVE OR ZERO WE CANNOT COME TO A CONCLUSION ABOUT THIS MOVE 

def MinMax(node, i_depth, i_playerNum):
    #print("Now I am at depth ", i_depth) # USED FOR DEBUGGING
    if i_depth == -2: # THIS RETURNS THE NODE VALUE WHEN THE TREE COMES TO A DEPTH OF -2
        #print("reached depth ", i_depth, " hence terminating ", " got return value ", node.i_value)
        return node.i_value #   IF THE PROGRAM REACHES THE FINAL DEPTH OF THE GOAL TREE RETURNS THE NODE VALUE OF THE LAST NODE
    
    if abs(node.i_value) == maxsize: #  THIS RETURNS THE NODE VALUE IF THE NODE HAS ONE THATS NON ZERO
        #print("HI")
        return node.i_value

    i_bestValue = maxsize * -i_playerNum #  IF NO BESTVALUE IS FOUND WHEN ITERATING THROUGH THE BRANCHES RETURNS THIS AS IT IS IN FAVOUR OF THE OPPONENT

    for i in range(len(node.children)): #   ITERATES THROUGH EVERY BRANCH OF THE GOAL TREE 
        child = node.children[i]
        i_val = MinMax(child, i_depth-1, -i_playerNum) #    RECURSION OCCURS TILL THE DEPTH BECOMES -2 OR A NODE VALUE IS FOUND

        if (abs(maxsize * i_playerNum - i_val) < abs(maxsize * i_playerNum - i_bestValue)) and i_bestValue != i_val:# IF THE NODE REUTRNS THE VALUE DESIRED BY THE PLAYER IT IS ASSIGNED TO BESTVALUE 
            i_bestValue = i_val
            #print("Best value was changed @ ", (child.i_depth, child.i_playernum, child.i_sticksRemaining, i_bestValue))

    return i_bestValue #    IF A BEST VALUE IS FOUND THROUGH RECURSION RETURN THIS VALUE

def WinCheck(i_sticks, i_playerNum): # CHECKS IF A PLAYER HAS WON
    if i_sticks <= 0:
        print("*"*30)
        if i_playerNum > 0:
            if i_sticks == 0:
                print("\tYou Win!")
            else:
                print("\tToo Many.You Lose")
        else:
            if i_sticks == 0:
                print("\tComputer Wins...Better Luck Next Time")
            else:
                print("\tComp Error")

        print("*"*30)
        return 0
    return 1

if __name__ == '__main__':
    # INITIALIZE THE TOTAL STICKS , DEPTH OF THE TREE AND THE STARTINGG PLAYER
    i_stickTotal = 11 # TOTAL NO OF STICKS IN THIS GAME
    i_depth = 5 # THE DEPTH OF THE GOAL TREEE THE COMPUTER WILL BUILD
    i_curPlayer = 1 # THIS WILL BE +1 FOR THE HUMAN AND -1 FOR THE COMPUTER
    print("""There are 11 sticks in total.\nYou can choose 1 or 2 sticks in each turn.\n\tGood Luck!!""")
    # GAME LOOP
    while i_stickTotal > 0:
        print("\n{} sticks remain. How many would you pick?".format(i_stickTotal))
        try:
            i_choice = int(input("\n1 or 2: "))
            if  i_choice - 1 == 0 or i_choice - 2 == 0:            
                i_stickTotal -= int(i_choice)
                if WinCheck(i_stickTotal, i_curPlayer):
                    i_curPlayer *= -1
                    node = Node(i_depth, i_curPlayer, i_stickTotal)
                    bestChoice = -100
                    i_bestValue = -i_curPlayer * maxsize

                    #   Determine No of Sticks to Remove

                    for i in range(len(node.children)):
                        n_child = node.children[i]
                        #print("heres what it look like ", n_child.i_depth, "and",i_depth)
                        i_val = MinMax(n_child, i_depth-1, i_curPlayer)
                        if abs(i_curPlayer * maxsize - i_val) <= abs(i_curPlayer*maxsize-i_bestValue):
                            i_bestValue = i_val
                            bestChoice = i
                            #print("Best value was changed @ ", i_depth, " by " , -i_curPlayer, " branch ", i, " to ", i_bestValue)



                    bestChoice += 1
                    print("Computer chooses: " + str(bestChoice) + "\tbased on value: " + str(i_bestValue))
                    i_stickTotal -= bestChoice
                    WinCheck(i_stickTotal, i_curPlayer)
                    i_curPlayer *= -1
                else:
                    print("You can take only a maximum of two sticks.")
                
        except:
            print("Invalid input.Only Numeric Values are accepted")
        
                
