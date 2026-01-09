import gradio as gr
import re
from langgraph_models.financial_advisor import get_financial_advice
from langgraph_models.career_counsellor import get_career_advice
from langgraph_models.leadership_skills import get_leadership_advice

# Updated chatbot_mode function to prevent auto-response
def chatbot_mode(selected_mode, user_input):
    user_input_lower = user_input.strip().lower()

    # Detect simple greetings based on input patterns
    if len(user_input_lower.split()) < 3 and not re.search(r"[?!.]", user_input_lower):
        # If it's short and lacks punctuation like a question or exclamation, it may be a greeting
        return "Hello! How can I assist you today?"

    if not user_input:  # Check if user_input is empty
        return ""  # No response if input is empty

    # Process the input based on the selected mode
    if selected_mode == "Financial Advisor":
        return get_financial_advice(user_input)
    elif selected_mode == "Career Counsellor":
        return get_career_advice(user_input)
    elif selected_mode == "Leadership Skills":
        return get_leadership_advice(user_input)
    else:
        return "Invalid mode selected."

# Gradio interface logic
with gr.Blocks() as demo:
    gr.Markdown("### Orphanage Chatbot")
    
    # Dropdown to select the mode
    mode_selector = gr.Dropdown(
        choices=["Financial Advisor", "Career Counsellor", "Leadership Skills"],
        label="Select Mode"
    )
    
    # Textbox for user input
    user_input = gr.Textbox(label="Your Question")
    
    # Output textbox with increased size (height) for better visibility
    output = gr.Textbox(label="Chatbot Response", interactive=False, lines=5)  # Adjusted output size
    
    # Add a button to submit the user input
    submit_button = gr.Button("Submit Question")

    # Call chatbot_mode when dropdown or input changes
    submit_button.click(
        chatbot_mode, 
        inputs=[mode_selector, user_input], 
        outputs=output
    )

# Launch the Gradio app
demo.launch()
