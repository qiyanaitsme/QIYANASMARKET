from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from Get_Categories import fetch_category_ids
from Display_Categories import display_categories
from EPS_Parsing import parse_epic_games
from DISCORD_Parsing import parse_discord
from my_token import TOKEN

def display_welcome_message(console):
    console.print("Привет! Это портативный парсер от Кианы.", style="bold green")
    console.print("Форум - https://lolz.live/kqlol/. Тг - t.me/selyaqiyana", style="bold yellow")
    console.print("Этот скрипт предназначен для получения информации о категориях и парсинга Epic Games и Discord.", style="bold blue")

def display_menu(console):
    table = Table(title="Доступные функции")
    table.add_column("Номер", justify="center", style="cyan", no_wrap=True)
    table.add_column("Функция", justify="center", style="magenta")

    table.add_row("1", "Получение всех категорий")
    table.add_row("2", "Парсинг Epic Games")
    table.add_row("3", "Парсинг Discord")

    console.print(table)

def main():
    console = Console()
    display_welcome_message(console)
    display_menu(console)

    choice = Prompt.ask("Выберите номер функции, которую хотите использовать")

    if choice == '1':
        categories = fetch_category_ids()
        display_categories(console, categories)
    elif choice == '2':
        parse_epic_games(console)
    elif choice == '3':
        parse_discord(console)
    else:
        console.print("Неверный выбор. Пожалуйста, попробуйте снова.", style="bold red")

if __name__ == "__main__":
    main()