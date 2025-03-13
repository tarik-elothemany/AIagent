from flask import Flask, request, jsonify
import google.generativeai as genai
import os
import json
from datetime import datetime
from config import GOOGLE_API_KEY

# Initialize Flask app
app = Flask(__name__)

# Configure Google AI Model
genai.configure(api_key=GOOGLE_API_KEY)

# Directory to save optimized rules
RULES_DIR = "optimized_rules"

# Ensure the rules directory exists
if not os.path.exists(RULES_DIR):
    os.makedirs(RULES_DIR)

# Function to optimize rules using AI
def optimize_wazuh_rules(category, alerts, rules):
    """Uses AI to optimize Wazuh rules based on alert data."""
    prompt = f"""
    You are a cybersecurity AI expert. Given these **Wazuh rules** for category **{category}**:
    {rules}

    And the **recent security alerts**:
    {alerts}

    🔹 **Your Task:**
    - Identify overly sensitive rules causing false positives.
    - Identify weak rules that need stricter conditions.
    - Suggest **improvements** in XML format.

    🚀 **Output Format:**
    - List of **optimized Wazuh rules** in XML format.
    - Explanation of changes.
    """

    response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
    return response.text

# Function to save rules to a file
def save_rules_to_file(category, optimized_rules):
    """Saves AI-generated rules to a file for manual review."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{RULES_DIR}/optimized_rules_{category}_{timestamp}.xml"

    with open(filename, "w") as file:
        file.write(optimized_rules)

    print(f"✅ Optimized rules saved: {filename}")
    return filename

# Route to receive alerts and process them
@app.route("/process_alerts", methods=["POST"])
def process_alerts():
    """Receives grouped alerts from Wazuh, processes them, and saves optimized rules."""
    data = request.json

    if not data:
        return jsonify({"error": "No alert data received"}), 400

    saved_files = []
    
    for group in data:
        category = group["category"]
        alerts = group["alerts"]
        
        # Fake function to simulate fetching rules (replace with real Wazuh API call if needed)
        rules = [f"<rule id='{5710 + i}' level='10'><description>Rule for {category} event {i}</description></rule>" for i in range(3)]

        # Generate optimized rules using AI
        optimized_rules = optimize_wazuh_rules(category, alerts, rules)

        # Save optimized rules to a file
        file_path = save_rules_to_file(category, optimized_rules)
        saved_files.append(file_path)

    return jsonify({"message": "Alerts processed, rules saved.", "saved_files": saved_files}), 200

# Run Flask API
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
