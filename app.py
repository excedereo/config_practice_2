import click

@click.command()
@click.option('--name', prompt='Имя пакета', help='Имя пакета для анализа.')
@click.option('--url', default=None, help='URL-адрес репозитория или путь к файлу.')
@click.option('--mode', default='test', help='Режим работы с репозиторием (по умолчанию "test").')
@click.option('--version', default=None, help='Версия пакета для анализа.')
@click.option('--depth', default=1, type=int, help='Максимальная глубина анализа зависимостей.')
@click.option('--filter', default='', help='Подстрока для фильтрации пакетов.')
def app(name, url, mode, version, depth, filter):
    click.echo(f'Имя пакета: {name}')
    click.echo(f'URL репозитория: {url}')
    click.echo(f'Режим работы с репозиторием: {mode}')
    click.echo(f'Версия пакета: {version}')
    click.echo(f'Максимальная глубина анализа зависимостей: {depth}')
    click.echo(f'Подстрока для фильтрации: {filter}')

    if version and not version.strip():
        raise click.BadParameter('Версия пакета не может быть пустой строкой.')

    if depth < 1:
        raise click.BadParameter('Максимальная глубина анализа зависимостей должна быть больше 0.')

if __name__ == '__main__':
    app()
