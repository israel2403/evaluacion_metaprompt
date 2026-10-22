# Evaluación asistida con metaprompts

Un **metaprompt** es una instrucción que guía al modelo para analizar otros prompts. Aquí contiene la rúbrica del anexo A del `Plan_de_Evaluacion_Prompt_and_Code_Challenge_2026.md`, las reglas de evidencia y la estructura de salida. Python prepara los documentos y comprueba las respuestas del modelo; no sustituye al modelo ni al especialista.

Esta herramienta propone una lectura inicial de las conversaciones y las bitácoras de los 25 equipos. No cambia el plan oficial, no decide sanciones ni calcula la clasificación. Solo calcula los **15 puntos provisionales de calidad** a partir de notas validadas en formato; no calcula los 10 de economía de iteraciones ni los 75 del juez. La conformidad del formato y la existencia de citas **no prueban que una nota sea correcta**.

Consulta [EJECUCION.md](EJECUCION.md) para clonar el proyecto y ejecutar una demostración completa en otra computadora.

## Qué produce

- Un paquete de **calidad** por equipo/ronda: conversación completa, sin bitácora ni logs del juez; evalúa primer y último prompt con contexto previo.
- Un paquete de **auditoría** separado: conversación y bitácora; busca discrepancias y prioriza hasta cinco verificaciones.
- Una ficha `revision.md` con notas propuestas, motivos, citas y líneas, asuntos por verificar y espacio de dictamen humano.
- Un `resumen.csv` para localizar los expedientes pendientes; no es una tabla de ganadores.

Las respuestas de IA se leen para entender el contexto y contrastar declaraciones, pero no reciben una nota de corrección técnica: eso exige las pruebas del juez. El programa no ejecuta código de participantes.

## Uso sin API: cualquier modelo que permita recibir texto

Requiere Python 3.10 o posterior; no necesita paquetes externos, claves ni conexión para las operaciones locales. Usa el modelo autorizado por el Comité. Las llamadas al modelo se hacen manualmente en este flujo; **el script no llama a una API**.

Desde la raíz de este repositorio, primero prueba el ejemplo ficticio incluido:

```sh
python3 evaluar.py preparar ejemplo/entrada /tmp/evaluacion-demo
```

1. Abre `/tmp/evaluacion-demo/E01_R2/solicitud_calidad.md` y envía todo su contenido al modelo en un chat nuevo. Guarda su JSON sin cercas Markdown como `/tmp/evaluacion-demo/E01_R2/respuesta_calidad.json`.
2. En **otro chat nuevo**, envía `solicitud_auditoria.md`. Guarda la respuesta como `respuesta_auditoria.json` en esa misma carpeta. No muestres la auditoría al evaluador de calidad antes de que califique.
3. Registra en un archivo `procedencia.md` junto a las respuestas el proveedor, etiqueta exacta de modelo/modo, fecha, evaluador responsable e incidencias. Conserva cada salida original; si repites una evaluación, usa otra carpeta para no reemplazarla.
4. Comprueba y consolida:

```sh
python3 evaluar.py revisar /tmp/evaluacion-demo
```

Abre `resumen.csv` y la ficha `E01_R2/revision.md`. Si falta una respuesta o su JSON es inválido, el programa lo señala. Una nota no evaluable no se convierte en cero. La auditoría puede faltar aunque exista nota de calidad: todos los expedientes siguen pendientes de validación humana.

## Preparar los equipos reales

Estructura de entrada (una carpeta por equipo **y ronda**, no por problema):

```text
entregas/
  E01_R1/
    conversacion.md
    bitacora.md
  E01_R2/
    conversacion.md
    bitacora.md
  E02_R1/
    conversacion.md
    bitacora.md
```

```sh
python3 evaluar.py preparar entregas evaluaciones_piloto
python3 evaluar.py revisar evaluaciones_piloto
```

