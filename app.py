import streamlit as st
import pandas as pd
import os

# ✅ Load dataset safely
file_path = os.path.join(os.getcwd(), "recipe_dataset.xlsx.csv")

try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    st.error(f"❌ File not found: {file_path}")
    st.stop()

st.title("🍲 AI Recipe Recommender")
st.write("Enter ingredients and get a full, easy-to-cook recipe suggestion!")

# 🧂 User input
user_input = st.text_input("Enter ingredients (comma separated):")

def recommend_recipe(user_ingredients):
    user_ingredients = [i.strip().lower() for i in user_ingredients.split(',')]
    
    def contains_ingredients(ingredients):
        ingredients_list = [i.strip().lower() for i in ingredients.split(',')]
        return any(item in ingredients_list for item in user_ingredients)
    
    filtered = df[df['Ingredients'].apply(contains_ingredients)]
    if filtered.empty:
        return None
    return filtered.iloc[0]

def generate_recipe_text(recipe):
    ingredients = recipe['Ingredients'].split(', ')
    method = recipe['Cooking_Method']
    steps = []

    if method.lower() in ['baking', 'roasting', 'grilling']:
        steps.append(f"1. Preheat your oven or grill for {method.lower()}.")
        steps.append(f"2. Prepare all ingredients: {', '.join(ingredients)}.")
        steps.append(f"3. {method.capitalize()} the ingredients until golden and cooked through.")
        steps.append(f"4. Serve hot with your favorite side or sauce.")
    elif method.lower() in ['sauteing', 'stir-frying']:
        steps.append(f"1. Heat a pan with a little oil.")
        steps.append(f"2. Add ingredients: {', '.join(ingredients)} and {method.lower()} for 5–7 minutes.")
        steps.append(f"3. Garnish and serve warm.")
    else:
        steps.append(f"1. Prepare: {', '.join(ingredients)}.")
        steps.append(f"2. Cook using {method.lower()} method until done.")
        steps.append("3. Serve and enjoy your meal!")

    return steps

# 🧑‍🍳 Generate recipe
if user_input:
    recipe = recommend_recipe(user_input)
    
    if recipe is not None:
        st.subheader("🍽️ Recipe Recommendation")
        st.write(f"**Recipe ID:** {recipe['Recipe_ID']}")
        st.write(f"**Cuisine:** {recipe['Cuisine']}")
        st.write(f"**Ingredients:** {recipe['Ingredients']}")
        st.write(f"**Cooking Method:** {recipe['Cooking_Method']}")
        st.write(f"**Difficulty:** {recipe['Difficulty']}")
        st.write(f"**Serving Size:** {recipe['Serving_Size']}")
        
        st.markdown("### 👨‍🍳 Cooking Steps")
        for step in generate_recipe_text(recipe):
            st.write(step)
    else:
        st.warning("No matching recipe found for these ingredients.")
