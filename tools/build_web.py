"""Gera a versão web: junta HTML + CSS + JS em um template e chama o pygbag.

Uso (na raiz do projeto):
    python tools/build_web.py           # gera app/build/web/ (para publicar)
    python tools/build_web.py --serve   # gera e abre servidor em http://localhost:8000

Por que um script? O pygbag aceita um único arquivo de template (.tmpl). Mantemos
o HTML, o CSS e o JavaScript em arquivos separados em web/src/ (mais fáceis de
editar) e este script os junta antes de cada build.
"""
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "web" / "src"
OUT = ROOT / "web" / "build" / "template.tmpl"
TITLE = "Labirinto Playground"


def assemble() -> Path:
    html = (SRC / "template.html").read_text(encoding="utf-8")
    css = (SRC / "style.css").read_text(encoding="utf-8")
    js = (SRC / "app.js").read_text(encoding="utf-8")

    # O pygbag processa o template com sintaxe estilo Jinja: estas sequências
    # no CSS/JS seriam interpretadas como comandos do template.
    for name, text in (("style.css", css), ("app.js", js)):
        for token in ("{{", "{%", "{#"):
            if token in text:
                sys.exit(f"erro: {name} contém '{token}', que conflita com o template do pygbag")

    for marker in ("<!-- @STYLE -->", "<!-- @SCRIPT -->"):
        if marker not in html:
            sys.exit(f"erro: marcador {marker} ausente em template.html")

    html = html.replace("<!-- @STYLE -->", f"<style>\n{css}\n</style>")
    html = html.replace("<!-- @SCRIPT -->", f"<script>\n{js}\n</script>")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html, encoding="utf-8")
    return OUT


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--serve", action="store_true", help="abre o servidor local do pygbag")
    parser.add_argument("--port", default="8000")
    args = parser.parse_args()

    template = assemble()
    print(f"template gerado: {template.relative_to(ROOT)}")

    cmd = [sys.executable, "-m", "pygbag", "--title", TITLE, "--ume_block", "0",
           "--template", str(template)]
    cmd += ["--port", args.port] if args.serve else ["--build"]
    cmd.append(str(ROOT / "app"))
    sys.exit(subprocess.call(cmd, cwd=ROOT))


if __name__ == "__main__":
    main()
