from assistant.engine import process_query
from assistant.validator import validate_query
import time


# ---------------------------
# 🔥 Streaming Output (Realtime Feel)
# ---------------------------
def stream_output(text):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(0.01)
    print()


# ---------------------------
# 🎮 Scenario Simulation (Adaptive)
# ---------------------------
def run_simulation():
    print("\n🎮 Election Scenario Simulation\n")

    trust_score = 0

    print("You are a citizen preparing for elections.\n")

    print("Step 1: Registration")
    choice = input("Do you register early? (yes/no): ").lower()
    if "yes" in choice:
        trust_score += 1
        print("✅ Good! You're prepared.\n")
    else:
        print("⚠️ Late registration may cause issues.\n")

    print("Step 2: Candidate Awareness")
    choice = input("Do you research candidates? (yes/no): ").lower()
    if "yes" in choice:
        trust_score += 1
        print("✅ Informed decision-making!\n")
    else:
        print("⚠️ Lack of knowledge affects choices.\n")

    print("Step 3: Voting")
    choice = input("Do you vote on election day? (yes/no): ").lower()
    if "yes" in choice:
        trust_score += 1
        print("🗳️ Vote successfully cast!\n")
    else:
        print("❌ You missed your chance to vote.\n")

    print("📊 Evaluating your election journey...\n")
    time.sleep(1)

    if trust_score == 3:
        print("🏆 Ideal citizen! You followed best practices.\n")
    elif trust_score == 2:
        print("👍 Good effort, but can improve.\n")
    else:
        print("⚠️ You need to engage more.\n")


# ---------------------------
# 🧭 Guide Mode
# ---------------------------
def show_guide():
    print("""
🧭 Election Guide:

1. Registration – Citizens register before deadline
2. Campaigning – Candidates promote their ideas
3. Voting – Citizens cast votes
4. Counting – Votes are verified
5. Results – Winners are announced
""")


# ---------------------------
# 🎯 Mission Mode (Scored)
# ---------------------------
def run_mission():
    print("\n🎯 Election Mission Mode\n")

    score = 0

    tasks = [
        ("Register yourself", "register"),
        ("Understand candidates", "campaign"),
        ("Cast your vote", "vote"),
    ]

    for task, keyword in tasks:
        print(f"👉 Task: {task}")
        user = input("Your action: ").lower()

        if keyword in user:
            score += 1
            print("✅ Success!\n")
        else:
            print("⚠️ Partial success.\n")

    print("📊 Mission Analysis:")
    time.sleep(1)

    print(f"Score: {score}/{len(tasks)}")

    if score == 3:
        print("🏆 Perfect mission!\n")
    elif score == 2:
        print("👍 Good job!\n")
    else:
        print("⚠️ Needs improvement.\n")


# ---------------------------
# 🚀 Main Application
# ---------------------------
def run():
    print("=" * 60)
    print("🗳️  ELECTION EXPERIENCE SYSTEM")
    print("=" * 60)
    print("An interactive, adaptive election assistant.\n")

    name = input("Enter your name: ")
    print("\nInitializing system...")
    time.sleep(1)

    print(f"\nWelcome {name}! 👋")
    print("Type 'help' to explore features.\n")

    history = []

    user_profile = {
        "weak_topics": {},
        "interactions": 0
    }

    while True:
        user_input = input("You: ").strip()

        # ---------------------------
        # EXIT + SMART SUMMARY
        # ---------------------------
        if user_input.lower() == "exit":
            print("\n📊 Session Summary:")
            print(f"- Total interactions: {user_profile['interactions']}")

            if user_profile["weak_topics"]:
                top = max(user_profile["weak_topics"], key=user_profile["weak_topics"].get)
                print(f"- Most explored topic: {top}")

            print("🧠 System adapted based on your interactions.")
            print("Assistant: Goodbye!")
            break

        # ---------------------------
        # HELP MODE
        # ---------------------------
        if user_input.lower() == "help":
            print("""
✨ Available Modes:

🧭 guide      → Step-by-step explanation
🎮 simulate   → Scenario-based experience
🎯 mission    → Interactive task-based mode

💬 Ask Questions:
- How do I register?
- How does voting work?
- When are results announced?

Type 'exit' to quit.
""")
            continue

        # ---------------------------
        # MODE ROUTING
        # ---------------------------
        if "guide" in user_input.lower():
            show_guide()
            continue

        if "simulate" in user_input.lower():
            run_simulation()
            continue

        if "mission" in user_input.lower():
            run_mission()
            continue

        # ---------------------------
        # VALIDATION
        # ---------------------------
        if not validate_query(user_input):
            print("Assistant: Invalid input.\n")
            continue

        # ---------------------------
        # CORE INTELLIGENCE
        # ---------------------------
        try:
            print("Assistant is thinking...")
            time.sleep(0.4)

            response = process_query(user_input)

            # Track user learning
            user_profile["interactions"] += 1
            history.append(user_input)

            for keyword in ["register", "vote", "count", "result", "campaign"]:
                if keyword in user_input.lower():
                    user_profile["weak_topics"][keyword] = user_profile["weak_topics"].get(keyword, 0) + 1

            # Smart suggestion
            if user_profile["interactions"] >= 3 and user_profile["weak_topics"]:
                weak = max(user_profile["weak_topics"], key=user_profile["weak_topics"].get)
                print(f"💡 Tip: Explore more about '{weak}' for deeper understanding.\n")

            label = "Assistant (adaptive):" if len(history) > 1 else "Assistant:"
            print(label, end=" ")
            stream_output(response)
            print()

        except Exception as e:
            print("Assistant: Error occurred:", str(e))


# ---------------------------
# ENTRY POINT
# ---------------------------
if __name__ == "__main__":
    run()