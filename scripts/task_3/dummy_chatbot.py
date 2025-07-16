import gradio as gr
import random

# Simple responses for the dummy chatbot
responses = [
    "Hello! How can I help you today?",
    "That's interesting! Tell me more.",
    "I'm here to chat with you!",
    "Thanks for sharing that with me.",
    "I'm a simple chatbot, but I'm happy to talk!",
    "That's a great question!",
    "I'm learning from our conversation.",
    "Feel free to ask me anything!",
    "I'm here to assist you.",
    "What would you like to know?",
]


def chatbot_response(message, history):
    """Generate a response for the chatbot"""
    if not message.strip():
        return "Please say something!"

    # Simple logic: use random responses for now
    response = random.choice(responses)

    # Add some basic pattern matching for common greetings
    message_lower = message.lower()
    if any(
        greeting in message_lower
        for greeting in ["hello", "hi", "hey", "good morning", "good afternoon"]
    ):
        response = "Hello! Nice to meet you! How are you doing today?"
    elif any(word in message_lower for word in ["how are you", "how do you do"]):
        response = "I'm doing great, thank you for asking! How about you?"
    elif any(
        word in message_lower for word in ["bye", "goodbye", "see you", "farewell"]
    ):
        response = "Goodbye! It was nice chatting with you. Have a great day!"
    elif "?" in message:
        response = "That's a good question! I'm a simple chatbot, so my responses are quite basic."

    return response


# Create the Gradio interface
def create_chatbot():
    with gr.Blocks(title="Basic Chatbot") as demo:
        gr.Markdown("# 🤖 Basic Chatbot")
        gr.Markdown("Welcome! I'm a simple chatbot. Feel free to chat with me!")

        chatbot = gr.Chatbot(height=400, show_label=False, container=True)

        with gr.Row():
            msg = gr.Textbox(
                placeholder="Type your message here...",
                show_label=False,
                container=False,
                scale=4,
            )
            submit_btn = gr.Button("Send", variant="primary", scale=1)

        clear = gr.Button("Clear Chat", variant="secondary")

        def respond(message, chat_history):
            bot_message = chatbot_response(message, chat_history)
            chat_history.append((message, bot_message))
            return "", chat_history

        # Connect both textbox submit and button click
        msg.submit(respond, [msg, chatbot], [msg, chatbot])
        submit_btn.click(respond, [msg, chatbot], [msg, chatbot])
        clear.click(lambda: None, None, chatbot, queue=False)

    return demo


if __name__ == "__main__":
    demo = create_chatbot()
    demo.launch(server_name="0.0.0.0", server_port=7860, share=True, debug=False)
