# RICCARDO SAMARITAN SM3201396

from processor import LMCProcessor
import argparse
from pathlib import Path

def main():

    # Parse command-line arguments, specifying the program to execute, the input queue, and the execution mode. 
    # If no execution mode is specified, the program will execute the entire program by default.
    parser = argparse.ArgumentParser(description="Execute an LMC Assembly program.")
    parser.add_argument("--program", required=True, help="Name of the Assembly file to execute (located in the 'tests' folder).")
    parser.add_argument("--input", help="Input queue (comma-separated integers).", default="")
    parser.add_argument("--mode", choices=["all", "steps"], default="all", help="Execution mode: 'all' (entire program) or 'steps' (step-by-step execution). Default mode is 'all'.")
    args = parser.parse_args()

    try:
        # Check if the specified program file exists
        if not Path(f"./tests/{args.program}").exists():
            print("Error: The specified file does not exist.")
            return

        # Initialize the processor with the provided program file
        processor = LMCProcessor(f"./tests/{args.program}")
        instructions = processor.loadAndNormalizeInstructions()

        # Resolve labels in the Assembly program
        resolved_instructions = processor.processLabels(instructions)

        # Convert resolved instructions into machine codes
        machine_codes = processor.convertResolvedInstructionsToMachineCode(resolved_instructions)

        # PREPARATION PHASE
        if args.input:
            # If input is provided: read it and covert it to a list of integers
            input_queue = [int(x) for x in args.input.split(",") if x.strip()]

            # Initialize the LMC memory with machine codes and input queue
            processor.initializeLmcMemory(machine_codes, input_queue)
        else:
            # Initialize the LMC memory with only machine codes
            processor.initializeLmcMemory(machine_codes)

        # EXECUTION PHASE
        if args.mode == "all":
            # Execute the entire program
            processor.executeProgram()
            print("Program finished with the following output queue:", processor.getOutputQueue())
            input("Press ENTER to inspect the LMC\n")
            # Display a summary of the LMC state
            print(processor.getLmcSummary())

        elif args.mode == "steps":
            # Execute the program step-by-step
            while processor.isProgramRunning():
                # Display the current state of the LMC
                output = processor.getLmcSummary()
                print(output)
                input("Press ENTER to execute the next step...")
                # Execute the next instruction
                processor.executeNextInstruction()
            print("Program finished with the following output queue:", processor.getOutputQueue())

    except ValueError:
        # Handle invalid input format (non-integer values)
        print("Error: Please provide integers separated by commas.")
        return
    except Exception as e:
        # Handle unexpected errors
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
