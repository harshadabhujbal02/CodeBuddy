from flask import Flask, jsonify, render_template, request
import os
import re
import json
try:
    from dotenv import load_dotenv
    # Load .env from the project folder, even if Flask is launched from another directory.
    load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"), override=False)
except ImportError:
    pass

app = Flask(__name__)

UNITS = [
    {"id": 1, "title": "Fundamentals of OOP", "hours": 7, "topics": ["Procedural programming vs OOP", "Basic and derived data types", "Constants, tokens, keywords, identifiers and variables", "Classes and objects", "struct vs class", "Control structures, arrays and strings", "Functions and prototypes", "Constructors and destructors", "Memory management", "Static members and inline functions", "Friend functions"]},
    {"id": 2, "title": "Inheritance", "hours": 7, "topics": ["Base and derived classes", "Protected members", "Class relationships", "Constructors and destructors in inheritance", "Function overriding", "Inheritance hierarchies", "Public and private inheritance", "Types of inheritance", "Ambiguity in multiple inheritance", "Virtual base classes", "Abstract classes", "Friend and nested classes"]},
    {"id": 3, "title": "Polymorphism", "hours": 7, "topics": ["Types of polymorphism", "Unary and binary operator overloading", "Function overloading", "Runtime polymorphism", "Base-class pointers", "Virtual and pure virtual functions", "Vtables", "Virtual destructors", "Abstract base classes"]},
    {"id": 4, "title": "Files and Streams", "hours": 7, "topics": ["File handling and file types", "Streams and stream classes", "File handling headers", "Opening, reading and writing files", "File pointers and navigation", "File error handling"]},
    {"id": 5, "title": "Exception Handling and Templates", "hours": 7, "topics": ["try, catch and throw", "Built-in and standard exceptions", "Custom exceptions", "Function templates", "Class templates", "Variable templates", "Default and non-type template arguments", "Template argument deduction"]},
    {"id": 6, "title": "Standard Template Library (STL)", "hours": 7, "topics": ["STL components", "Iterators", "Container adapters", "array, vector, queue, deque and forward_list", "set, multiset, map and multimap", "unordered associative containers", "Sorting, searching, copying and counting algorithms"]},
]

PRACTICALS = [
    "Find the sum of digits of an integer", "Display prime numbers between 1 and n", "Declare and define a class; access its members", "Demonstrate default, parameterized and copy constructors", "Create a STUDENT class", "Demonstrate operator overloading and function overloading", "Demonstrate a friend function and friend class", "Implement different types of inheritance", "Sort values using a template", "Handle exceptions using try and catch", "Catch all exceptions using catch(...)"
]

QA = [
    {"keys": ["what is oop", "object oriented programming"], "question": "What is OOP?", "answer": "OOP stands for Object-Oriented Programming. It organizes programs around classes and objects and commonly uses encapsulation, abstraction, inheritance and polymorphism."},
    {"keys": ["what is a class", "define class"], "question": "What is a class?", "answer": "A class is a user-defined type that groups data members and member functions into one unit. It acts as a blueprint for creating objects."},
    {"keys": ["what is an object", "define object"], "question": "What is an object?", "answer": "An object is an instance of a class. It has its own state (data) and can use the behaviours defined by the class."},
    {"keys": ["encapsulation"], "question": "What is encapsulation?", "answer": "Encapsulation combines data and the functions that operate on it in a class. Access specifiers such as private, protected and public help control access."},
    {"keys": ["inheritance", "types of inheritance"], "question": "What is inheritance?", "answer": "Inheritance lets a derived class reuse or extend features of a base class. Common forms are single, multiple, multilevel, hierarchical and hybrid inheritance."},
    {"keys": ["polymorphism"], "question": "What is polymorphism?", "answer": "Polymorphism means one interface or name can represent different behaviours. Compile-time examples include function/operator overloading; runtime polymorphism commonly uses virtual functions."},
    {"keys": ["abstraction"], "question": "What is abstraction?", "answer": "Abstraction exposes essential operations while hiding implementation details. In C++, abstract classes can be created with at least one pure virtual function."},
    {"keys": ["constructor", "types of constructor"], "question": "What is a constructor?", "answer": "A constructor is a special member function called when an object is initialized. Common forms taught in this course are default, parameterized and copy constructors."},
    {"keys": ["destructor"], "question": "What is a destructor?", "answer": "A destructor is called when an object is destroyed. Its name is the class name prefixed with ~, it has no return type, and it takes no parameters."},
    {"keys": ["function overloading", "overloading"], "question": "What is function overloading?", "answer": "Function overloading defines multiple functions with the same name but different parameter lists. The compiler selects a matching overload from the call arguments."},
    {"keys": ["function overriding", "overriding"], "question": "What is function overriding?", "answer": "Overriding occurs when a derived class provides a matching implementation of a base-class virtual function. It supports runtime polymorphism when called through a suitable base reference or pointer."},
    {"keys": ["virtual function", "pure virtual"], "question": "What is a virtual function?", "answer": "A virtual function enables dynamic dispatch: when called through a base-class pointer or reference, the derived implementation can be selected at runtime. A pure virtual function is declared with = 0."},
    {"keys": ["friend function", "friend class"], "question": "What is a friend function?", "answer": "A friend function is not a member of the class, but the class can grant it access to private and protected members using the friend declaration."},
    {"keys": ["file handling", "fstream", "ifstream", "ofstream"], "question": "How does file handling work in C++?", "answer": "Include <fstream>. Use std::ifstream to read, std::ofstream to write, or std::fstream for both. Check that the file opened successfully before reading or writing."},
    {"keys": ["exception", "try catch", "try-catch", "throw"], "question": "What is exception handling?", "answer": "Exception handling manages runtime error conditions. Put risky code in try, raise an exception with throw, and handle matching exception types in catch blocks."},
    {"keys": ["template", "function template", "class template"], "question": "What is a template in C++?", "answer": "Templates let functions or classes work with types specified as parameters, supporting reusable generic code. Function and class templates are included in this syllabus."},
    {"keys": ["stl", "standard template library"], "question": "What is the STL?", "answer": "The Standard Template Library provides reusable containers, iterators and algorithms. This syllabus includes sequence, associative and unordered associative containers plus sorting, searching, copying and counting algorithms."},
    {"keys": ["vector", "array container"], "question": "What is a vector in C++?", "answer": "std::vector is a sequence container that stores elements contiguously and can grow or shrink dynamically. Include <vector> and write std::vector<T>."},
    {"keys": ["difference between class and struct", "struct vs class"], "question": "What is the difference between class and struct in C++?", "answer": "For class, members and base classes are private by default. For struct, they are public by default. Both can have data, functions, constructors and inheritance."},
]

