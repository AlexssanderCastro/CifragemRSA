import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

from rsa_core import (
    blocos_para_texto,
    cifrar_mensagem,
    decifrar_mensagem,
    gerar_chaves_automatico,
    gerar_chaves_com_primos,
    texto_para_blocos,
)


BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"


class RSARequestHandler(BaseHTTPRequestHandler):
    def _send_json(self, payload, status=200):
        data = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _serve_file(self, file_path: Path, content_type: str):
        if not file_path.exists():
            self.send_error(404, "Arquivo nao encontrado")
            return
        content = file_path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self._serve_file(STATIC_DIR / "index.html", "text/html; charset=utf-8")
            return
        if self.path == "/style.css":
            self._serve_file(STATIC_DIR / "style.css", "text/css; charset=utf-8")
            return
        if self.path == "/app.js":
            self._serve_file(STATIC_DIR / "app.js", "application/javascript; charset=utf-8")
            return
        self.send_error(404, "Rota nao encontrada")

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(length).decode("utf-8") if length else "{}"
            data = json.loads(body)
        except json.JSONDecodeError:
            self._send_json({"error": "JSON invalido."}, status=400)
            return

        try:
            if self.path == "/api/generate":
                # Se p e q vierem preenchidos, gera com esses primos; senao, gera automaticamente.
                p_raw = data.get("p")
                q_raw = data.get("q")
                if p_raw not in (None, "") and q_raw not in (None, ""):
                    keys = gerar_chaves_com_primos(int(p_raw), int(q_raw))
                else:
                    bits = int(data.get("bits", 16))
                    keys = gerar_chaves_automatico(bits)
                self._send_json(keys)
                return

            if self.path == "/api/encrypt":
                message = data.get("message", "")
                e = int(data["e"])
                n = int(data["n"])
                blocks = cifrar_mensagem(message, e, n)
                self._send_json({
                    "ciphertext_blocks": blocks,
                    "ciphertext_text": blocos_para_texto(blocks),
                })
                return

            if self.path == "/api/decrypt":
                ciphertext_text = data.get("ciphertext", "")
                d = int(data["d"])
                n = int(data["n"])
                blocks = texto_para_blocos(ciphertext_text)
                message = decifrar_mensagem(blocks, d, n)
                self._send_json({"message": message})
                return

            self._send_json({"error": "Rota nao encontrada."}, status=404)
        except KeyError as exc:
            self._send_json({"error": f"Campo obrigatorio ausente: {exc}"}, status=400)
        except ValueError as exc:
            self._send_json({"error": str(exc)}, status=400)
        except UnicodeDecodeError:
            self._send_json(
                {"error": "Falha ao decodificar UTF-8. Verifique se a chave privada corresponde ao texto cifrado."},
                status=400,
            )
        except Exception as exc:
            self._send_json({"error": f"Erro interno: {exc}"}, status=500)


def run_server(host="127.0.0.1", port=8000):
    server = HTTPServer((host, port), RSARequestHandler)
    print(f"Servidor RSA em http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
