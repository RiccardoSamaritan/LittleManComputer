# RICCARDO SAMARITAN SM3201396

class MemoryCell:
    """
    Represents a memory cell that can store either data or an instruction.
    """
    def __init__(self, content=None, opcode=None, address=None):
        if content is not None:
            self._validate_content(content)
            self._content = content
            self._opcode = None
            self._address = None
        elif opcode is not None and address is not None:
            self._validate_opcode(opcode)
            self._validate_address(address)
            self._content = (opcode * 100) + address
            self._opcode = opcode
            self._address = address
        else:
            raise ValueError("Must provide either content or both opcode and address.")

    @staticmethod
    def _validate_content(content):
        if not isinstance(content, int):
            raise ValueError("Content must be an integer.")

    @staticmethod
    def _validate_opcode(opcode):
        if not isinstance(opcode, int) or not (0 <= opcode <= 9):
            raise ValueError("Opcode must be an integer between 0 and 9.")

    @staticmethod
    def _validate_address(address):
        if not isinstance(address, int) or not (0 <= address <= 99):
            raise ValueError("Address must be an integer between 0 and 99.")

    @property
    def content(self):
        """Gets the content of the cell."""
        return self._content

    @content.setter
    def content(self, value):
        self._validate_content(value)
        self._content = value
        self._opcode = None
        self._address = None

    @property
    def opcode(self):
        """Gets the opcode of the instruction, if applicable."""
        return self._opcode

    @property
    def address(self):
        """Gets the address of the instruction, if applicable."""
        return self._address

    def __repr__(self):
        return f"MemoryCell(content={self._content})"