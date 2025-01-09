# RICCARDO SAMARITAN SM3201396

from assembler import Assembler
from lmc import LMC
from lmc_exceptions import EmptyInputQueueException, HaltException

class LMCProcessor:
    """
    LMCProcessor orchestrates the process of loading, parsing, and executing assembly instructions
    using the Little Man Computer (LMC) model.
    """
    def __init__(self, filename):
        """
        Initialize the LMCProcessor with the specified assembly file.

        :param filename: The name of the file containing the assembly code.
        """
        self.filename = filename
        self.assembler = Assembler(filename)  # Assembler instance for handling assembly operations.
        self.lmc = LMC()  # Little Man Computer instance for execution.

    def loadAndNormalizeInstructions(self):
        """
        Loads and normalizes instructions from the assembly file.

        :returns: List of normalized instructions.
        """
        return self.assembler.loadInstructionsFromFile()

    def processLabels(self, instructions):
        """
        Identifies and resolves labels in the assembly instructions, replacing them with memory addresses.

        :parameter instructions: List of assembly instructions.
        :returns: List of resolved instructions with labels replaced by memory addresses.
        """
        resolved_instructions = self.assembler.extractLabels(instructions)
        self.assembler.substituteLabelsWithAddresses(resolved_instructions)
        return resolved_instructions

    def convertResolvedInstructionsToMachineCode(self, resolved_instructions):
        """
        Converts resolved assembly instructions into machine code.

        :parameter resolved_instructions: List of resolved assembly instructions.
        :returns: List of machine codes.
        """
        machine_codes = []
        for instruction in resolved_instructions:
            machine_codes.append(self.convertInstructionToMachineCode(instruction))
        return machine_codes

    def convertInstructionToMachineCode(self, instruction):
        """
        Parses a single assembly instruction into machine code.

        :param instruction: The instruction to parse.
        :returns: Machine code corresponding to the instruction.
        """
        machine_code = None
        if len(instruction) == 2:  # Action instruction with operand.
            machine_code = self.assembler.parseActionInstruction(instruction)
        elif len(instruction) == 1:  # Input/Output instruction.
            machine_code = self.assembler.parseIoInstruction(instruction)
        else:
            raise ValueError("Invalid instruction format.")  # Handle unexpected instruction format.
        return machine_code

    def initializeLmcMemory(self, machine_codes, input_data=None):
        """
        Initializes the LMC memory with machine codes and input data.

        :param machine_codes: List of machine codes to load into memory.
        :param input_data: Input data queue for the LMC (default: empty list).
        """
        if input_data is None:
            input_data = []
        self.lmc.initializeMemory(machine_codes, input_data)

    def executeProgram(self):
        """
        Runs the LMC program to completion, handling potential exceptions.
        """
        try:
            self.lmc.executeProgram()
        except EmptyInputQueueException as e:
            print(f"Error: {e}")
        except HaltException as e:
            print(f"LMC halted: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def isProgramRunning(self):
        """
        Checks whether the LMC can continue running.

        :returns: True if the LMC is not halted, False otherwise.
        """
        return not self.lmc.halted

    def executeNextInstruction(self):
        """
        Executes the LMC program one step at a time.
        """
        self.lmc.executeProgramStepwise()

    def getOutputQueue(self):
        """
        Retrieves the results from the LMC output queue.

        :returns: List of items in the output queue.
        """
        return self.lmc.output_queue.items

    def getLmcSummary(self):
        """
        Creates an Output instance summarizing the LMC's current state.

        :returns: An Output object containing the LMC state summary.
        """
        return LMCSummary(
            program_counter=self.lmc.program_counter,
            accumulator=self.lmc.accumulator,
            memory=self.lmc.memory,
            output_queue=self.lmc.output_queue,
            input_queue=self.lmc.input_queue,
        )

class LMCSummary:
    """
    Represents the state of the Little Man Computer (LMC) at a specific point in time.
    """
    def __init__(self, program_counter, accumulator, memory, output_queue, input_queue):
        """
        Initializes the Output object with the LMC's state.

        :param program_counter: Current program counter.
        :param accumulator: Current accumulator value.
        :param memory: Current state of memory cells.
        :param output_queue: Current state of the output queue.
        :param input_queue: Current state of the input queue.
        """
        self.program_counter = program_counter
        self.accumulator = accumulator
        self.memory = memory
        self.output_queue = output_queue
        self.input_queue = input_queue

    def __str__(self):
        """
        Generates a formatted string representation of the LMC state.

        :returns: Formatted string summarizing the LMC state.
        """
        memory_state = "\n".join([f"{i:02d}: {cell.content}" for i, cell in enumerate(self.memory)])

        return (
            f"~~~ LMC State ~~~\n"
            f"Program Counter: {self.program_counter}\n"
            f"Accumulator: {self.accumulator}\n"
            f"Input Queue:\n{self.input_queue.items}\n"
            f"Output Queue:\n{self.output_queue.items}\n"
            f"Memory:\n{memory_state}\n"
            f"~~~~~~~~~~~~~~~~~"
        )