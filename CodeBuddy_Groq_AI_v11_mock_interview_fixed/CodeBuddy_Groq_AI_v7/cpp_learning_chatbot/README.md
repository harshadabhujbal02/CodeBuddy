# CodeBuddy — AI-Powered Coding Companion

**Ask. Learn. Code. Grow.**

CodeBuddy is an AI-powered programming learning website designed to help students understand programming concepts, practice coding, and prepare for technical interviews. It provides interactive learning support with a focus on C++ programming and Object-Oriented Programming (OOP).

Built using Python Flask and the Groq API, CodeBuddy aims to make programming education more accessible through AI-generated explanations, code examples, and interview practice.

## Features

### 1. AI Programming Chatbot
- Ask programming-related questions in natural language.
- Get AI-generated explanations for programming concepts.
- Learn C++, Object-Oriented Programming, and other programming fundamentals.
- Understand concepts with examples and step-by-step explanations.

### 2. C++ Code Examples
- Explore common programming examples and concepts.
- Understand program structure, syntax, and implementation.
- Use examples to support practical coding and academic learning.

### 3. Multi-Language Learning
- Learn programming concepts across supported languages, including C++, C, Java, and Python.
- Compare how programming concepts are implemented in different languages where supported.

### 4. Mock Interview Practice
- Practice technical interview questions.
- Review questions related to OOP, inheritance, polymorphism, classes, objects, and other programming topics.
- Improve programming knowledge and interview preparation.

### 5. Study Resources
- Use available local question banks and study materials.
- Revise programming concepts and prepare for examinations and technical interviews.

### 6. Responsive Website
- Access the website through a modern web browser.
- Use the responsive interface on supported desktop and mobile devices.

## Technology Stack

| Component | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, Flask |
| AI Integration | Groq API |
| AI Model | Configurable through environment variables |
| Deployment | Render |
| Version Control | Git and GitHub |

## Project Structure

The project structure may vary depending on the version being used.

```text
CodeBuddy/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/
├── static/
└── data/
```

**Note:** The `data/` folder is an example. Include the actual question-bank or resource folders used by your project.

## Prerequisites

Before running CodeBuddy locally, install:

- Python 3.10 or a compatible version supported by the project dependencies
- pip (Python package installer)
- Git (optional for local setup, required for the Git workflow)
- A Groq API key

You can obtain an API key from the [Groq Console](https://console.groq.com/).

## Installation and Setup

### Step 1: Download the Project

Clone the GitHub repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Navigate into the project folder:

```bash
cd CodeBuddy
```

Alternatively, download the repository as a ZIP file and extract it.

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can run the project using the virtual environment's Python executable directly.

### Step 3: Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the same folder as `app.py`.

Add your own Groq API key and the model configured for your project:

```dotenv
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-120b
PORT=5000
```

Replace `your_groq_api_key` with your actual key. Use a model currently available to your Groq account.

**Security:** Never upload your `.env` file or expose your API key in frontend JavaScript, screenshots, or public repositories. Keep `.env` excluded through `.gitignore`.

### Step 5: Run the Application

```bash
python app.py
```

Open the website in your browser:

http://127.0.0.1:5000

Keep the terminal running while using the locally hosted website.

## Deployment

CodeBuddy can be deployed to a supported hosting platform such as Render.

General deployment steps:

1. Push the project files to GitHub.
2. Create a new web service on [Render](https://render.com/).
3. Connect your GitHub repository.
4. Set the build command to:

   ```bash
   pip install -r requirements.txt
   ```

5. Set the start command to:

   ```bash
   gunicorn app:app
   ```

6. Add `GROQ_API_KEY` and `GROQ_MODEL` under the service's environment variables.
7. Deploy the application and test its features.

**Deployment note:** The command `gunicorn app:app` assumes that the Flask application object is named `app` in `app.py`. Adjust it if your project uses a different name. Confirm that all required files and dependencies are included before deploying.

## Security and Best Practices

- Store API keys in environment variables.
- Never commit `.env` files or other secrets to GitHub.
- Keep dependencies documented in `requirements.txt`.
- Do not store sensitive user information unnecessarily.
- Test the chatbot and other features after every deployment.
- Check hosting limits and API usage limits before making the website publicly available.

## Future Enhancements

Potential improvements include:

- More comprehensive programming question banks.
- Additional coding exercises and quizzes.
- AI-assisted mock interview feedback.
- Improved code explanations and debugging assistance.
- Progress tracking and personalized learning paths.
- Additional programming languages and learning resources.

These are possible future improvements and are not necessarily implemented in the current version.

## Purpose of the Project

CodeBuddy aims to make programming easier to learn by combining AI-assisted explanations, practical code examples, and interview preparation in one accessible learning platform.

It is intended as a learning companion for students, beginners, and aspiring developers.

## Author

**Project:** CodeBuddy — AI-Powered Coding Companion

**Domain:** Programming Education and Interview Preparation

**Developed using:** Python, Flask, HTML, CSS, JavaScript, and Groq API
