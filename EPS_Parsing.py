import requests
import json
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from datetime import datetime
import chardet
import time
from my_token import TOKEN

def parse_epic_games(console):
    console.print("Парсинг Epic Games", style="bold green")

    start_page = int(Prompt.ask("Введите начальный номер страницы (≥ 1)", default="1"))
    end_page = int(Prompt.ask("Введите конечный номер страницы (≥ 1)", default="10"))
    auction = Prompt.ask("Введите тип аукциона (yes/no)", default="no")
    pmin = Prompt.ask("Введите минимальную цену (≥ 1)", default="5")
    pmax = Prompt.ask("Введите максимальную цену (≤ 50)", default="50")

    origins = Prompt.ask("Введите происхождение (autoreg, personal, resale) через запятую", default="autoreg")
    origin_list = [origin.strip() for origin in origins.split(",")]

    sb = Prompt.ask("Был ли ранее продан? (true/false)", default="false")
    sb_by_me = Prompt.ask("Был ли ранее продан вами? (true/false)", default="false")
    nsb = Prompt.ask("Не был ранее продан? (true/false)", default="true")
    nsb_by_me = Prompt.ask("Не был ранее продан вами? (true/false)", default="true")
    change_email = Prompt.ask("Можно сменить почту? (yes/no)", default="yes")
    gmin = Prompt.ask("Введите минимальное количество игр", default="1")
    gmax = Prompt.ask("Введите максимальное количество игр", default="10")

    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {TOKEN}"
    }

    txt_data = []

    for page in range(start_page, end_page + 1):
        url = (
            f"https://api.lzt.market/epicgames?page={page}&auction={auction}&pmin={pmin}&pmax={pmax}&"
            f"origin[]={'&origin[]='.join(origin_list)}&sb={sb}&sb_by_me={sb_by_me}&nsb={nsb}&"
            f"nsb_by_me={nsb_by_me}&change_email={change_email}&gmin={gmin}&gmax={gmax}"
        )

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            rawdata = response.content
            result = chardet.detect(rawdata)
            encoding = result['encoding']

            response_data = rawdata.decode(encoding)
            data = json.loads(response_data)

            console.print(f"Парсинг страницы {page} завершен успешно!", style="bold green")

            if data['items']:
                table = Table(title=f"Результаты парсинга Epic Games - Страница {page}")
                table.add_column("ID", justify="center", style="cyan")
                table.add_column("Название", justify="center", style="magenta")
                table.add_column("Цена", justify="center", style="green")
                table.add_column("Статус", justify="center", style="blue")
                table.add_column("Количество игр", justify="center", style="yellow")

                for item in data['items']:
                    title = item.get("title", "N/A").encode('utf-8', 'replace').decode('utf-8')
                    table.add_row(
                        str(item.get("item_id", "N/A")),
                        title,
                        str(item.get("price", "N/A")),
                        item.get("item_state", "N/A"),
                        str(item.get("eg_game_count", "N/A"))
                    )
                    txt_data.append(f"{item.get('item_id', 'N/A')}, {title}, {item.get('price', 'N/A')}, {item.get('item_state', 'N/A')}, {item.get('eg_game_count', 'N/A')}")

                console.print(table)
            else:
                console.print(f"Нет доступных элементов на странице {page}.", style="bold red")

            console.print(f"Всего найдено элементов на странице {page}: {data['totalItems']}", style="bold yellow")
        else:
            console.print(f"Ошибка при парсинге страницы {page}: {response.status_code} - {response.text}", style="bold red")

        time.sleep(3)

    if txt_data:
        date_str = datetime.now().strftime("%d.%m.%Y")
        filename = f"{date_str}-EPS.txt"
        with open(filename, mode='w', encoding='utf-8') as file:
            file.write("\n".join(txt_data))

        console.print(f"Данные успешно сохранены в {filename}", style="bold yellow")

if __name__ == "__main__":
    console = Console()
    parse_epic_games(console)