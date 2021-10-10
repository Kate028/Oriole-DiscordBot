from bot import Oriole
import os
from dotenv import load_dotenv

load_dotenv()


def main() -> None:
    bot = Oriole()
    bot.run(os.getenv("TOKEN"))


if __name__ == "__main__":
    main()
