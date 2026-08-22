class MemoryAgent:

    def __init__(self):

        print("Memory Agent Loaded!")

        # Stores conversation history
        self.chat_history = []

    # Save one interaction
    def save(self, question, answer):

        self.chat_history.append({
            "question": question,
            "answer": answer
        })

    # Return complete history
    def get_history(self):

        return self.chat_history

    # Return only last N conversations
    def get_recent(self, n=3):

        return self.chat_history[-n:]

    # Clear memory
    def clear(self):

        self.chat_history = []

        print("Memory Cleared!")



if __name__ == "__main__":

    memory = MemoryAgent()

    while True:

        print("\n========== Memory Menu ==========")
        print("1. Save Conversation")
        print("2. Show History")
        print("3. Show Last 3")
        print("4. Clear Memory")
        print("5. Exit")

        choice = input("\nChoose : ")

        if choice == "1":

            question = input("Question : ")
            answer = input("Answer : ")

            memory.save(question, answer)

            print("\nConversation Saved!")

        elif choice == "2":

            history = memory.get_history()

            print("\n========== HISTORY ==========\n")

            if len(history) == 0:
                print("No conversations found.")

            else:

                for i, item in enumerate(history):

                    print(f"Conversation {i+1}")
                    print("Question :", item["question"])
                    print("Answer   :", item["answer"])
                    print("-"*50)

        elif choice == "3":

            history = memory.get_recent()

            print("\n========== LAST CONVERSATIONS ==========\n")

            if len(history) == 0:
                print("No conversations found.")

            else:

                for i, item in enumerate(history):

                    print(f"Conversation {i+1}")
                    print("Question :", item["question"])
                    print("Answer   :", item["answer"])
                    print("-"*50)

        elif choice == "4":

            memory.clear()

        elif choice == "5":

            print("Goodbye!")
            break

        else:

            print("Invalid Choice!")