QUIZ = [{'unit': 1, 'q': 'Which keyword declares a class?', 'options': ['object', 'class', 'define', 'new'], 'answer': 1, 'explanation': 'The class keyword declares a class.'}, {'unit': 1, 'q': 'What is an object?', 'options': ['A loop', 'An instance of a class', 'A header', 'A function prototype'], 'answer': 1, 'explanation': 'An object is an instance of a class.'}, {'unit': 1, 'q': 'What is encapsulation?', 'options': ['Combining data and methods', 'Repeating code', 'Sorting data', 'Opening files'], 'answer': 0, 'explanation': 'Encapsulation bundles data and methods and controls access.'}, {'unit': 1, 'q': 'Which access is default in class?', 'options': ['public', 'private', 'protected', 'global'], 'answer': 1, 'explanation': 'Class members are private by default.'}, {'unit': 1, 'q': 'Which access is default in struct?', 'options': ['private', 'protected', 'public', 'static'], 'answer': 2, 'explanation': 'Struct members are public by default.'}, {'unit': 1, 'q': 'What is a constructor?', 'options': ['A special initializer', 'A loop', 'A namespace', 'A return type'], 'answer': 0, 'explanation': 'Constructors initialize objects.'}, {'unit': 1, 'q': 'What symbol begins a destructor name?', 'options': ['!', '~', '#', '&'], 'answer': 1, 'explanation': 'A destructor name is prefixed by ~.'}, {'unit': 1, 'q': 'Can a constructor have a return type?', 'options': ['Yes, int', 'Yes, void', 'No', 'Only bool'], 'answer': 2, 'explanation': 'Constructors have no return type.'}, {'unit': 1, 'q': 'What is function overloading?', 'options': ['Same name, different parameter lists', 'Same name only', 'Different classes only', 'Same return type only'], 'answer': 0, 'explanation': 'Overloads differ by parameter lists.'}, {'unit': 1, 'q': 'Can return type alone overload functions?', 'options': ['Yes', 'No', 'Only with static', 'Only in templates'], 'answer': 1, 'explanation': 'Return type alone cannot distinguish overloads.'}, {'unit': 1, 'q': 'Which keyword declares a constant variable?', 'options': ['constant', 'finalize', 'const', 'fixed'], 'answer': 2, 'explanation': 'const declares an object that cannot be modified through that name.'}, {'unit': 1, 'q': 'What does inline suggest?', 'options': ['No function call', 'Compiler may substitute function body', 'Always faster', 'Makes global variable'], 'answer': 1, 'explanation': 'inline is an optimization/linkage-related specifier, not a speed guarantee.'}, {'unit': 1, 'q': 'What is a friend function?', 'options': ['Always a member', 'Non-member granted access', 'Constructor', 'Virtual method'], 'answer': 1, 'explanation': 'A class may grant a non-member friend access to private/protected members.'}, {'unit': 1, 'q': 'Which operator accesses a member through an object?', 'options': ['->', '.', '::', '&'], 'answer': 1, 'explanation': 'The dot operator accesses members through an object.'}, {'unit': 1, 'q': 'What does static data member mean?', 'options': ['One copy shared by class', 'One per object always', 'Local variable', 'Constant only'], 'answer': 0, 'explanation': 'A static data member belongs to the class rather than each instance.'}, {'unit': 2, 'q': 'What is inheritance?', 'options': ['Deriving a class from another', 'Opening a file', 'Looping', 'Casting only'], 'answer': 0, 'explanation': 'Inheritance allows a derived class to reuse or extend a base class.'}, {'unit': 2, 'q': 'Which is not a common inheritance form?', 'options': ['Single', 'Multiple', 'Multilevel', 'Circular'], 'answer': 3, 'explanation': 'Common forms include single, multiple, multilevel, hierarchical and hybrid.'}, {'unit': 2, 'q': 'Which access specifier allows derived classes access but hides from unrelated code?', 'options': ['private', 'protected', 'public', 'global'], 'answer': 1, 'explanation': 'protected members are accessible in derived classes.'}, {'unit': 2, 'q': 'Which syntax shows public inheritance?', 'options': ['class D + B', 'class D: public B', 'class D inherits B', 'class D -> B'], 'answer': 1, 'explanation': 'Use colon and public base-class name.'}, {'unit': 2, 'q': 'What is multiple inheritance?', 'options': ['One base, one derived', 'One class has multiple base classes', 'A class has many objects', 'Many functions'], 'answer': 1, 'explanation': 'A derived class can inherit from more than one base.'}, {'unit': 2, 'q': 'What can cause ambiguity in multiple inheritance?', 'options': ['Same member name in bases', 'Using int', 'Constructors only', 'Comments'], 'answer': 0, 'explanation': 'Same-named inherited members may require qualification.'}, {'unit': 2, 'q': 'How can inherited member ambiguity be resolved?', 'options': ['Scope qualification', 'Delete class', 'Use goto', 'Use typedef'], 'answer': 0, 'explanation': 'Use forms such as obj.BaseA::show().'}, {'unit': 2, 'q': 'What is multilevel inheritance?', 'options': ['A->B->C chain', 'One class two bases', 'Many derived siblings', 'No base'], 'answer': 0, 'explanation': 'A derived class becomes a base for another class.'}, {'unit': 2, 'q': 'What is hierarchical inheritance?', 'options': ['Several derived classes share one base', 'One chain', 'Multiple bases', 'No class'], 'answer': 0, 'explanation': 'Multiple derived classes inherit from one base.'}, {'unit': 2, 'q': 'What is a virtual base class used for?', 'options': ['Avoid duplicate shared base subobjects in diamond inheritance', 'Make all methods static', 'Create files', 'Overload operators'], 'answer': 0, 'explanation': 'Virtual inheritance can ensure a shared base subobject in a diamond.'}, {'unit': 2, 'q': 'Can a derived class access private base members directly?', 'options': ['Yes always', 'No, not directly', 'Only with public inheritance', 'Only static'], 'answer': 1, 'explanation': 'Private base members are not directly accessible to derived classes.'}, {'unit': 2, 'q': 'When are base constructors called?', 'options': ['After derived destructor', 'Before derived constructor body', 'Never', 'Only manually'], 'answer': 1, 'explanation': 'Base subobjects are initialized before the derived constructor body.'}, {'unit': 2, 'q': 'What is function overriding?', 'options': ['Derived redefines matching virtual function', 'Same name different params', 'Operator symbol', 'Template deduction'], 'answer': 0, 'explanation': 'Overriding supplies a derived implementation of a virtual function.'}, {'unit': 2, 'q': 'What does final on a class prevent?', 'options': ['Object creation', 'Further derivation', 'Member functions', 'Constructors'], 'answer': 1, 'explanation': 'A final class cannot be used as a base class.'}, {'unit': 2, 'q': 'What is an abstract class?', 'options': ['Class with a pure virtual function', 'Class with no methods', 'Only private class', 'Template class'], 'answer': 0, 'explanation': 'A class with a pure virtual function is abstract.'}, {'unit': 3, 'q': 'What is polymorphism?', 'options': ['Many forms/behaviours', 'Only data hiding', 'File reading', 'Memory allocation'], 'answer': 0, 'explanation': 'Polymorphism lets one interface represent different behaviours.'}, {'unit': 3, 'q': 'Function overloading is usually what type?', 'options': ['Runtime', 'Compile-time', 'File-time', 'No polymorphism'], 'answer': 1, 'explanation': 'Overload selection is generally compile-time.'}, {'unit': 3, 'q': 'What is operator overloading?', 'options': ['Define operator behavior for user-defined types', 'Create new symbols', 'Change precedence', 'Rename keywords'], 'answer': 0, 'explanation': 'It defines how existing operators work with user-defined types.'}, {'unit': 3, 'q': 'Which is a valid overloaded operator?', 'options': ['**', '+', '@', '%%'], 'answer': 1, 'explanation': 'Operators such as + can be overloaded for user-defined types.'}, {'unit': 3, 'q': 'Can operator precedence be changed by overloading?', 'options': ['Yes', 'No', 'Only +', 'Only classes'], 'answer': 1, 'explanation': 'Overloading does not change precedence or associativity.'}, {'unit': 3, 'q': 'What enables runtime dispatch?', 'options': ['Virtual functions', 'Macros', 'typedef', 'const only'], 'answer': 0, 'explanation': 'Virtual functions enable dynamic dispatch.'}, {'unit': 3, 'q': 'What is a pure virtual function syntax marker?', 'options': ['==0', '=0', '=>0', 'virtual()'], 'answer': 1, 'explanation': 'A pure virtual function declaration ends with = 0.'}, {'unit': 3, 'q': 'What is a vtable commonly associated with?', 'options': ['Virtual dispatch implementation', 'File stream', 'Template parameter', 'Loop control'], 'answer': 0, 'explanation': 'Compilers commonly use virtual tables to implement virtual dispatch.'}, {'unit': 3, 'q': 'Why use a virtual destructor in a polymorphic base?', 'options': ['Safe deletion through base pointer', 'Faster loops', 'Overload constructors', 'Prevent inheritance'], 'answer': 0, 'explanation': 'It ensures the derived destructor runs when deleting through a base pointer.'}, {'unit': 3, 'q': 'Can functions overload by parameter count?', 'options': ['Yes', 'No', 'Only templates', 'Only constructors'], 'answer': 0, 'explanation': 'Different parameter counts can distinguish overloads.'}, {'unit': 3, 'q': 'Can functions overload by parameter types?', 'options': ['Yes', 'No', 'Only return type', 'Only private'], 'answer': 0, 'explanation': 'Parameter types can distinguish overloads.'}, {'unit': 3, 'q': 'What does override keyword do?', 'options': ['Requests compiler check of overriding', 'Makes method private', 'Makes function static', 'Creates overload'], 'answer': 0, 'explanation': 'override helps detect signature mismatches.'}, {'unit': 3, 'q': 'Which operator is commonly unary?', 'options': ['++', '+ with two operands', '[]', '()'], 'answer': 0, 'explanation': 'Prefix/postfix ++ is unary.'}, {'unit': 3, 'q': 'What is a base pointer pointing to derived object useful for?', 'options': ['Runtime polymorphism', 'File sorting', 'Preprocessor', 'No use'], 'answer': 0, 'explanation': 'Virtual calls can dispatch to derived implementations.'}, {'unit': 3, 'q': 'Which must be user-defined for overloaded operator?', 'options': ['At least one operand type', 'Both operands must be int', 'No operands', 'Return type'], 'answer': 0, 'explanation': 'At least one operand must be a class or enumeration type.'}, {'unit': 4, 'q': 'Which header provides C++ file streams?', 'options': ['<fstream>', '<vector>', '<thread>', '<map>'], 'answer': 0, 'explanation': 'fstream provides file stream classes.'}, {'unit': 4, 'q': 'Which class is used for file input?', 'options': ['ofstream', 'ifstream', 'ostringstream', 'ostream only'], 'answer': 1, 'explanation': 'ifstream reads from files.'}, {'unit': 4, 'q': 'Which class is used for file output?', 'options': ['ifstream', 'ofstream', 'istream', 'istringstream'], 'answer': 1, 'explanation': 'ofstream writes to files.'}, {'unit': 4, 'q': 'Which mode truncates an existing output file?', 'options': ['ios::trunc', 'ios::in', 'ios::ate only', 'ios::binary only'], 'answer': 0, 'explanation': 'ios::trunc truncates existing content.'}, {'unit': 4, 'q': 'How should you check a file opened?', 'options': ['if(!file)', 'if(file==0.5)', 'while(false)', 'sizeof(file)'], 'answer': 0, 'explanation': 'Check the stream state before using it.'}, {'unit': 4, 'q': 'Which function reads a line into string?', 'options': ['getline', 'readline only', 'scanline', 'gets'], 'answer': 0, 'explanation': 'std::getline reads a line from a stream.'}, {'unit': 4, 'q': 'What does eof indicate?', 'options': ['End-of-file state', 'File opened', 'Write success only', 'Directory'], 'answer': 0, 'explanation': 'eofbit indicates an end-of-file condition has been encountered.'}, {'unit': 4, 'q': 'What does seekg change?', 'options': ['Input position', 'Output position only', 'File name', 'Stream type'], 'answer': 0, 'explanation': 'seekg moves the get/input position.'}, {'unit': 4, 'q': 'What does seekp change?', 'options': ['Output position', 'Input position only', 'File permissions', 'Buffer size'], 'answer': 0, 'explanation': 'seekp moves the put/output position.'}, {'unit': 4, 'q': 'What does tellg return?', 'options': ['Input position', 'Output bytes only', 'File size always', 'Error text'], 'answer': 0, 'explanation': 'tellg reports the input position.'}, {'unit': 4, 'q': 'Which stream supports both input and output files?', 'options': ['fstream', 'ifstream only', 'ofstream only', 'cout'], 'answer': 0, 'explanation': 'fstream supports both input and output.'}, {'unit': 4, 'q': 'What is ios::binary for?', 'options': ['Binary mode', 'Append only', 'Read only', 'Text conversion'], 'answer': 0, 'explanation': 'ios::binary requests binary mode.'}, {'unit': 4, 'q': 'What does ios::app do?', 'options': ['Writes at end', 'Truncates file', 'Reads only', 'Closes file'], 'answer': 0, 'explanation': 'Append mode writes at the end.'}, {'unit': 4, 'q': 'Why close a file explicitly?', 'options': ['Release resources/flush output', 'Delete it', 'Rename it', 'Compile it'], 'answer': 0, 'explanation': 'Closing finalizes stream use and flushes pending output.'}, {'unit': 4, 'q': 'What does a stream error state help detect?', 'options': ['Read/write/open failures', 'Syntax highlighting', 'Inheritance', 'Templates'], 'answer': 0, 'explanation': 'Stream state flags help detect I/O failures.'}, {'unit': 5, 'q': 'Which block encloses code that may throw?', 'options': ['try', 'catch', 'throw', 'finally'], 'answer': 0, 'explanation': 'A try block encloses code to monitor for exceptions.'}, {'unit': 5, 'q': 'Which keyword raises an exception?', 'options': ['catch', 'throw', 'try', 'raise'], 'answer': 1, 'explanation': 'throw signals an exception.'}, {'unit': 5, 'q': 'Which block handles exceptions?', 'options': ['catch', 'try', 'switch', 'using'], 'answer': 0, 'explanation': 'catch handles matching thrown exceptions.'}, {'unit': 5, 'q': 'What does catch(...) mean?', 'options': ['Catch any exception type', 'Catch integers only', 'Rethrow automatically', 'No exceptions'], 'answer': 0, 'explanation': 'The ellipsis handler catches any exception type.'}, {'unit': 5, 'q': 'What is a function template?', 'options': ['Generic function parameterized by types', 'Macro only', 'Virtual class', 'File function'], 'answer': 0, 'explanation': 'Function templates support type-generic functions.'}, {'unit': 5, 'q': 'Which keyword begins a template declaration?', 'options': ['generic', 'template', 'typename only', 'class only'], 'answer': 1, 'explanation': 'template begins a template declaration.'}, {'unit': 5, 'q': 'What can typename introduce?', 'options': ['A type template parameter', 'A file', 'A loop', 'An exception'], 'answer': 0, 'explanation': 'typename is commonly used for type template parameters.'}, {'unit': 5, 'q': 'What is a class template?', 'options': ['Class parameterized by types/values', 'Class without members', 'Abstract class only', 'Friend class only'], 'answer': 0, 'explanation': 'Class templates define families of classes.'}, {'unit': 5, 'q': 'What is a non-type template parameter?', 'options': ['Compile-time value parameter', 'Only a class name', 'Runtime input', 'Exception type only'], 'answer': 0, 'explanation': 'Non-type parameters are compile-time values such as an integer.'}, {'unit': 5, 'q': 'What is template argument deduction?', 'options': ['Compiler infers template arguments', 'User enters runtime value', 'Linker finds file', 'Object copies class'], 'answer': 0, 'explanation': 'The compiler can infer template arguments from function call arguments.'}, {'unit': 5, 'q': 'Which standard exception represents out-of-range access?', 'options': ['std::out_of_range', 'std::cout', 'std::vector', 'std::ifstream'], 'answer': 0, 'explanation': 'std::out_of_range is a standard exception type.'}, {'unit': 5, 'q': 'Why catch exceptions by const reference?', 'options': ['Avoid copying and preserve polymorphism', 'Make exception mutable', 'Hide type', 'Always faster compile'], 'answer': 0, 'explanation': 'const reference avoids slicing/copying and supports polymorphic exceptions.'}, {'unit': 5, 'q': 'What is rethrow syntax?', 'options': ['throw;', 'throw null', 'catch;', 'raise()'], 'answer': 0, 'explanation': 'A bare throw inside a handler rethrows the current exception.'}, {'unit': 5, 'q': 'Can a template support multiple types?', 'options': ['Yes', 'No', 'Only int', 'Only classes'], 'answer': 0, 'explanation': 'Templates can have multiple template parameters.'}, {'unit': 5, 'q': 'What should happen after a resource acquisition failure?', 'options': ['Handle/report failure appropriately', 'Ignore it always', 'Return random data', 'Disable exceptions'], 'answer': 0, 'explanation': 'Handle failure so the program remains correct and clear.'}, {'unit': 6, 'q': 'What does STL stand for?', 'options': ['Standard Template Library', 'System Type Language', 'Simple Text Library', 'Standard Transfer Logic'], 'answer': 0, 'explanation': 'STL is the Standard Template Library.'}, {'unit': 6, 'q': 'Which is a sequence container?', 'options': ['vector', 'map', 'set', 'unordered_set'], 'answer': 0, 'explanation': 'vector is a sequence container.'}, {'unit': 6, 'q': 'Which container stores key-value pairs ordered by key?', 'options': ['map', 'vector', 'queue', 'forward_list'], 'answer': 0, 'explanation': 'map stores unique keys with associated values in key order.'}, {'unit': 6, 'q': 'Which container allows duplicate sorted keys?', 'options': ['multiset', 'set', 'unordered_set', 'array'], 'answer': 0, 'explanation': 'multiset allows duplicate keys and maintains ordering.'}, {'unit': 6, 'q': 'Which container is typically hash-based?', 'options': ['unordered_map', 'map', 'set', 'deque'], 'answer': 0, 'explanation': 'unordered_map uses hashing and does not maintain sorted key order.'}, {'unit': 6, 'q': 'What is an iterator?', 'options': ['Object used to traverse container elements', 'A class constructor', 'A file mode', 'An exception'], 'answer': 0, 'explanation': 'Iterators provide a common way to access container elements.'}, {'unit': 6, 'q': 'Which algorithm sorts a range?', 'options': ['std::sort', 'std::find', 'std::count', 'std::copy'], 'answer': 0, 'explanation': 'std::sort sorts a range with random-access iterators.'}, {'unit': 6, 'q': 'Which algorithm searches for a value linearly?', 'options': ['std::find', 'std::sort', 'std::copy', 'std::swap'], 'answer': 0, 'explanation': 'std::find searches a range for a matching value.'}, {'unit': 6, 'q': 'Which container is dynamically resizable?', 'options': ['vector', 'array', 'pair', 'tuple'], 'answer': 0, 'explanation': 'vector can grow and shrink dynamically.'}, {'unit': 6, 'q': 'Which container provides double-ended insertion/removal?', 'options': ['deque', 'set', 'map', 'stack only'], 'answer': 0, 'explanation': 'deque supports efficient operations at both ends.'}, {'unit': 6, 'q': 'Which is a container adapter?', 'options': ['queue', 'vector', 'map', 'set'], 'answer': 0, 'explanation': 'queue is a container adapter.'}, {'unit': 6, 'q': 'What does std::count do?', 'options': ['Counts matching values', 'Sorts values', 'Copies range', 'Reverses file'], 'answer': 0, 'explanation': 'std::count counts occurrences of a value in a range.'}, {'unit': 6, 'q': 'What does std::copy do?', 'options': ['Copies a range', 'Sorts range', 'Searches key', 'Removes duplicates'], 'answer': 0, 'explanation': 'std::copy copies elements from one range to another.'}, {'unit': 6, 'q': 'What does std::array represent?', 'options': ['Fixed-size sequence container', 'Hash map', 'Linked queue', 'Exception'], 'answer': 0, 'explanation': 'std::array is a fixed-size array container.'}, {'unit': 6, 'q': 'Which header declares vector?', 'options': ['<vector>', '<map>', '<fstream>', '<exception>'], 'answer': 0, 'explanation': 'Include <vector> for std::vector.'}]

