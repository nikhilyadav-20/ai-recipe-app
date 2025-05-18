import pandas as pd
import spacy

nlp = spacy.load("en_core_web_sm")

# Extract the main dish/ingredient from user input
def extract_food(user_input):
    doc = nlp(user_input)
    for chunk in doc.noun_chunks:
        return chunk.text
    return user_input

# Return matching recipe(s) with step-by-step instructions, visuals, and extras
def find_recipe(food, dataset_path='recipes.csv'):
    df = pd.read_csv(dataset_path)
    matches = df[df['title'].str.contains(food, case=False, na=False)]

    if matches.empty:
        return "❌ Sorry, no recipe found for that food."

    result = ""
    for _, recipe in matches.iterrows():
        # Break instructions into numbered steps
        raw_steps = recipe['instructions'].replace('.', '.|').split('|')
        steps = [step.strip() for step in raw_steps if step.strip()]
        step_text = '\n'.join([f"{i+1}. {s}" for i, s in enumerate(steps)])

        # Build the full display block
        result += f"""### 🍽️ {recipe['title']}

**🧂 Ingredients:**  
{recipe['ingredients']}

**🕒 Time:** {recipe['time']}  
**🔥 Difficulty:** {recipe['difficulty']}

**📋 Step-by-Step Instructions:**  
{step_text}

"""
        # Add image if present
        if 'image_url' in recipe and pd.notna(recipe['image_url']):
            result += f"![{recipe['title']}]({recipe['image_url']})\n\n"

        # Add video if present
        if 'video_url' in recipe and pd.notna(recipe['video_url']):
            result += f"[📺 Watch Tutorial Video]({recipe['video_url']})\n\n"

        result += "---\n"

    return result
