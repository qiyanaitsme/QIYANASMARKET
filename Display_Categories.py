from rich.table import Table

def display_categories(console, categories):
    console.print("Категории:", style="bold yellow")

    category_table = Table(title="Список категорий")
    category_table.add_column("Номер", justify="center", style="cyan")  # Изменено на "Номер"
    category_table.add_column("ID", justify="center", style="magenta")
    category_table.add_column("Название", justify="center", style="green")
    category_table.add_column("Имя", justify="center", style="blue")
    category_table.add_column("URL", justify="center", style="blue")

    for index, category in enumerate(categories, start=1):  # Используем enumerate для последовательных номеров
        category_table.add_row(
            str(index),  # Номер
            str(category["category_id"]),
            category["category_title"],
            category["category_name"],
            category["category_url"]
        )

    console.print(category_table)
