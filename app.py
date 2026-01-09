import gradio as gr
import openai
import os
import re
from langgraph_models.financial_advisor import get_financial_advice
from langgraph_models.career_counsellor import get_career_advice
from langgraph_models.leadership_skills import get_leadership_advice
from dotenv import load_dotenv

load_dotenv()  # Load the API key from the .env file
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define chatbot_mode function for Gradio to interact with
def chatbot_mode(selected_mode, user_input, history):
    user_input_lower = user_input.strip().lower()

    # Detect simple greetings based on input patterns
    if len(user_input_lower.split()) < 3 and not re.search(r"[?!.]", user_input_lower):
        return "Hello! How can I assist you today?", history

    if not user_input:  # Check if user_input is empty
        return "", history  # No response if input is empty

    # Append user input to the history for persistence
    history.append(f"User: {user_input}")

    # Add system instructions for context
    if selected_mode == "Financial Advisor":
        history.append("System: You are a financial advisor for children.")
    elif selected_mode == "Career Counsellor":
        history.append("System: You are a career counselor for children.")
    elif selected_mode == "Leadership Skills":
        history.append("System: You are a leadership coach for children.")

    messages = [{"role": "system", "content": history[-1]}] + [{"role": "user", "content": user_input}]
    response = ""

    try:
        # OpenAI API call with streaming enabled
        for chunk in openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Use GPT-4o-mini
            messages=messages,
            temperature=0.7,
            max_tokens=300,
            stream=True  # Enable streaming
        ):
            # Extract content from the 'delta' field of the stream response
            if 'choices' in chunk:
                content = chunk['choices'][0].get('delta', {}).get('content', '')
                response += content
                yield response  # Stream response incrementally

    except Exception as e:
        print(f"Error during streaming: {e}")
        return "An error occurred while generating the response.", history

    # Append model response to history
    history.append(f"Assistant: {response}")
    return response, history  # Return both response and updated history

# Create Gradio interface function
def create_gradio_interface():
    with gr.Blocks() as demo:
        gr.Markdown("### Orphanage Chatbot")

        mode_selector = gr.Dropdown(
            choices=["Financial Advisor", "Career Counsellor", "Leadership Skills"],
            label="Select Mode"
        )

        user_input = gr.Textbox(label="Your Question", placeholder="Type your question here...")
        output = gr.Textbox(label="Chatbot Response", interactive=False, lines=5)  # Adjusted output size
        submit_button = gr.Button("Submit Question")

        state = gr.State([])  # Store conversation history

        submit_button.click(
            chatbot_mode,
            inputs=[mode_selector, user_input, state],
            outputs=[output, state],
        )

    return demo

# Launch Gradio interface directly without Flask
demo = create_gradio_interface()
demo.launch(share=True)  # This will make the app publicly accessible if needed
