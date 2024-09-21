import requests
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
import time
from datetime import datetime
from my_token import TOKEN

def parse_discord(console):
    console.print("Парсинг Discord", style="bold green")

    auction = Prompt.ask("Аукцион (yes/no)", default="no")
    pmin = int(Prompt.ask("Введите минимальную цену (1 минимум)", default="1"))
    pmax = int(Prompt.ask("Введите максимальную цену (100000 максимум)", default="10"))
    origin = Prompt.ask("Происхождение (brute, fishing, stealer, personal, resale, autoreg])", default="autoreg")
    email_type = Prompt.ask("Тип email (email_type[autoreg, native])", default="autoreg")
    sb = Prompt.ask("Был ли ранее продан? (true/false)", default="false")
    sb_by_me = Prompt.ask("Был ли ранее продан вами? (true/false)", default="false")
    nsb = Prompt.ask("Не был ранее продан? (true/false)", default="true")
    nsb_by_me = Prompt.ask("Не был ранее продан вами? (true/false)", default="true")
    nitro_type = int(Prompt.ask("Введите тип Nitro (0 - нету нитро /1 - classic /2 - full /3 - basic)", default="0"))
    start_page = int(Prompt.ask("Введите начальный номер страницы (≥ 1)", default="1"))
    end_page = int(Prompt.ask("Введите конечный номер страницы (≥ 1)", default="100"))

    current_date = datetime.now().strftime("%d.%m.%Y")
    file_name = f"{current_date}-DISCORD.txt"

    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {TOKEN}"
    }

    with open(file_name, 'w', encoding='utf-8') as file:
        for page in range(start_page, end_page + 1):
            url = (
                f"https://api.lzt.market/discord?page={page}&auction={auction}&pmin={pmin}&pmax={pmax}&"
                f"origin[]={origin}&email_type[]={email_type}&sb={sb}&sb_by_me={sb_by_me}&nsb={nsb}&"
                f"nsb_by_me={nsb_by_me}&nitro_type={nitro_type}"
            )

            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                data = response.json()

                if data.get('items'):
                    table = Table(title=f"Результаты парсинга Discord - Страница {page}")
                    table.add_column("ID", justify="center", style="cyan")
                    table.add_column("Цена", justify="center", style="green")
                    table.add_column("Состояние", justify="center", style="blue")
                    table.add_column("Тип Email", justify="center", style="magenta")
                    table.add_column("Тип Nitro", justify="center", style="yellow")

                    for item in data['items']:
                        item_id = str(item.get("item_id", "N/A"))
                        price = str(item.get("price", "N/A"))
                        item_state = str(item.get("item_state", "N/A"))
                        email_type = str(item.get("email_type", "N/A"))
                        discord_nitro_type = str(item.get("discord_nitro_type", "N/A"))

                        table.add_row(item_id, price, item_state, email_type, discord_nitro_type)

                        file.write(f"ID: {item_id}, Цена: {price}, Состояние: {item_state}, "
                                   f"Тип Email: {email_type}, Тип Nitro: {discord_nitro_type}\n")

                    console.print(table)
                else:
                    console.print(f"Нет доступных элементов на странице {page}.", style="bold red")
            else:
                console.print(f"Ошибка запроса на странице {page}: {response.status_code}", style="bold red")

            time.sleep(3)

if __name__ == "__main__":
    console = Console()
    parse_discord(console)
