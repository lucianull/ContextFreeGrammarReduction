from queue import Queue

class ContextFreeGrammar:
    def __init__(self, text_file) -> None:
        self.Variables = []
        self.Terminals = []
        self.Rules = {}
        self.StartVariable = []
        with open(text_file) as inFILE:
            while True:
                line = inFILE.readline().rstrip()
                if line == "":
                    break
                if line == "Variables:":
                    line = inFILE.readline().rstrip()
                    while line != "End":
                        self.Variables.append(line)
                        line = inFILE.readline().rstrip()
                if line == "Terminals:":
                    line = inFILE.readline().rstrip()
                    while line != "End":
                        self.Terminals.append(line)
                        line = inFILE.readline().rstrip()
                if line == "Start variable:":
                    line = inFILE.readline().rstrip()
                    while line != "End":
                        self.StartVariable.append(line.rstrip())
                        line = inFILE.readline().rstrip()
                if line == "Rules:":
                    line = inFILE.readline().rstrip()
                    while line != "End":
                        arrow_pos = line.find("->")
                        state = line[:arrow_pos]
                        if state not in self.StartVariable:
                            self.Rules[state] = []
                        line = line[arrow_pos + 2:]
                        pos = line.find('|')
                        while pos != -1:
                            self.Rules[state].append(line[:pos])
                            line = line[pos + 1:]
                            pos = line.find('|')
                        self.Rules[state].append(line)
                        line = inFILE.readline().rstrip()
        self.Terminals.append('^')
            
                
    def getVariables(self) -> list:
        return self.Variables


    def getTerminals(self) -> list:
        return self.Terminals


    def getRules(self) -> dict:
        return self.Rules


    def getStartVariable(self):
        return self.StartVariable
    

    def Validate(self) -> bool:
        if len(self.StartVariable) > 1:
            return 0
        for terminal in self.Terminals:
            if terminal in self.Variables:
                return 0
        for key, value in self.Rules.items():
            if key not in self.Variables:
                return 0
            for states in value:
                for x in states:
                    if x not in self.Variables and x not in self.Terminals:
                        return 0
        return 1


    def UselessReduction(self) -> None:
        VariablesFreq = [0 for x in range(len(self.Variables))]
        TerminalsFreq = [0 for x in range(len(self.Terminals))]
        VariablesPos = {}
        TerminalsPos = {}
        i = 0
        for x in self.Variables:
            VariablesPos[x] = i
            i += 1
        i = 0
        for x in self.Terminals:
            TerminalsPos[x] = i
            i += 1
        queue = Queue()
        queue.put(self.StartVariable[0])
        VariablesFreq[VariablesPos[self.StartVariable[0]]] = 1
        while queue.empty() == 0:
            state = queue.get()
            if state in VariablesPos:
                for transition in self.Rules[state]:
                    for x in transition:
                        if x in TerminalsPos:
                            TerminalsFreq[TerminalsPos[x]] = 1
                        else:
                            if VariablesFreq[VariablesPos[x]] == 0:
                                queue.put(x)
                                VariablesFreq[VariablesPos[x]] = 1
        Variables = []
        Terminals = []
        Rules = {}
        for x in self.Variables:
            if VariablesFreq[VariablesPos[x]] == 1:
                Variables.append(x)
        for x in self.Terminals:
            if TerminalsFreq[TerminalsPos[x]] == 1:
                Terminals.append(x)
        self.Variables = Variables
        self.Terminals = Terminals
        for x, y in self.Rules.items():
            if x in self.Variables:
                Rules[x] = y
        self.Rules = Rules

    
    def NullReduction(self) -> None:
        epsilonTransition = [x for x, y in self.Rules.items() for z in y if '^' in z]
        for state in epsilonTransition:
            for x, y in self.Rules.items():
                try:
                    self.Rules[x].remove('^')
                except:
                    pass
                for z in y:
                    if state in z:
                        i = 0
                        n = len(self.Rules[x])
                        while i < n:
                            letter_index = 0
                            for letter in self.Rules[x][i]:
                                if letter == state:
                                    newRule = self.Rules[x][i][:letter_index] + self.Rules[x][i][letter_index + 1:]
                                    if newRule not in self.Rules[x]:
                                        self.Rules[x].append(newRule)
                                        n += 1
                                letter_index += 1
                            i += 1
                        break
    

    def Check(self, state) -> bool:
        for s in self.Rules[state]:
            if s in self.Variables:
                return 0
        return 1

    
    def UnitReduction(self):
        ok = 1
        while ok:
            ok = 0
            for key in self.Rules.keys():
                state_index = 0
                n = len(self.Rules[key])
                while state_index < n:
                    if self.Rules[key][state_index] in self.Variables and self.Check(self.Rules[key][state_index]):
                        state = self.Rules[key][state_index]
                        self.Rules[key].pop(state_index)
                        n -= 1
                        for x in self.Rules[state]:
                            if x not in self.Rules[key]:
                                self.Rules[key].append(x)
                                ok = 1
                                n += 1
                        state_index -= 1
                    state_index += 1
            
    
    def PrintContextFreeGrammar(self) -> None:
        print("Variables:")
        for x in self.Variables:
            print(x)
        print("End")
        for x in self.Terminals:
            print(x)
        print("End")
        print("Rules:")
        for x, y in self.Rules.items():
            rule = ""
            for z in y:
                rule = rule + '|' + z
            print(x + '->' + rule[1:])
        print("End")
        print("Start Variable:")
        print(self.StartVariable[0])
        print("End")


if __name__ == '__main__':
    CFG = ContextFreeGrammar("cfg_config_file")
    if CFG.Validate() == 1:
        print("The CFG introduced is valid")
    else:
        print("The CFG introduced is invalid")
