import gradio as gr
import torch
from transformers import AutoTokenizer, DistilBertForSequenceClassification
import numpy as np

# Load tokenizer from base model
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

# Load the fine-tuned model using DistilBertForSequenceClassification directly
MODEL_PATH = "./takemeter-model/content/takemeter-model/checkpoint-27"
model = DistilBertForSequenceClassification.from_pretrained(MODEL_PATH)

# Label mapping (must match your LABEL_MAP)
ID_TO_LABEL = {0: "analysis", 1: "hot_take", 2: "reaction"}

def classify_post(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=256)
    with torch.no_grad():
        outputs = model(**inputs)
    probs = torch.nn.functional.softmax(outputs.logits, dim=-1).numpy()[0]
    pred_id = np.argmax(probs)
    label = ID_TO_LABEL[pred_id]
    confidence = float(probs[pred_id])
    return f"**Predicted Label:** {label}\n**Confidence:** {confidence:.2%}"

iface = gr.Interface(
    fn=classify_post,
    inputs=gr.Textbox(lines=5, placeholder="Enter a fantasy football post here..."),
    outputs=gr.Markdown(),
    title="TakeMeter - Fantasy Football Classifier",
    description="Classifies posts as **analysis**, **hot_take**, or **reaction** using the fine-tuned model."
)

iface.launch()