SNIPPETS = [
    {"title": "Class and object", "unit": 1, "code": "#include <iostream>\n#include <string>\nusing namespace std;\n\nclass Student {\npublic:\n    string name;\n    void introduce() { cout << \"Hello, \" << name << endl; }\n};\n\nint main() {\n    Student s;\n    s.name = \"Asha\";\n    s.introduce();\n    return 0;\n}"},
    {"title": "Constructor example", "unit": 1, "code": "#include <iostream>\nusing namespace std;\n\nclass Box {\n    int width;\npublic:\n    Box() : width(0) {}\n    Box(int w) : width(w) {}\n    void show() { cout << width << endl; }\n};\n\nint main() { Box a; Box b(5); a.show(); b.show(); }"},
    {"title": "Inheritance", "unit": 2, "code": "#include <iostream>\nusing namespace std;\n\nclass Animal {\npublic:\n    void eat() { cout << \"Eating\\n\"; }\n};\nclass Dog : public Animal {\npublic:\n    void bark() { cout << \"Barking\\n\"; }\n};\nint main() { Dog d; d.eat(); d.bark(); }"},
    {"title": "Function template", "unit": 5, "code": "#include <iostream>\nusing namespace std;\n\ntemplate <typename T>\nT bigger(T a, T b) { return (a > b) ? a : b; }\n\nint main() {\n    cout << bigger(4, 9) << endl;\n    cout << bigger(2.5, 1.5) << endl;\n}"},
    {"title": "Read a text file", "unit": 4, "code": "#include <fstream>\n#include <iostream>\n#include <string>\nusing namespace std;\n\nint main() {\n    ifstream file(\"notes.txt\");\n    if (!file) { cerr << \"Could not open file\\n\"; return 1; }\n    string line;\n    while (getline(file, line)) cout << line << endl;\n}"},
]


