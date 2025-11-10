import click
import urllib.request
import re
from collections import deque

def parse_cargo_toml(text):
    deps_section = re.search(r'\[dependencies\](.*?)\n\[', text, re.S) or \
                   re.search(r'\[dependencies\](.*)', text, re.S)
    if not deps_section:
        return {}
    deps_text = deps_section.group(1).strip()
    deps = {}
    for line in deps_text.splitlines():
        line = line.strip()
        if line and not line.startswith('#'):
            name = line.split('=')[0].strip()
            deps[name] = []
    return deps

def bfs_dependencies(graph, start, max_depth, filter_substr):
    visited = set()
    queue = deque([(start, 0)])
    result = []

    while queue:
        node, depth = queue.popleft()
        if node in visited or (filter_substr and filter_substr in node):
            continue
        visited.add(node)
        result.append((node, depth))
        if depth < max_depth:
            for dep in graph.get(node, []):
                queue.append((dep, depth + 1))
    return result

@click.command()
@click.option('--name', prompt='Имя пакета', help='Имя пакета для анализа.')
@click.option('--url', default=None, help='URL Cargo.toml для real режима.')
@click.option('--version', default=None, help='Версия пакета для анализа.')
@click.option('--max_depth', default=3, type=int, help='Максимальная глубина анализа зависимостей.')
@click.option('--filter_substr', default='', help='Подстрока для фильтрации пакетов.')
@click.option('--mode', default='real', type=click.Choice(['real', 'test']), help='Режим работы: real или test')
def app(name, url, version, max_depth, filter_substr, mode):
    print(f"Имя пакета: {name}, Версия: {version}, Режим: {mode}, Фильтр: {filter_substr}, Глубина: {max_depth}\n")

    if mode == 'real':
        if not url:
            print("Для real режима нужно указать URL Cargo.toml")
            return
        try:
            with urllib.request.urlopen(url) as f:
                text = f.read().decode('utf-8')
        except Exception as e:
            print(f"Ошибка загрузки файла: {e}")
            return

        graph = {name: list(parse_cargo_toml(text).keys())}

        cargo_version_match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', text)
        cargo_version = cargo_version_match.group(1) if cargo_version_match else None
        if version and cargo_version and cargo_version != version:
            print(f"Версия в Cargo.toml ({cargo_version}) отличается от указанной ({version}).\n")

    else:
        graph = {
            "A": ["B", "C"],
            "B": ["C", "D"],
            "C": ["E"],
            "D": ["A"],
            "E": []
        }
        name = "A"

    result = bfs_dependencies(graph, name, max_depth, filter_substr)

    for node, depth in result:
        print(f"{node} (глубина {depth})")

if __name__ == "__main__":
    app()