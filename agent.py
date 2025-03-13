import google.generativeai as genai
import os
from config import GOOGLE_API_KEY

#----------------------------------------------------------------------------------------------
# ✅ Set up Gemini AI Model (Google Generative AI)
genai.configure(api_key=GOOGLE_API_KEY)

#----------------------------------------------------------------------------------------------
# ✅ AI-Driven Wazuh Rule Optimization Function
def optimize_wazuh_rules(old_rules, weekly_alerts):
    """
    AI analyzes past Wazuh alerts and existing rules to generate improved detection rules.
    """
    # Check if inputs are valid
    if not old_rules or not weekly_alerts:
        return "⚠️ Error: No rules or alerts provided for optimization."

    # Construct the prompt for AI processing
    prompt = f"""
    You are a cybersecurity AI expert specializing in Wazuh XDR rules.

    Given the following **Wazuh rules**:
    {', '.join(old_rules)}

    And the **weekly security alerts triggered**:
    {', '.join(weekly_alerts)}

    🔹 **Your Task:**
    - Analyze which rules are **generating too many false positives**.
    - Identify **new attack patterns** that require stricter rules.
    - Suggest **rule improvements** (adjust severity, add new conditions).
    - If a rule is too broad, provide a **more specific version**.

    🚀 **Output Format:**
    - List of **optimized Wazuh rules** in XML format.
    - Explanation of why each rule was adjusted.
    """

    try:
        # Call Gemini AI model
        response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ AI Processing Error: {str(e)}"

#----------------------------------------------------------------------------------------------
# ✅ Run the AI Optimization Process
if __name__ == "__main__":
    print("\n🚀 Starting AI-Driven Wazuh Rule Optimization...\n")

    # Example: Define Old Rules and Weekly Alerts
    old_rules = [
        '<rule id="5710" level="10"><decoded_as>json</decoded_as><description>Multiple failed SSH logins</description></rule>',
        '<rule id="5720" level="8"><decoded_as>json</decoded_as><description>High CPU usage by unknown process</description></rule>'
    ]
    weekly_alerts = [
        'Alert: 5710 triggered 50 times (SSH brute force attempt)',
        'Alert: 5720 triggered 30 times (Possible malware activity)'
    ]

    # Invoke AI rule optimization
    optimized_rules = optimize_wazuh_rules(old_rules, weekly_alerts)

    # Print AI-generated optimized rules
    print("\n🔍 **Optimized Wazuh Rules:**\n", optimized_rules)
