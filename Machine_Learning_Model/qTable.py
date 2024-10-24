import numpy as np
from itertools import product
import json
from settings import VISION_RANGE
import os

class QTable:
    def __init__(self):
        self.state_values = [i for i in range(VISION_RANGE+1)] + [16]
        self.state_variables = 5
        self.n_actions = 2
        try:
            with open('qTable.json', 'r') as file:
                data = json.load(file)
            
            if not data:
                print("Could not load Q-Table, creating new one (JSON file was empty)")
                self.Q = self.initQ()
            else:
                print("Successfully loaded Q-Table from file")
                self.Q = data
        
        except (FileNotFoundError, json.JSONDecodeError):
            print("Could not load Q-Table from JSON, creating new one")
            self.Q = self.initQ()

    def initQ(self) : 
        Q= {}
        
        all_state_combinations = list(product(self.state_values, repeat=self.state_variables))

        for state_combination in all_state_combinations :
            Q[str(state_combination)] = {}
            for action in range(0,self.n_actions) :
                Q[str(state_combination)][str(action)] = 0
        return Q
    
    def saveQ(self, filename = "qTable.json"):
        with open('qTable.json', 'w') as file:
            json.dump(self.Q, file)
    
    def backupQ(self):
        filename = "qTable_backup"
        backup_folder = 'backup'
        os.makedirs(backup_folder, exist_ok=True)

        num_files = len([name for name in os.listdir(backup_folder) if os.path.isfile(os.path.join(backup_folder, name))])
        backup_filename = f"{filename}_{num_files}.json"
        full_path = os.path.join(backup_folder, backup_filename)

        file_index = 0
        while os.path.isfile(full_path):
            file_index += 1
            backup_filename = f"{filename}_{file_index}.json"
            full_path = os.path.join(backup_folder, backup_filename)

        with open(full_path, 'w') as file:
            json.dump(self.Q, file)

    def update(self,state,next_state,action,gamma,alpha,reward):
        combination = state.combination()
        next_combination = next_state.combination()
        next_max = max(self.Q[str(next_combination)].values())
        self.Q[str(combination)][str(action)] += alpha*(reward+gamma*next_max-self.Q[str(combination)][str(action)])
        return self.Q[str(combination)][str(action)]