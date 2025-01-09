# RICCARDO SAMARITAN SM3201396

from lmc import LMC
from lmc_exceptions import *

class Assembler:

    def __init__(self, filename):
        """
        Initializes the Assembler object, responsible for loading and analyzing the assembly code.

        :parameter filename: The name of the file containing the assembly code.
        """
        self.lmc = LMC() 
        self.filename = filename
        self.labels = {}
        self.instructions_dict = {
            "ADD": 1,
            "SUB": 2,
            "STA": 3,
            "LDA": 5,
            "BRA": 6,
            "BRZ": 7,
            "BRP": 8,
            "INP": 901,
            "OUT": 902,
            "HLT": 0,
            "DAT": None
        }

    def loadInstructionsFromFile(self):
        """
        Loads assembly instructions from a file and normalizes their format.

        :returns: A list of normalized instructions.
        """
        instr = []
        try:
            with open(self.filename, 'r') as f:
                for line in f:
                    line = line.split('//')[0].strip()  # Removes comments (anything after '//') and spaces.
                    if line:
                        instr.append(self.normalizeInstruction(line))  # Adds the normalized instruction.
        except FileNotFoundError:
            print(f"Error: The file '{self.filename}' was not found.")
        except Exception as e:
            print(f"Error reading the file: {e}")  # Handles any other errors during file reading.

        return instr

    def normalizeInstruction(self, instruction):
        """
        Normalizes the instruction: converts it to uppercase and removes extra spaces.

        :parameter instruction: The instruction to normalize.
        :returns: The normalized instruction.
        """
        return ' '.join(instruction.upper().split())  # Removes extra spaces and converts to uppercase.

    def parseActionInstruction(self, instruction):
        """
        Analyzes an action-type instruction (e.g., 'ADD', 'SUB') and returns the machine code.

        :parameter instruction: The instruction to analyze.
        :returns: A list containing the opcode and the operand.
        """
        machine_code = 0
        try:
            opcode = self.parseInstructionOpcode([instruction[0]])  # Gets the opcode for the instruction.
            operand = int(instruction[1])  # Converts the operand to an integer.
        except InstructionNotFoundException:
            pass  
        except ValueError:
            try:
                # If operand is not a number, it might be a label.
                machine_code += self.get_label_address()(instruction[1])
            except LabelNotFoundException:
                pass
        except Exception:
            print("Unexpected error occurred during action parsing.")

        return [opcode, operand]  # Returns the machine code of the instruction.

    def parseIoInstruction(self, instruction):
        """
        Analyzes an input/output instruction (e.g., 'INP', 'OUT') and returns its machine code.

        :parameter instruction: The input/output instruction to analyze.
        :returns: A list containing the opcode and the operand, divided into two parts.
        """
        value = 0
        # If the instruction is valid, it gets the corresponding machine code.
        code = self.getMachineCode(instruction[0])
        if code is not None:
            value += code
        else:
            return [None, value]  # Returns None if the instruction is not valid.

        # Returns the machine code split into two parts (opcode and operand).
        return [value // 100, value % 100]

    def parseInstructionOpcode(self, instruction):
        """
        Analyzes a single "word" (part of the instruction) and returns its corresponding machine code.

        :parameter instruction: A list containing the instruction to analyze.
        :returns: The machine code of the instruction.
        """
        if instruction:
            return self.getMachineCode(instruction[0])  # Returns the machine code for the instruction.
        return None  # If the instruction is empty, returns None.

    def getMachineCode(self, word):
        """
        Converts a word (e.g., 'ADD', 'SUB') into its corresponding machine code.

        :parameter word: The word of the instruction.
        :returns: The machine code corresponding to the word.
        """
        # Checks if the word exists in the instructions dictionary.
        if word in self.instructions_dict:
            return self.instructions_dict[word]
        raise InstructionNotFoundException  # Raises an exception if the word is not found.

    def extractLabels(self, instructions):
        """
        Identifies labels in the assembly code, stores them with their memory addresses, and removes them from the instructions.

        :parameter instructions: A list of assembly instructions.
        :returns: A list of instructions with labels removed.
        """
        wiped_instructions = []  # List to store instructions without labels.
        for i, instruction in enumerate(instructions):
            parts = instruction.split()  # Splits the instruction into words.
            if len(parts) == 3:  # If there's a label, it will be the first word.
                self.labels[parts[0]] = i  # Stores the label with its memory address.
                del parts[0]  # Removes the label from the instruction.
            elif len(parts) == 2 and parts[0] not in self.instructions_dict:
                # If the first part is not a valid instruction, treat it as a label.
                self.labels[parts[0]] = i
                del parts[0]  # Removes the label.
            wiped_instructions.append(parts)  # Adds the instruction without the label.

        return wiped_instructions  # Returns the list of instructions without labels.

    def substituteLabelsWithAddresses(self, instructions):
        """
        Replaces labels in the instructions with their memory addresses.

        :parameter instructions: The list of instructions containing labels.
        """
        for instruction in instructions:
            # If the last word is a label, replace it with its memory address.
            if instruction[-1] in self.labels:
                instruction[-1] = self.labels[instruction[-1]]

    def get_label_address(self, label):
        """
        Searches for a label in the labels dictionary.

        :parameter label: The name of the label.
        :returns: The memory address of the label.
        """
        # If the label exists in the dictionary, return its memory address.
        if label in self.labels:
            return self.labels[label]
        raise LabelNotFoundException  # Raises an exception if the label is not found.
