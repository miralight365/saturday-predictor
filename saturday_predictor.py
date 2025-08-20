import streamlit as st
from collections import Counter
from itertools import combinations

st.title("🔮 Saturday Number Predictor")
st.write("Enter your weekday numbers to get predicted numbers for Saturday!")

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
days_data = {}

# Input fields for each day
for day in days:
    user_input = st.text_input(f"{day} numbers (comma-separated)", key=day)
    if user_input:
        try:
            days_data[day] = [int(x.strip()) for x in user_input.split(',') if x.strip().isdigit()]
        except:
            st.error(f"Invalid input for {day}. Please enter 5 comma-separated numbers.")

def analyze_and_predict(days_data, top_n=5):
    all_values = []
    for values in days_data.values():
        all_values.extend(values)

    freq_counter = Counter(all_values)
    most_common = freq_counter.most_common(top_n)

    all_diffs = []
    for a, b in combinations(all_values, 2):
        all_diffs.append(abs(a - b))
    diff_counter = Counter(all_diffs)
    common_diffs = diff_counter.most_common(top_n)

    seen = {}
    for day, numbers in days_data.items():
        for number in numbers:
            seen.setdefault(number, set()).add(day)
    repeating_numbers = [num for num, days in seen.items() if len(days) > 1]

    daily_averages = {day: sum(nums)//len(nums) for day, nums in days_data.items()}
    overall_average = sum(all_values) // len(all_values)

    predictions = set()
    predictions.update([num for num, _ in most_common])
    predictions.update([d for d, _ in common_diffs if 1 <= d <= 99])
    predictions.update(repeating_numbers)
    predictions.add(overall_average)
    predictions.update(daily_averages.values())

    predicted_numbers = sorted(list(predictions))[:10]

    return {
        "Most Common Numbers": most_common,
        "Common Differences": common_diffs,
        "Repeating Numbers": repeating_numbers,
        "Daily Averages": daily_averages,
        "Overall Average": overall_average,
        "Predicted Saturday Numbers": predicted_numbers
    }

# Predict Button
if st.button("🎯 Predict Saturday Numbers"):
    if all(len(v) == 5 for v in days_data.values()):
        results = analyze_and_predict(days_data)

        st.subheader("📊 Prediction Summary")
        for key, value in results.items():
            st.write(f"**{key}**: {value}")
    else:
        st.warning("Please enter 5 numbers for each weekday.")