La primera orden prepara todos los equipos presentes; la segunda lee sus respuestas cuando estén guardadas. Para 25 equipos en una ronda son 50 solicitudes (dos fases). No se necesita una llamada por cada iteración. En R1 se recibe la conversación de ambos problemas dentro del mismo expediente, conservando la etiqueta P1/P2 y el orden cronológico. Si hubo varios chats, inclúyelos completos, separados y con IDs únicos; señala regeneraciones explícitamente. El modelo no puede recuperar mensajes que no fueron entregados.

Formato recomendado de conversación:

````md
# Chat A
## I01 · Alumno · P1
[Prompt exacto]
## I01 · IA
[Respuesta completa]
## I02 · Alumno · P1
[Seguimiento exacto]
## I02 · IA
[Respuesta completa]
````

Retira nombres, correos y cuentas de GitHub antes de preparar los paquetes, manteniendo códigos anónimos. El script no anonimiza automáticamente. No incluyas logs del juez ni tablas de clasificación. Los prompts pueden contener resultados locales: por ello la evaluación a ciegas tiene una limitación residual incluso sin bitácora.

Si la conversación no cabe en el contexto del modelo, no la trunques ni selecciones solo los mejores intentos. Detén ese expediente y prepara una revisión humana o un procedimiento por segmentos previamente validado. Esta versión no estima tokens ni fragmenta automáticamente.

## Revisión rápida por especialista

1. Verificar que el primer/último prompt y el número de interacciones sean correctos; distinguir último prompt de último código generado.
2. Leer los fragmentos citados y su contexto; confirmar las cuatro notas (0–2) de cada prompt. Corregir notas y dejar justificación en el dictamen humano, conservando la respuesta original.
3. Revisar asuntos de auditoría y comprobar fuera de esta herramienta las versiones de código, resultados del juez y horas de GitHub. Una discrepancia es una pregunta, no una sanción.
4. Firmar las notas definitivas e incorporarlas a la hoja oficial; nunca publicar directamente el CSV provisional.

El plan vigente exige dos evaluadores para finalistas y resolución de diferencias mayores de dos puntos. Un modelo no debe contarse automáticamente como segundo evaluador. **Si desean sustituir esa regla por modelo + especialista, el Comité debe modificar explícitamente el plan antes del evento.** Esta implementación mantiene la regla vigente y reduce trabajo mediante prelectura documentada. La puntuación propuesta es `15 × promedio(totales de primer/último prompt) / 8`; un único prompt se cuenta una sola vez.

La ficha muestra las evidencias en JSON para mantener visibles todos los criterios. No calcula duración hasta resolver, no verifica admisibilidad y no infiere aprendizaje duradero. La prioridad de un hallazgo es una sugerencia del modelo; el especialista valida su importancia.

## Calibración antes del evento

Usa conversaciones completas de simulacro (los ejemplos anteriores de bitácora no contienen esas conversaciones). Un especialista califica sin ver la propuesta del modelo; luego comparen por criterio, conteos y errores de evidencia. Incluyan casos incompletos, cambios de chat, regeneraciones e instrucciones maliciosas dentro de la evidencia. Midan el tiempo real de revisión por equipo antes de comprometer el horario de 25 equipos. Fijen modelo y versión de metaprompts para toda la ronda.

El manifiesto conserva una copia exacta de las fuentes, sus hashes SHA-256 y los de los metaprompts para trazabilidad; no constituye firma ni prueba de autenticidad. Las citas se verifican contra esa copia. Si cambian las entregas o la rúbrica, generen una nueva carpeta de evaluación. `preparar` y `revisar` pueden sobrescribir sus propios archivos de salida; no reutilicen una carpeta de una evaluación cerrada.

## Pruebas locales

```sh
python3 -m unittest discover -s tests -v
```

Estas pruebas comprueban separación de fases, rechazo de citas inventadas/notas inválidas y manejo de notas faltantes. No miden precisión del modelo. Se incluyen respuestas manuales ficticias en `ejemplo/respuestas/E01_R2/` para probar el flujo local. No proceden de una evaluación con IA ni constituyen notas de referencia.
