#!/usr/bin/env python3
"""Preparación y revisión local de evaluaciones asistidas; solo biblioteca estándar."""
import argparse
import csv
import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
CRITERIOS = ('objetivo', 'contexto', 'restricciones', 'verificacion')


def digest(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def preparar(entrada, salida):
    salida.mkdir(parents=True, exist_ok=True)
    for equipo in sorted(entrada.iterdir()):
        if not equipo.is_dir():
            continue
        conv = equipo / 'conversacion.md'
        if not conv.is_file():
            print(f'OMITIDO {equipo.name}: falta conversacion.md')
            continue
        destino = salida / equipo.name
        destino.mkdir(exist_ok=True)
        fuentes = {'conversacion.md': conv.read_text(encoding='utf-8')}
        bit = equipo / 'bitacora.md'
        if bit.is_file():
            fuentes['bitacora.md'] = bit.read_text(encoding='utf-8')
        for tipo in ('calidad', 'auditoria'):
            docs = fuentes if tipo == 'auditoria' else {'conversacion.md': fuentes['conversacion.md']}
            paquete = (BASE / f'metaprompt_{tipo}.md').read_text(encoding='utf-8')
            paquete += '\n\nDOCUMENTOS (números de línea añadidos por el programa):\n'
            for nombre, texto in docs.items():
                paquete += f'\nARCHIVO: {nombre}\n'
                paquete += '\n'.join(f'{i}: {linea}' for i, linea in enumerate(texto.splitlines(), 1)) + '\n'
            (destino / f'solicitud_{tipo}.md').write_text(paquete, encoding='utf-8')
        manifiesto = {'version': 1, 'fuentes': fuentes,
                      'sha256': {k: digest(v) for k, v in fuentes.items()},
                      'rubricas_sha256': {t: digest((BASE / f'metaprompt_{t}.md').read_text(encoding='utf-8'))
                                           for t in ('calidad', 'auditoria')}}
        (destino / 'manifiesto.json').write_text(json.dumps(manifiesto, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f'Preparado {destino}; faltantes: {"ninguno" if bit.is_file() else "bitacora.md"}')


def entero(valor):
    return type(valor) is int and valor >= 0


def validar(data, tipo, fuentes):
    errores = []
    def exigir(condicion, mensaje):
        if not condicion:
            errores.append(mensaje)
    def evidencia(items, etiqueta):
        exigir(isinstance(items, list) and bool(items), f'{etiqueta}: sin evidencia')
        if not isinstance(items, list):
            return
        for e in items:
            if not isinstance(e, dict):
                errores.append(f'{etiqueta}: evidencia inválida')
                continue
            nombre, a, b, cita = (e.get(k) for k in ('archivo', 'desde', 'hasta', 'cita'))
            lineas = fuentes.get(nombre, '').splitlines()
            valido = entero(a) and entero(b) and 1 <= a <= b <= len(lineas)
            exigir(valido, f'{etiqueta}: archivo o líneas inválidas')
            exigir(isinstance(cita, str) and bool(cita.strip()) and valido and
                    cita in '\n'.join(lineas[a-1:b]), f'{etiqueta}: cita no verificable')
    exigir(isinstance(data, dict), 'La raíz debe ser objeto')
    if not isinstance(data, dict):
        return errores
    exigir(data.get('tipo') == tipo, 'Tipo incorrecto')
    conteo = data.get('interacciones_observadas')
    exigir('interacciones_observadas' in data and (conteo is None or entero(conteo)), 'Conteo inválido')
    if tipo == 'calidad':
        prompts = data.get('prompts')
        exigir(isinstance(prompts, list), 'Falta lista de prompts')
        if not isinstance(prompts, list):
            return errores
        posiciones = [p.get('posicion') for p in prompts if isinstance(p, dict)]
        exigir(posiciones in ([], ['unico'], ['primero', 'ultimo']), 'Posiciones inválidas o duplicadas')
        for p in prompts:
            if not isinstance(p, dict):
                errores.append('Prompt inválido')
                continue
            exigir(isinstance(p.get('interaccion'), str) and bool(p['interaccion']), 'Falta interacción')
            criterios = p.get('criterios', {})
            if not isinstance(criterios, dict):
                errores.append('Criterios inválidos')
                continue
            exigir(set(criterios) == set(CRITERIOS), 'Deben existir los cuatro criterios')
            for nombre in CRITERIOS:
                c = criterios.get(nombre, {})
                if not isinstance(c, dict):
                    errores.append(f'{nombre}: criterio inválido')
                    continue
                nota = c.get('puntaje')
                exigir('puntaje' in c and (nota is None or (type(nota) is int and nota in (0, 1, 2))), f'{nombre}: nota inválida')
                exigir(isinstance(c.get('motivo'), str) and bool(c['motivo'].strip()), f'{nombre}: falta motivo')
                evidencia(c.get('evidencias'), nombre)
        for campo in ('alertas', 'observaciones'):
            exigir(isinstance(data.get(campo), list) and all(isinstance(x, str) for x in data[campo]), f'{campo}: lista inválida')
        if not prompts:
            exigir(bool(data.get('alertas')), 'Sin prompts debe explicar la falta')
    else:
        declarado = data.get('interacciones_declaradas')
        exigir('interacciones_declaradas' in data and (declarado is None or entero(declarado)), 'Total declarado inválido')
        hallazgos = data.get('hallazgos')
        exigir(isinstance(hallazgos, list) and len(hallazgos) <= 5, 'Hallazgos inválidos o más de cinco')
        for h in hallazgos if isinstance(hallazgos, list) else []:
            if not isinstance(h, dict):
                errores.append('Hallazgo inválido')
                continue
            exigir(h.get('prioridad') in ('alta', 'media', 'baja'), 'Prioridad inválida')
            for campo in ('asunto', 'accion'):
                exigir(isinstance(h.get(campo), str) and bool(h[campo].strip()), f'Falta {campo}')
            evidencia(h.get('evidencias'), 'hallazgo')
        exigir(isinstance(data.get('resumen'), str), 'Falta resumen')
    return errores


def revisar(carpeta):
    filas = []
    for expediente in sorted(carpeta.iterdir()):
        if not (expediente / 'manifiesto.json').is_file():
            continue
        manifiesto = json.loads((expediente / 'manifiesto.json').read_text(encoding='utf-8'))
        fuentes = manifiesto['fuentes']
        notas, problemas, resumen = [], [], []
        if 'bitacora.md' not in fuentes:
            problemas.append('Falta bitácora: comprobar con organización')
        for tipo in ('calidad', 'auditoria'):
            archivo = expediente / f'respuesta_{tipo}.json'
            if not archivo.is_file():
                problemas.append(f'Falta respuesta {tipo}')
                continue
            try:
                data = json.loads(archivo.read_text(encoding='utf-8'))
                errores = validar(data, tipo, fuentes)
            except (ValueError, TypeError) as error:
                errores = [str(error)]
            if errores:
                problemas.extend(f'{tipo}: {e}' for e in errores)
                continue
            resumen.append(f'### {tipo}\n\n```json\n{json.dumps(data, ensure_ascii=False, indent=2)}\n```\n')
            if tipo == 'calidad':
                problemas.extend(data['alertas'])
                for p in data['prompts']:
                    valores = [p['criterios'][c]['puntaje'] for c in CRITERIOS]
                    if None in valores:
                        problemas.append('Prompt no evaluable: requiere especialista')
                    else:
                        notas.append(sum(valores))
            else:
                problemas.extend(f"{h['prioridad']}: {h['asunto']}" for h in data['hallazgos'])
                if data['interacciones_declaradas'] != data['interacciones_observadas']:
                    problemas.append('Discrepancia de interacciones: comprobar, sin sanción automática')
        # No producir promedio parcial cuando falta uno de los prompts.
        calidad = None
        calidad_path = expediente / 'respuesta_calidad.json'
        if calidad_path.is_file():
            try:
                d = json.loads(calidad_path.read_text(encoding='utf-8'))
                if not validar(d, 'calidad', fuentes) and notas and len(notas) == len(d['prompts']):
                    calidad = 15 * (sum(notas) / len(notas)) / 8
            except (ValueError, TypeError):
                pass
        ficha = '# Revisión del especialista\n\nEstado: PENDIENTE DE VALIDACIÓN HUMANA.\n\n'
        ficha += f'Calidad propuesta (máximo 15): {calidad if calidad is not None else "ND"}.\n\n'
        ficha += 'Comprobar primero/último prompt, contexto heredado, citas y cada nota.\n\n'
        ficha += '\n'.join(f'- {x}' for x in problemas) + '\n\n' + '\n'.join(resumen)
        ficha += '\n## Dictamen humano\n\nEspecialista: [ ] · Fecha: [ ]\n\nNotas definitivas por criterio: [ ]\n\nCambios y justificación: [ ]\n\nSegundo evaluador de finalistas: [ ]\n'
        (expediente / 'revision.md').write_text(ficha, encoding='utf-8')
        filas.append({'expediente': expediente.name, 'calidad_propuesta_15': calidad if calidad is not None else 'ND',
                      'asuntos_revision': len(problemas), 'estado': 'PENDIENTE', 'revision': str(expediente / 'revision.md')})
    with (carpeta / 'resumen.csv').open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['expediente', 'calidad_propuesta_15', 'asuntos_revision', 'estado', 'revision'])
        writer.writeheader()
        writer.writerows(filas)
    print(f'{len(filas)} expedientes; resumen en {carpeta / "resumen.csv"}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='accion', required=True)
    p = sub.add_parser('preparar')
    p.add_argument('entrada', type=Path)
    p.add_argument('salida', type=Path)
    p = sub.add_parser('revisar')
    p.add_argument('carpeta', type=Path)
    args = parser.parse_args()
    if args.accion == 'preparar':
        preparar(args.entrada, args.salida)
    else:
        revisar(args.carpeta)

if __name__ == '__main__':
    main()
