# utils
Reusable code or "utilities" with definitions (interfaces) and implementations.
While this repository only supports Python interfaces currently, implementations of interfaces can be done in any language.

## Installation
`pip install -e .`  
Remove -e for production or if you won't be making any changes to the repository code.

Add the following to your .bashrc file or script for initializing your Python virtual environment:  
`export PYTHONPATH=$PYTHONPATH:<path to repository folder>/src`  

## Full list of instructions
The following terminal commands are from outside the repository directory (change env_utils to the filepath where you want to place the virtual environment files).  
`sudo apt install python3.8  
virtualenv --python /usr/bin/python3.8 env_utils

Add the following 6 lines to the file env_utils/bin/activate, replacing "utils" with what NAME is set to at line 17 of setup.py (change it to what you want your repository or package to be called):  
`export PYTHONPATH=<path to repository folder>/src`  
`alias def="repo_utils define"`  
`alias test="repo_utils test_def"`  
`alias finddef="repo_utils find_definition"`  
`alias mvdef="repo_utils rename_def"`  
`alias instdef="repo_utils install_def"`

`source env_utils/bin/activate`  
`cd utils`  
`pip install -e .`  

## Updating dependencies
`pip install -r requirements.txt`  

To install dependencies for a particular definition:  
`instdef <definition name>`  

## Goals
There are two principle goals for the organization of this repository:

- Reusability - Code is findable, understood, and useable in multiple contexts
- Experimentation - All interfaces can be implemented in multiple ways, and these implementations can be compared.

## Folders
- src - For code interfaces (definitions) and their implementations.
- src/solutions - Solutions contain the definitions of functions (snake_case), classes (camelCase), and other objects.
- src/metrics - Metrics are definitions which compare multiple implementations of an interface and return a number between 0 and 1.
- data - Standard data or test data, separated into folders
- notebooks - For ipynb files that can be run in a Jupyter notebook.

### Note on test files
- Instead of a separate tests folder, it's recommended to put a file starting with test_ in the same directory as the module being tested.

## Folders as categories
To start, code should be under at least one subfolder of src/objects or src/solutions, and data a subfolder under data. This encourages reasonable organization. Folder location can be changed later, since file path isn't needed for importing.

## Category labels
It's recommended to specify a list of `categories` at the top of in every code file. Example:  
`categories = ['recommendation', 'summarization']`  
This allows searching for code by category, and means a single module can have multiple categories. Each parent folder under src will be included as a category automatically.

## Importing
Regardless of file location, importing works as such:
`from repo_utils import summarize`
By adding the src directory to your Python path, you can import as such:
`from repo_utils import summarize`
The latter is how imports are done throughout the repository. Each of the top-level directories under src are considered namespaces.

## Definitions and Implementations
Every object and function in this repository is considered an interface, also called a solution definition, which could have many alternative implementations. This doesn't require coding any differently except when choosing to do the below. A function or object can be converted into an interface at any time without affecting other code that depends on it.

To define an interface, create a folder with the name to be imported, and then create a file inside it with the same name. This serves as the interface. Then either in the same file or as separate files, create implementations. These can even be imported from subfolders.

Implementations aren't intended to be publicly accessible except by the interface. To use a specific implementation, set the `version` parameter of the interface after importing.

Unit tests are generally for the defined interface, and these should be put in the same folder as the interface. There can also be unit tests for specific implementations as needed. Test filenames start with "test_".

Metrics are placed in a separate metrics folder, since metrics may apply to multiple definitions. Metrics themselves have interfaces and implementations. However, metrics return a single number.

For those definitions that have associated metrics, the implementation used for that definition will be the one with the highest metric scores.

## Command Line Interface
The standard command line interface for the repository is defined at src/solutions/project/command_line. All definitions are automatically useable by the command line, and this command line interface is available after installation (by executing the name of the repository).

Usage:
`repo_utils <namespace> <definition name>`  

Examples:
`repo_utils find_definition define`  
`repo_utils solutions test_def define`

Here are recommended aliases for your .bashrc file for convenience:  
`alias def="repo_utils define"`  
`alias test="repo_utils test_def"`  
`alias finddef="repo_utils find_definition"`  
`alias mvdef="repo_utils rename_def"`  
`alias instdef="repo_utils install_dependencies"`  

To go to the directory of a definition:  
`cd $(finddef <definition name>)`
