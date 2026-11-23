import asyncio

from src.agents.investigation_agent import investigate


async def main():
    print("Banking Complaint Investigation Agent")
    print("Type 'exit' to quit.\n")

    while True:
        question = (await asyncio.to_thread(input,"You > ")).strip()

        if question.lower() in {"exit", "quit"}:
            break

        if not question:
            continue

        try:
            answer = await investigate(question)
            print(f"\nAgent > {answer}\n")

        except Exception as error:
            print(f"\nError: {error}\n")


if __name__ == "__main__":
    asyncio.run(main())
