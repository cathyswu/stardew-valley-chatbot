from rag_system import get_rag_chain

def main():
    rag_chain = get_rag_chain()
    print("🌟 Welcome to the Stardew Valley Assistant! 🌟")
    print("I'm here to help with all your farming questions - crops, animals, fishing, mining, and more!")
    print("Ask me anything about Stardew Valley gameplay, or type 'exit' to quit.\n")

    while True:
        query = input("You: ")
        if query.lower() in ("exit", "quit"):
            break
        result = rag_chain.invoke(query)
        # Extract just the answer text from the result dict
        if isinstance(result, dict):
            answer = result.get('result', str(result))
        else:
            answer = str(result)
        print(f"Bot: {answer}\n")

if __name__ == "__main__":
    main()