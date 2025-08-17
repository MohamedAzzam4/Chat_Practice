# Language Practice Tutor API

This project is a FastAPI-based API that provides a conversational AI language tutor named "Ahmed". The primary goal of this API is to help users practice a new language in a comfortable, low-pressure, and natural conversational environment, focusing on building confidence over perfection.

## ✨ Features

-   **Conversational AI Tutor**: Engage in a natural, back-and-forth conversation with an AI tutor persona.
-   **Dynamic Persona**: The tutor, Ahmed, has his own interests (photography, hiking, coffee) to make conversations more engaging.
-   **Adaptive Difficulty**: The tutor adjusts its vocabulary and sentence complexity based on the user's stated proficiency level (A1-C2).
-   **Stateless API Design**: The API is stateless, meaning the entire chat history is passed with each request, simplifying deployment and scalability.
-   **Encouraging & Patient**: Designed to be a patient and encouraging partner, prioritizing conversational flow.

## 🛠️ Technology Stack

-   **Backend**: Python 3.9+
-   **Framework**: FastAPI
-   **Data Validation**: Pydantic
-   **LLM Integration**: OpenAI-compatible API
-   **Server**: Uvicorn

## 🚀 Getting Started

Follow these instructions to get the project up and running on your local machine.

### Prerequisites

-   Python 3.9 or higher
-   `pip` package manager

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/MohamedAzzam4/Chat_Practice](https://github.com/MohamedAzzam4/Chat_Practice)
    cd your-repository-name
    ```

2.  **Create and activate a virtual environment:**
    - On macOS/Linux:
      ```bash
      python3 -m venv venv
      source venv/bin/activate
      ```
    - On Windows:
      ```bash
      python -m venv venv
      .\venv\Scripts\activate
      ```

3.  **Install the required dependencies:**
    First, create a `requirements.txt` file with the following content:
    ```txt
    fastapi
    uvicorn[standard]
    python-dotenv
    openai
    ```
    Then, install them using pip:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    Create a file named `.env` in the root directory of the project and add your API key:
    ```
    ROUTER_API_KEY="your_api_key_here"
    ```

### Running the API

To run the application locally, use the following command:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
The `--reload` flag enables auto-reloading for development. For production, you can remove it. The API will be available at `http://127.0.0.1:8000`.

##  kullanım API Usage

The API has one main endpoint to handle the chat.

### `/chat`

-   **Method**: `POST`
-   **Description**: Sends a user message and the conversation history to the tutor and gets a response.

#### Request Body

The request body must be a JSON object with the following structure:

```json
{
  "target_language": "Spanish",
  "user_level": "B1",
  "user_message": "Hola, como estas?",
  "chat_history": []
}
```
* `chat_history`: For the first message, send an empty list `[]`. For subsequent messages, send the `updated_chat_history` received from the previous response.

#### Example Response

```json
{
  "tutor_response": "¡Hola! Estoy muy bien, gracias. Justo estaba pensando en tomar un café. ¿Y tú, qué tal tu día?",
  "updated_chat_history": [
    {
      "role": "system",
      "content": "..."
    },
    {
      "role": "user",
      "content": "Hola, como estas?"
    },
    {
      "role": "assistant",
      "content": "¡Hola! Estoy muy bien, gracias. Justo estaba pensando en tomar un café. ¿Y tú, qué tal tu día?"
    }
  ]
}
```

## 📝 Future Development

-   **Smarter Correction Logic**: Implementing a dual-agent system where one agent focuses on conversation while a separate, silent agent analyzes errors and provides structured feedback.
-   **Dockerization**: Containerizing the application with Docker for easier deployment and environment consistency.
