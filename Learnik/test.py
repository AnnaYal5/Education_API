from AI.services.comunication import AICommunicator

import asyncio

async def main():
    ai_communicator = AICommunicator()
    conspect = await ai_communicator.generate_test(
        theme="Роль заліза в природі",
        count_questions=5,
        language="Українська",
        difficulty=3,
        font="Roboto",
        font_size=20
    )

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(conspect)

if __name__ == "__main__":
    asyncio.run(main())