# Focused definitions fix common beginner questions and are available without an API key.
QA.extend([
 {"keys":["founder of c++","who created c++","who invented c++"],"question":"Who is the founder of C++?","answer":"Bjarne Stroustrup created C++. He began developing it in 1979 at Bell Labs, building on the C language and adding object-oriented features. The language was initially called “C with Classes” and was renamed C++ in 1983."},
 {"keys":["history of c++","brief history of c++","when was c++ created"],"question":"What is the history of C++?","answer":"Bjarne Stroustrup began developing C++ at Bell Labs in 1979 as “C with Classes,” combining C’s efficiency with object-oriented programming ideas. It was renamed C++ in 1983. The first ISO standard was published in 1998 (C++98), followed by major standards including C++11, C++14, C++17, C++20 and C++23."},
 {"keys":["operator overloading","what is operator","overload operator"],"question":"What is operator overloading?","answer":"Operator overloading lets a user-defined type specify what an existing C++ operator (such as +, -, ==, or ++) means for its objects. For example, Complex operator+(const Complex& rhs) const can return a new Complex containing the sums of the real and imaginary parts. It does not create new operators or change precedence; at least one operand must be a user-defined type."},
 {"keys":["function overloading","what is function overloading"],"question":"What is function overloading?","answer":"Function overloading means declaring multiple functions with the same name but different parameter lists (different number, types, or order of parameters). Example: int add(int a,int b); double add(double a,double b); int add(int a,int b,int c); The compiler chooses an overload from the call arguments. Return type alone cannot distinguish overloads. It is compile-time polymorphism."},
 {"keys":["difference between overloading and overriding","overloading vs overriding"],"question":"Overloading vs overriding","answer":"Overloading: same function name, different parameter lists, usually resolved at compile time; it can occur in one scope. Overriding: a derived class provides a matching implementation of a virtual base-class function, enabling runtime dispatch through a base pointer/reference. Use override in the derived class so the compiler checks the signature."},
 {"keys":["what is docker","docker in project","use docker"],"question":"What is Docker and how is it used here?","answer":"Docker packages the Flask app and its dependencies into a reproducible container. From the project folder run: docker compose up --build, then open http://localhost:5000. Copy .env.example to .env and put your API key there only if you want AI answers. Never commit or share .env. Docker must be installed and running first."},
 {"keys":["api key","openai api","ai enabled"],"question":"How do I enable AI answers?","answer":"Create your own API key in your AI provider account, copy .env.example to .env, and set OPENAI_API_KEY=your_key and optionally OPENAI_MODEL=gpt-4.1-mini. Restart Flask (or Docker Compose). API usage may cost money. Keep the key on the server in .env; never paste it into HTML/JavaScript or share it publicly."},
 {"keys":["c language","python code","java code","programming languages"],"question":"Which languages are supported?","answer":"The Code Examples tab includes beginner examples in C++, C, Java, and Python. Select a language filter to focus the list. Concepts can differ between languages—for example, C has no classes or operator overloading like C++."},
])

