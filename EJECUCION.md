# Cómo ejecutar el proyecto en otra computadora

## Requisitos y descarga

Necesitas Git y Python 3.10 o posterior. No hay dependencias externas ni claves de API. El programa prepara archivos; las consultas al modelo se realizan manualmente.

```sh
git clone https://github.com/israel2403/evaluacion_metaprompt.git
cd evaluacion_metaprompt
python3 --version
```

Si el repositorio es privado, el propietario debe dar acceso a tu cuenta de GitHub. También puedes descargar y descomprimir el ZIP desde GitHub. En Windows usa `py -3` en lugar de `python3`; ejecuta todo desde la carpeta que contiene `evaluar.py`.

## Demostración con las dos bitácoras suministradas

Se incluyen copias completas de `ejemplo_bitacora_alumnos_solucion_completada.md` en `ejemplo/bitacoras/entrada/E01_R1/bitacora.md` y de `ejemplo_bitacora_alumnos_reto_incompleto.md` en `ejemplo/bitacoras/entrada/E02_R2/bitacora.md`.

Las bitácoras mencionan conversaciones y código que no están adjuntos. Sus enlaces a la plantilla original son referencias del documento fuente; esa plantilla no es necesaria para ejecutar Python. Cada `conversacion.md` es un marcador que declara la ausencia de mensajes. No representa una conversación reconstruida.

```sh
python3 evaluar.py preparar ejemplo/bitacoras/entrada salida_demo
```

Copia `respuesta_calidad.json`, `respuesta_auditoria.json` y `procedencia.md` desde cada carpeta de `ejemplo/bitacoras/respuestas/` a su carpeta correspondiente dentro de `salida_demo/`. Puedes hacerlo con el explorador o ejecutar este comando portable:

```sh
python3 -c "from pathlib import Path; import shutil; origen=Path('ejemplo/bitacoras/respuestas'); [shutil.copy2(p, Path('salida_demo') / p.relative_to(origen)) for p in origen.glob('*/*') if p.is_file()]"
python3 evaluar.py revisar salida_demo
```

Abre `salida_demo/resumen.csv` y `salida_demo/E01_R1/revision.md` o `salida_demo/E02_R2/revision.md`. Deben aparecer dos expedientes con calidad `ND`, pendientes de validación humana y con aviso de conversación faltante. Las respuestas JSON son ejemplos manuales, no salidas de IA ni calificaciones oficiales. No hacen falta los archivos de la computadora de origen.

## Ejemplo sintético con conversación completa

También se conserva un ejemplo ficticio independiente con dos interacciones, distinto de las bitácoras anteriores:

```sh
python3 evaluar.py preparar ejemplo/entrada salida_demo/sintetico
python3 -c "from pathlib import Path; import shutil; origen=Path('ejemplo/respuestas'); [shutil.copy2(p, Path('salida_demo/sintetico') / p.relative_to(origen)) for p in origen.glob('*/*') if p.is_file()]"
python3 evaluar.py revisar salida_demo/sintetico
```

Su nota propuesta será 15/15 por las respuestas manuales incluidas, únicamente para comprobar el cálculo; no es una nota validada.

## Evaluar entregas propias

1. Crea `entregas/E01_R1/conversacion.md` con los mensajes completos y `entregas/E01_R1/bitacora.md` con la bitácora. Usa otra carpeta por equipo y ronda. Sustituye los marcadores de demostración cuando corresponda.
2. Ejecuta `python3 evaluar.py preparar entregas evaluaciones_piloto`.
3. Envía el contenido de `solicitud_calidad.md` al modelo autorizado en un chat nuevo; guarda su respuesta como `respuesta_calidad.json` en el mismo expediente. Repite con `solicitud_auditoria.md` en otro chat nuevo. Guarda solo JSON, sin cercas Markdown. No uses las respuestas de demostración para entregas reales.
4. Registra proveedor, modelo/modo, fecha, evaluador e incidencias en `procedencia.md`.
5. Ejecuta `python3 evaluar.py revisar evaluaciones_piloto` y revisa las fichas con un especialista.

Usa carpetas nuevas para cada evaluación: preparar y revisar pueden sobrescribir sus salidas, incluido el dictamen humano en `revision.md`. Las carpetas de entregas y resultados están excluidas de Git para evitar publicar datos de participantes por accidente.

## Comprobar la instalación

```sh
python3 -m unittest discover -s tests -v
```

Si aparece `Falta respuesta`, copia o guarda los dos JSON en la carpeta del expediente que contiene `manifiesto.json`. Si aparece `cita no verificable`, revisa el texto literal y las líneas de la conversación original. `ND` significa que no hay una nota evaluable; no equivale a cero.
