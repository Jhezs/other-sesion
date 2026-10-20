import json, tempfile, unittest
from pathlib import Path

import ahorro


class Ahorro(unittest.TestCase):
    def test_carpeta_se_busca_hacia_arriba(self):
        with tempfile.TemporaryDirectory() as d:
            raiz = Path(d)
            proyecto = Path("/ruta/mi proyecto")
            (raiz / "-ruta-mi-proyecto").mkdir()
            sub = proyecto / "frontend" / "src"
            self.assertEqual(ahorro.carpeta_proyecto(sub, raiz), raiz / "-ruta-mi-proyecto")
            self.assertIsNone(ahorro.carpeta_proyecto("/otra/ruta", raiz))

    def test_cargar_no_duplica_mensajes(self):
        usage = {"input_tokens": 2, "cache_creation_input_tokens": 10, "cache_read_input_tokens": 100, "output_tokens": 5}
        lineas = [
            {"message": {"id": "a", "usage": usage}},
            {"message": {"id": "a", "usage": usage}},  # repetido: se cuenta una vez
            {"message": {"id": "b", "usage": {**usage, "cache_read_input_tokens": 200}}},
            "no es json",
        ]
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "s.jsonl"
            f.write_text("\n".join(l if isinstance(l, str) else json.dumps(l) for l in lineas), encoding="utf-8")
            t = ahorro.cargar(f)
        self.assertEqual((t["turnos"], t["salida"], t["primero"], t["ultimo"]), (2, 10, 112, 212))


if __name__ == "__main__":
    unittest.main()