def normalize(text):
    return re.sub(r"[^a-z0-9+#]+", " ", (text or "").lower()).strip()


def answer_question(question, history=None):
    """Answer exact curated questions locally, then use the AI tutor for open-ended questions."""
    normalized = normalize(question)
    if not normalized:
        return {"answer": "Ask me anything about C++, OOP, programming concepts, debugging, algorithms, or your syllabus.", "source": "CodeBuddy"}

    # Open-ended questions go to the model before broad topic/bank matches. This avoids
    # returning an unrelated bank item just because it shares one or two words.
    # Prefer Groq when configured (fast OpenAI-compatible API); OpenAI remains optional fallback.
    groq_key = os.getenv("GROQ_API_KEY", "").strip()
    openai_key = os.getenv("OPENAI_API_KEY", "").strip()
    if groq_key or openai_key:
        try:
            from openai import OpenAI
            if groq_key:
                client = OpenAI(
                    api_key=groq_key,
                    base_url="https://api.groq.com/openai/v1",
                    timeout=45.0,
                    max_retries=1,
                )
                model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile").strip()
                source_label = "Groq AI"
            else:
                client = OpenAI(api_key=openai_key, timeout=45.0, max_retries=1)
                model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini").strip()
                source_label = "OpenAI tutor"

            messages = [{
                "role": "system",
                "content": (
                    "You are CodeBuddy, an expert, patient, conversational programming tutor. "
                    "Answer the user's actual question directly and naturally; do not require exact keywords "
                    "or claim that a question is outside a local study bank. Handle follow-up questions using "
                    "conversation history. Prioritize C++, object-oriented programming, the ADPC303 S.Y. B.Tech "
                    "syllabus, C, Java, Python, debugging, algorithms, and practical/lab work, but answer general "
                    "questions too when appropriate. For code requests, provide a correct, complete, compilable "
                    "example in the language requested, then explain important lines and show expected output. "
                    "For C++ use standard C++ and prefer std:: qualification in beginner examples. Keep answers "
                    "engaging, structured, beginner-friendly, and visually scannable. For requests such as "
                    "'explain in detail', teach like an excellent interactive tutor rather than a plain textbook. "
                    "Use a useful title and numbered sections when appropriate: definition, intuitive real-life "
                    "analogy, syntax, a relevant example or simple diagram, complete C++ program, expected output, "
                    "step-by-step walkthrough, types or comparisons when relevant, advantages, common mistakes, "
                    "quick revision, and an exam-ready conclusion. Adapt the length to the question: simple questions "
                    "should stay concise, while detailed questions should be comprehensive. Use Markdown headings, "
                    "real **bold emphasis**, bullet lists, tables only when useful, and fenced code blocks with language "
                    "labels. Never output visible raw Markdown markers as if they were plain text; the frontend renders "
                    "Markdown. Keep the explanation lively with relatable examples, small conceptual diagrams made "
                    "with text when useful, and practical takeaways; avoid filler, excessive emojis, and repetitive "
                    "sections. When explaining inheritance, cover the relevant inheritance types and show code/output "
                    "where useful. For any topic, select sections that genuinely fit the question instead of forcing "
                    "every section into every answer. "
                    "When the user asks for code, a program, an example, implementation, or output, provide the "
                    "complete requested code, then a brief explanation and sample output. Do not answer a code "
                    "request with only a definition. If the user asks a simple request like Hello World, answer "
                    "it directly without overexplaining. "
                    "Never invent sources or claim code was executed."
                )
            }]
            if isinstance(history, list):
                for turn in history[-8:]:
                    if not isinstance(turn, dict):
                        continue
                    role = turn.get("role")
                    content = turn.get("content")
                    if role in ("user", "assistant") and isinstance(content, str) and content.strip():
                        messages.append({"role": role, "content": content[:3000]})
            messages.append({"role": "user", "content": question})
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.4,
                max_tokens=1800,
            )
            answer = response.choices[0].message.content if response.choices else ""
            if answer and answer.strip():
                return {"answer": answer.strip(), "source": source_label}
            ai_error = "The AI tutor returned an empty response. Please try again."
        except Exception as exc:
            error_type = type(exc).__name__
            status = getattr(exc, "status_code", None)
            raw_message = str(exc)
            print(f"CodeBuddy AI request failed: provider={'Groq' if groq_key else 'OpenAI'}, type={error_type}, status={status}, message={raw_message[:400]}")
            diagnostic = raw_message.lower()
            if status == 401 or "invalid_api_key" in diagnostic or "authentication" in error_type.lower():
                ai_error = "Groq/OpenAI rejected the API key. Check the key in your project .env file and make sure it is active."
            elif status == 429 or "rate_limit" in diagnostic or "quota" in diagnostic:
                ai_error = "The AI provider rate limit or quota was reached. Wait and retry, or check your provider dashboard and model limits."
            elif status == 404 or "model_not_found" in diagnostic:
                ai_error = "The selected AI model is unavailable to this key. Check GROQ_MODEL in .env against the models enabled for your account."
            elif "connection" in error_type.lower() or "timeout" in error_type.lower():
                ai_error = "CodeBuddy could not connect to the AI provider. Check your internet connection and try again."
            else:
                ai_error = f"The AI request failed ({error_type}). Check the Flask terminal for details."
    else:
        ai_error = None

    # Keep curated syllabus answers as a fallback when the AI is not configured or cannot answer.
    # When Groq is configured, it gets the first chance to answer, including code/example requests.
    candidates = []
    for item in QA:
        for key in item["keys"]:
            nk = normalize(key)
            if nk and (nk in normalized or normalized in nk and len(normalized) > 7):
                candidates.append((len(nk), item))
    if candidates:
        item = max(candidates, key=lambda x: x[0])[1]
        return {"answer": item["answer"], "source": "CodeBuddy study guide", "matched": item["question"]}

    # Free local retrieval: search all 1,000 curated study records without any API key.
    # Token overlap, phrase overlap, and fuzzy similarity make natural phrasing more forgiving.
    try:
        from difflib import SequenceMatcher
        with open(os.path.join(app.root_path, "data", "question_bank.json"), encoding="utf-8") as f:
            bank = json.load(f)

        stop_words = {"what", "is", "are", "the", "a", "an", "in", "on", "of", "for", "to", "and", "or", "how", "why", "when", "where", "can", "could", "please", "explain", "tell", "me", "about", "with", "does", "do", "difference", "between"}
        aliases = {
            "constructor": {"constructors", "initialize", "initialization", "parameterized", "copy constructor"},
            "destructor": {"destroy", "cleanup"},
            "polymorphism": {"overloading", "overriding", "virtual", "dynamic binding", "compile time", "runtime"},
            "inheritance": {"base class", "derived class", "parent class", "child class"},
            "file": {"fstream", "ifstream", "ofstream", "stream", "reading", "writing"},
            "exception": {"try", "catch", "throw", "error handling"},
            "template": {"generic programming", "function template", "class template"},
            "stl": {"standard template library", "vector", "map", "set", "iterator", "container"},
            "class": {"object", "member function", "data member", "access specifier"},
        }
        query_tokens = {w for w in normalized.split() if len(w) > 1 and w not in stop_words}
        expanded = set(query_tokens)
        for token in list(query_tokens):
            for root, related in aliases.items():
                if token == root or token in related:
                    expanded.add(root)
                    expanded.update(related)
        ranked = []
        for item in bank:
            qtext = normalize(item.get("question", ""))
            topic = normalize(item.get("topic", ""))
            atext = normalize(item.get("answer", ""))
            title_tokens = set((qtext + " " + topic).split())
            answer_tokens = set(atext.split())
            overlap = len(expanded & title_tokens)
            answer_overlap = len(query_tokens & answer_tokens)
            phrase_bonus = 2.5 if normalized and (normalized in qtext or qtext in normalized) else 0
            fuzzy = SequenceMatcher(None, normalized, qtext).ratio()
            score = overlap * 2.0 + answer_overlap * 0.25 + phrase_bonus + fuzzy
            if item.get("topic", "").lower() in normalized:
                score += 1.5
            ranked.append((score, item))
        ranked.sort(key=lambda pair: pair[0], reverse=True)
        if ranked and ranked[0][0] >= 2.0:
            best_score, best = ranked[0]
            # Avoid overclaiming when a query is too broad; present a few related topics.
            if best_score >= 4.0 or len(query_tokens) <= 2:
                related_items = []
                for score, item in ranked[1:]:
                    if score >= 2.0 and item.get("question") != best.get("question"):
                        related_items.append(item.get("question", ""))
                    if len(related_items) == 2:
                        break
                answer = best.get("answer", "")
                if related_items:
                    answer += "\n\n**Related questions you can ask:**\n" + "\n".join("- " + q for q in related_items)
                return {"answer": answer, "source": "Free local study bank", "matched": best.get("question", "")}
    except (OSError, ValueError, TypeError, ImportError):
        pass

    # Friendly free-mode response: no payment details or API key are required.
    suggestions = ["Explain constructors with a C++ example", "Difference between overloading and overriding", "Write a program for inheritance", "Explain try, catch and throw", "How do vectors and iterators work in STL"]
    return {
        "answer": (
            "I couldn't find a reliable answer in CodeBuddy's offline study bank for that exact wording. "
            "CodeBuddy is running in free local mode, so no API key or payment details are needed. "
            "Try asking with a C++ topic or a more specific phrase.\n\n**Try one of these:**\n" +
            "\n".join("- " + suggestion for suggestion in suggestions)
        ),
        "source": "Free local tutor"
    }


