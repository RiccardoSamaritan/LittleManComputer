# RICCARDO SAMARITAN SM3201396

from lmc_exceptions import *
from lmc_queue import LMC_Queue
from memory_cell import MemoryCell

MIN_VALUE = 0
MAX_VALUE = 999
MEMORY_SIZE = 100

class LMC:
    """
    Simulates the Little Man Computer (LMC), a simple model of a CPU with memory, 
    input/output queues, and basic instructions.
    """
    def __init__(self):
        """
        Initializes the LMC with memory, registers, and I/O queues.
        """
        self.memory = [MemoryCell(content=0) for _ in range(MEMORY_SIZE)]  # Memory cells
        self.accumulator = 0  # Register to hold arithmetic results
        self.program_counter = 0  # Tracks the current instruction address
        self.input_queue = LMC_Queue()  # Queue for input values
        self.output_queue = LMC_Queue()  # Queue for output values
        self.overflow_flag = False  # Indicates arithmetic overflow
        self.halted = False  # Indicates if the program has halted

        # Mapping opcodes to corresponding methods
        self.instruction_set = {
            1: self._add,
            2: self._subtract,
            3: self._store,
            5: self._load,
            6: self._branch,
            7: self._branch_if_zero,
            8: self._branch_if_positive,
            9: self._handle_input_output
        }

    def fetchNextInstruction(self):
        """
        Fetches the next instruction from memory and increments the program counter.

        :returns: The current memory cell containing the instruction.
        :raises IndexError: If the program counter is out of bounds.
        """
        if not (0 <= self.program_counter < MEMORY_SIZE):
            raise IndexError("Program counter out of bounds.")
        cell = self.memory[self.program_counter]
        self.program_counter += 1
        return cell

    def executeInstruction(self, cell: MemoryCell):
        """
        Decodes and executes the instruction in the given memory cell.

        :param cell: The memory cell containing the instruction.
        :raises ValueError: If the opcode is invalid.
        """
        if cell.opcode in self.instruction_set:
            self.instruction_set[cell.opcode](cell.address)
        else:
            raise ValueError(f"Invalid opcode: {cell.opcode}")

    def _add(self, address: int):
        """
        Adds the value at the specified memory address to the accumulator.

        :param address: Memory address to fetch the value from.
        """
        value = self.getMemoryCellValue(address)
        self.accumulator = (self.accumulator + value) % 1000
        self.overflow_flag = not (MIN_VALUE <= self.accumulator <= MAX_VALUE)

    def _subtract(self, address: int):
        """
        Subtracts the value at the specified memory address from the accumulator.

        :param address: Memory address to fetch the value from.
        """
        value = self.getMemoryCellValue(address)
        self.accumulator = (self.accumulator - value) % 1000
        self.overflow_flag = not (MIN_VALUE <= self.accumulator <= MAX_VALUE)

    def _store(self, address: int):
        """
        Stores the value of the accumulator into the specified memory address.

        :param address: Memory address to store the value.
        """
        self.validateMemoryAddress(address)
        self.memory[address].content = self.accumulator

    def _load(self, address: int):
        """
        Loads the value from the specified memory address into the accumulator.

        :param address: Memory address to load the value from.
        """
        self.accumulator = self.getMemoryCellValue(address)

    def _branch(self, address: int):
        """
        Sets the program counter to the specified address (unconditional jump).

        :param address: Memory address to jump to.
        """
        self.program_counter = address

    def _branch_if_zero(self, address: int):
        """
        Jumps to the specified address if the accumulator is zero.

        :param address: Memory address to jump to.
        """
        if self.accumulator == 0 and not self.overflow_flag:
            self.program_counter = address

    def _branch_if_positive(self, address: int):
        """
        Jumps to the specified address if the accumulator is positive.

        :param address: Memory address to jump to.
        """
        if not self.overflow_flag:
            self.program_counter = address

    def _handle_input_output(self, address: int):
        """
        Handles input and output operations.

        :param address: Determines whether to perform input (1) or output (2).
        :raises EmptyInputQueueException: If the input queue is empty during input.
        """
        if address == 1:  # Input
            if self.input_queue.empty():
                raise EmptyInputQueueException("Input queue is empty.")
            self.accumulator = self.input_queue.dequeue()
        elif address == 2:  # Output
            self.output_queue.enqueue(self.accumulator)

    def initializeMemory(self, machine_codes, input_data=[]):
        """
        Loads machine codes into memory and populates the input queue.

        :param machine_codes: List of tuples containing opcodes and addresses.
        :param input_data: List of input values for the program.
        """
        for value in input_data:
            self.input_queue.enqueue(value)
        for i, (opcode, address) in enumerate(machine_codes):
            if opcode is not None:
                self.memory[i] = MemoryCell(opcode=opcode, address=address)
            else:
                self.memory[i] = MemoryCell(content=address)

    def getMemoryCellValue(self, address: int) -> int:
        """
        Retrieves the value stored at the specified memory address.

        :param address: Memory address to retrieve the value from.
        :returns: The content of the memory cell.
        """
        self.validateMemoryAddress(address)
        return self.memory[address].content

    def validateMemoryAddress(self, address: int):
        """
        Validates that the specified memory address is within bounds.

        :parameter address: Memory address to validate.
        :raises IndexError: If the address is out of bounds.
        """
        if not (0 <= address < MEMORY_SIZE):
            raise IndexError(f"Address {address} out of bounds.")

    def executeProgram(self):
        """
        Executes the program until a HALT instruction is encountered.
        """
        while not self.halted:
            self.executeSingleInstruction()

    def executeProgramStepwise(self):
        """
        Executes the program one instruction at a time.
        """
        if not self.halted:
            self.executeSingleInstruction()

    def executeSingleInstruction(self):
        """
        Executes a single instruction in the program.
        """
        cell = self.fetchNextInstruction()
        if cell.opcode is None:
            raise HaltException("Data interpreted as instruction.")
        if cell.opcode == 0:  # HALT
            self.halted = True
        else:
            self.executeInstruction(cell)