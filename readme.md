## Explanation video link https://youtu.be/DC_oqTlcTEc

## Design Patterns
1. The core of this application uses the REPL Command Pattern to encapsulate each operation (e.g., Add, Subtract, Multiply, Divide) as a command with an execute() method. This allows for easy extension (e.g., adding new plugins) without modifying existing code
2. Abstract Base Class: Command in app/commands/__init__.py
3. Defines the execute() method as an abstract method.
4. Concrete Commands: AddCommand, SubtractCommand, MultiplyCommand, DivideCommand in their respective plugin folders (e.g., app/plugins/add/__init__.py).
5. Each implements execute(), prompting for input and performing the calculation.
6. Commands can be dynamically registered and executed by name via the CommandHandler (see app/commands/__init__.py), making the system highly extensible.

## Environmental Variable
1. We use this to access .csv file name to store the history
2. We use this to keep the log file names where all the error logs will be stored.

## Logging
1. We log both informational messages and errors to help monitor the application and debug issues.
2. We log errors if a plugin fails to import, warnings if directories are missing etc

## 