@app.get("/api/questions")
def question_bank():
    path = os.path.join(app.root_path, "data", "question_bank.json")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    query = request.args.get("q", "").strip().lower()
    limit = min(max(int(request.args.get("limit", "100")), 1), 1000)
    if query:
        data = [x for x in data if query in x["question"].lower() or query in x["answer"].lower() or query in x.get("topic", "").lower()]
    return jsonify({"total": len(data), "questions": data[:limit]})

@app.get("/api/examples")
def examples():
    path = os.path.join(app.root_path, "data", "code_examples.json")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    # The Code Examples view is C++-first; each example carries alternate-language versions.
    language = request.args.get("language", "C++").lower()
    if language in ("all", "c++"):
        data = [x for x in data if x["language"].lower() == "c++"]
    else:
        data = [x for x in data if x["language"].lower() == language]
    return jsonify(data)

@app.get("/")
def home():
    with open(os.path.join(app.root_path, "data", "code_examples.json"), encoding="utf-8") as f:
        all_snippets = json.load(f)
    return render_template("index.html", units=UNITS, practicals=PRACTICALS, snippets=all_snippets)

@app.get("/api/health")
def health():
    groq_key = os.getenv("GROQ_API_KEY", "").strip()
    openai_key = os.getenv("OPENAI_API_KEY", "").strip()
    return jsonify({
        "status": "ok",
        "ai_enabled": bool(groq_key or openai_key),
        "provider": "Groq" if groq_key else ("OpenAI" if openai_key else "Local study bank"),
        "model": (os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile") if groq_key else os.getenv("OPENAI_MODEL", "gpt-4.1-mini")).strip(),
        "key_configured": bool(groq_key or openai_key)
    })

@app.post("/api/chat")
def chat():
    payload = request.get_json(silent=True) or {}
    question = str(payload.get("message", "")).strip()[:2000]
    if not question:
        return jsonify({"error": "Please type a question first."}), 400
    history = payload.get("history", [])
    return jsonify(answer_question(question, history=history))

@app.get("/api/quiz")
def quiz():
    # Six unit-wise quizzes, 15 questions per unit. Answers stay server-side until grading.
    unit = request.args.get("unit", "1")
    try: unit = int(unit)
    except ValueError: unit = 1
    selected = [q for q in QUIZ if q["unit"] == unit]
    return jsonify([{ "id": i, "q": q["q"], "options": q["options"] } for i, q in enumerate(selected)])

@app.post("/api/quiz/grade")
def grade_quiz():
    payload = request.get_json(silent=True) or {}
    answers = payload.get("answers", {})
    try: unit = int(payload.get("unit", 1))
    except (ValueError, TypeError): unit = 1
    selected_quiz = [q for q in QUIZ if q["unit"] == unit]
    results = []
    score = 0
    for i, q in enumerate(selected_quiz):
        selected = answers.get(str(i))
        correct = selected == q["answer"]
        score += int(correct)
        results.append({"id": i, "correct": correct, "answer": q["answer"], "explanation": q["explanation"]})
    return jsonify({"score": score, "total": len(QUIZ), "results": results})

@app.route("/api/interview/questions")
def interview_questions():
    """Return the C++ OOP interview questions bundled with CodeBuddy."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "interview_questions.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            questions = json.load(f)
        if not isinstance(questions, list):
            raise json.JSONDecodeError("Expected a list of questions", "", 0)
        return jsonify(questions)
    except (OSError, json.JSONDecodeError) as exc:
        app.logger.exception("Could not load interview questions: %s", exc)
        return jsonify({"error": "Interview question bank could not be loaded."}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
