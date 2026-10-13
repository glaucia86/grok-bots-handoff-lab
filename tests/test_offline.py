"""Teste offline: roda a parte do tutorial que não usa API, com a conversa sintética.

Rode com: python -m unittest discover -s tests
Não precisa de chave; nenhuma chamada de rede é feita.
"""
import os, subprocess, sys, tempfile, unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(RAIZ, "scripts")
sys.path.insert(0, SCRIPTS)
import comum  # noqa: E402


class Offline(unittest.TestCase):
    def test_marcar_blocos_sintetico(self):
        with tempfile.TemporaryDirectory() as d:
            saida = os.path.join(d, "blocos.md")
            r = subprocess.run([sys.executable, "marcar_blocos.py", "--conversa", "../exemplo/conversa-sintetica.md",
                                "--saida", saida, "--mensagens", "3"], cwd=SCRIPTS, capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn("12 mensagens -> 4 blocos", r.stdout)
            self.assertEqual(list(comum.ler_blocos(saida)), ["B01", "B02", "B03", "B04"])

    def test_bm25_acha_bloco_certo(self):
        b = comum.ler_blocos(os.path.join(RAIZ, "exemplo", "blocos-sinteticos.md"))
        ids = list(b); idx = comum.BM25([b[i] for i in ids])
        top, _, _ = idx.buscar("revisão do Bruno", 1)
        self.assertTrue(top and "Bruno" in b[ids[top[0]]])

    def test_montar_blocos_respeita_teto(self):
        blocos = {"B01": "a " * 5000, "B02": "b " * 5000, "B03": "c " * 5000}
        txt = comum.montar_blocos(list(blocos), blocos, ["a"], teto_tokens=100)
        self.assertLess(len(txt), 100 * 3.6 + 200)

    def test_sem_chave_para_com_mensagem(self):
        env = {k: v for k, v in os.environ.items() if k != "OPENAI_API_KEY"}
        r = subprocess.run([sys.executable, "-c", "import comum; comum.chave()"], cwd=SCRIPTS,
                           capture_output=True, text=True, env=env)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("OPENAI_API_KEY", r.stderr)


if __name__ == "__main__":
    unittest.main()
