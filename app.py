import click
import urllib.request
import re

@click.command()
@click.option('--name', prompt='Имя пакета', help='Имя пакета для анализа.')
@click.option('--url', default=None, help='URL-адрес репозитория или путь к файлу.')
@click.option('--mode', default='test', help='Режим работы с репозиторием (по умолчанию "test").')
@click.option('--version', default=None, help='Версия пакета для анализа.')
@click.option('--depth', default=1, type=int, help='Максимальная глубина анализа зависимостей.')
@click.option('--filter', default='', help='Подстрока для фильтрации пакетов.')
def app(name, url, mode, version, depth, filter):
    click.echo(f'Имя пакета: {name}')
    click.echo(f'Версия пакета: {version}')
    click.echo(f'URL: {url}')

    try:
        with urllib.request.urlopen(url) as response:
            text = response.read().decode('utf-8')
    except Exception as e:
        click.echo(f'Ошибка загрузки файла: {e}')
        return

    version_match = re.search(r'version\s*=\s*"([^"]+)"', text)
    if version_match:
        found_version = version_match.group(1)
        if found_version != version:
            click.echo(f'Внимание: версия в Cargo.toml ({found_version}) отличается от указанной ({version}).')
    else:
        click.echo('Версия пакета не найдена в Cargo.toml.')

    deps_match = re.search(r'\[dependencies\](.*?)(?:\n\[[^\]]+\]|$)', text, re.S)
    if not deps_match:
        click.echo('Секция [dependencies] не найдена.')
        return

    deps_text = deps_match.group(1).strip()
    if not deps_text:
        click.echo('Секция зависимостей пуста.')
        return

    click.echo('\nПрямые зависимости:')
    for line in deps_text.splitlines():
        line = line.strip()
        if line and not line.startswith('#'):
            click.echo(f'  {line}')

    click.echo('\nЗавершено успешно.')


if __name__ == '__main__':
    app()