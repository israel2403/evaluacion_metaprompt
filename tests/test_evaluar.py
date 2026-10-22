import copy
import tempfile
import unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from evaluar import preparar, revisar, validar


class EvaluacionTests(unittest.TestCase):
    def setUp(self):
        self.fuentes = {'conversacion.md': '## I01\nCuenta pares.\n'}
        c = {'puntaje': 1, 'motivo': 'Parcial', 'evidencias': [
            {'archivo': 'conversacion.md', 'desde': 2, 'hasta': 2, 'cita': 'Cuenta pares.'}]}
        self.data = {'tipo': 'calidad', 'interacciones_observadas': 1,
                     'prompts': [{'posicion': 'unico', 'interaccion': 'I01',
                                  'criterios': {n: copy.deepcopy(c) for n in
                                                ('objetivo', 'contexto', 'restricciones', 'verificacion')}}],
                     'alertas': [], 'observaciones': []}

    def test_evidencia_inventada_y_notas_invalidas(self):
        self.assertEqual(validar(self.data, 'calidad', self.fuentes), [])
        c = self.data['prompts'][0]['criterios']['objetivo']
        c['puntaje'] = True
        c['evidencias'][0]['cita'] = 'No existe'
        errores = validar(self.data, 'calidad', self.fuentes)
        self.assertTrue(any('nota inválida' in e for e in errores))
        self.assertTrue(any('cita no verificable' in e for e in errores))

    def test_sin_evidencia_y_posiciones_duplicadas(self):
        self.data['prompts'][0]['criterios']['contexto']['evidencias'] = []
        self.data['prompts'] *= 2
        self.assertTrue(validar(self.data, 'calidad', self.fuentes))

    def test_separacion_de_fases_y_faltantes(self):
        with tempfile.TemporaryDirectory() as tmp:
            raiz = Path(tmp)
            entrada = raiz / 'entrada' / 'E01'
            entrada.mkdir(parents=True)
            (entrada / 'conversacion.md').write_text(self.fuentes['conversacion.md'])
            (entrada / 'bitacora.md').write_text('RESULTADO_SECRETO_DEL_EQUIPO')
            salida = raiz / 'salida'
            preparar(raiz / 'entrada', salida)
            self.assertNotIn('RESULTADO_SECRETO_DEL_EQUIPO', (salida / 'E01' / 'solicitud_calidad.md').read_text())
            self.assertIn('RESULTADO_SECRETO_DEL_EQUIPO', (salida / 'E01' / 'solicitud_auditoria.md').read_text())
            revisar(salida)
            self.assertIn('ND', (salida / 'resumen.csv').read_text())

    def test_no_promedio_parcial(self):
        import json
        with tempfile.TemporaryDirectory() as tmp:
            raiz = Path(tmp)
            e = raiz / 'E01'
            e.mkdir()
            (e / 'manifiesto.json').write_text(json.dumps({'fuentes': self.fuentes}))
            self.data['prompts'][0]['posicion'] = 'primero'
            ultimo = copy.deepcopy(self.data['prompts'][0])
            ultimo['posicion'] = 'ultimo'
            ultimo['criterios']['objetivo']['puntaje'] = None
            self.data['prompts'].append(ultimo)
            (e / 'respuesta_calidad.json').write_text(json.dumps(self.data))
            revisar(raiz)
            self.assertIn('ND', (raiz / 'resumen.csv').read_text())

if __name__ == '__main__':
    unittest.main()
