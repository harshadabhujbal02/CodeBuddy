#include <iostream>
#include <string>
#include <cctype>

using namespace std;

int main()
{
    string question;

    cout << "========================================" << endl;
    cout << "        OOP STUDY CHATBOT" << endl;
    cout << "========================================" << endl;
    cout << "Bot: Hello! I am your OOP Study Chatbot." << endl;
    cout << "Bot: Ask me an OOP question." << endl;
    cout << "Bot: Type 'bye' to exit." << endl;

    while (true)
    {
        cout << "\nYou: ";
        getline(cin, question);

        // Convert the question into lowercase
        for (char &c : question)
        {
            c = tolower(c);
        }

        // Exit the chatbot
        if (question == "bye")
        {
            cout << "Bot: Thank you for using OOP Study Chatbot!" << endl;
            break;
        }

        // OOP
        else if (question == "what is oop" || question == "what is oop?")
        {
            cout << "Bot: OOP stands for Object-Oriented Programming." << endl;
            cout << "Bot: It is a programming approach based on classes and objects." << endl;
        }

        // Class
        else if (question == "what is a class" || question == "what is a class?")
        {
            cout << "Bot: A class is a blueprint or template used to create objects." << endl;
        }

        // Object
        else if (question == "what is an object" || question == "what is an object?")
        {
            cout << "Bot: An object is an instance of a class." << endl;
        }

        // Encapsulation
        else if (question == "what is encapsulation" || question == "what is encapsulation?")
        {
            cout << "Bot: Encapsulation is the process of combining data and functions into a single unit." << endl;
        }

        // Inheritance
        else if (question == "what is inheritance" || question == "what is inheritance?")
        {
            cout << "Bot: Inheritance allows one class to acquire the properties and functions of another class." << endl;
        }

        // Polymorphism
        else if (question == "what is polymorphism" || question == "what is polymorphism?")
        {
            cout << "Bot: Polymorphism means one name having multiple forms." << endl;
        }

        // Abstraction
        else if (question == "what is abstraction" || question == "what is abstraction?")
        {
            cout << "Bot: Abstraction means hiding unnecessary implementation details and showing only essential information." << endl;
        }

        // Constructor
        else if (question == "what is a constructor" || question == "what is a constructor?")
        {
            cout << "Bot: A constructor is a special member function that is automatically called when an object is created." << endl;
        }

        // Destructor
        else if (question == "what is a destructor" || question == "what is a destructor?")
        {
            cout << "Bot: A destructor is a special member function that is automatically called when an object is destroyed." << endl;
        }

        // Function overloading
        else if (question == "what is function overloading" || question == "what is function overloading?")
        {
            cout << "Bot: Function overloading means defining multiple functions with the same name but different parameters." << endl;
        }

        // Function overriding
        else if (question == "what is function overriding" || question == "what is function overriding?")
        {
            cout << "Bot: Function overriding occurs when a derived class provides its own implementation of a base class function." << endl;
        }

        // Unknown question
        else
        {
            cout << "Bot: Sorry, I don't know that question yet." << endl;
        }
    }

    return 0;
}