# LittleManComputer

## Description

This is a simple implementation in Python of the LittleManComputer (LMC). The project was carried out as part of the final exam of the "Advanced and parallel programming" course at the University of Trieste. 

The program is able to execute the LMC instructions and to print the state of the memory and the registers at each step. The program can also execute the LMC instructions in a step-by-step mode, allowing the user to execute the program instruction by instruction.

---

## How to run the program

To run the program, you need to have Python installed on your machine. The program was developed using Python 3.8.5, but it should work with any version of Python 3.

To run the program, you need to execute the following command:

```bash
python main.py --program <file_name> --input <input_queue> --mode <execution_mode>
```

where:
```
<file_name> is the name of the .lmc file containing the LMC program
<input_queue> is the input queue to be used by the program
<execution_mode> is the execution mode of the program (either 'all' or 'step'). If not specified, the program will run in 'all' mode, which means that the program will execute all the instructions in the program at once.
```

---

## Example of usage

To run the program, you can use the following example:

```bash
python main.py --program fibonacci.lmc --input 5 --mode all
```

This command will execute the LMC program contained in the `fibonacci.lmc` file with the input queue set to 5. The program will execute all the instructions at once.
We expect the program to print the Fibonacci's series up to the 5th element. The ouput should be:

```
Program finished with the following output queue: [0, 1, 1, 2, 3]
```

Another example of usage is the following:

```bash
python main.py --program multiplication.lmc --input 13,13
```

This command will execute the LMC program contained in the `multiplication.lmc` file with the input queue set to 13,13. The program will execute all the instructions at once because the mode is not specified. We expect the program to print the result of the multiplication of 13 by 13. The ouput should be:

```
Program finished with the following output queue: [169]
```
---
