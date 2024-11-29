from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = "distilgpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def generate_feedback(prompt):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(inputs["input_ids"], max_length=100)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def generate_trend_analysis(data):
    prompt = f"Analyze the trends for {data['time_period']} period: {data['sales']}"
    return generate_feedback(prompt)
