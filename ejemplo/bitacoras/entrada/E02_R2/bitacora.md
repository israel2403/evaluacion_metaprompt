# Ejemplo 2: reto incompleto al terminar el tiempo

> Ejemplo llenado con datos ficticios, basado en la Parte A de la [plantilla principal](plantilla_reporte_evaluacion_ia_hackathon.md). Los nombres de archivos ilustran qué entregar; no son evidencias reales adjuntas. No necesitan redactar más que esto.

## 1. Antes de empezar

Datos precargados por la organización:

| ID de sesión | Equipo (código) | Reto / versión | Duración disponible | Versión de plantilla |
| --- | --- | --- | --- | --- |
| S02 | E02 | R02/v1 — Ruta mínima con presupuesto de combustible | 45 minutos | 2.0 |

Datos que llena el equipo:

| Dato | Respuesta |
| --- | --- |
| Integrantes | 2 |
| Experiencia en retos algorítmicos del integrante con más experiencia | 0 — Ninguna |
| Frecuencia de uso de IA para programar del integrante que más la usa | 1 — Menos de una vez por semana |
| ¿Alguien ya conocía este problema o su solución? | No |
| Lenguaje de programación | Python 3 |
| IA utilizada: producto, modelo o modo visible y plan | ChatGPT / modelo o modo no visible (ND) / gratuito |
| ¿Comienzan en un chat nuevo? | Sí |
| Hora de inicio | 10:00 |

## 2. Durante el reto

Guardamos los mensajes y las respuestas completos en `entrega/conversacion.md`, identificados como I01, I02 e I03. Solo anotamos una fila por interacción aquí.

| Interacción | Minuto desde el inicio | IA utilizada | ¿Para qué la consultaron? | ¿Qué aportaron al prompt? | Resultado observado |
| --- | --- | --- | --- | --- | --- |
| I01 | 3 | Inicial | Código | EN, RE | INC |
| I02 | 18 | Inicial | Diagnóstico | FE, CP, HP | SC |
| I03 | 30 | Inicial | Corrección | RE, HP, VE | LIM |

**Códigos rápidos:** EN = enunciado; RE = restricciones; CP = caso con salida esperada; FE = fallo observado; HP = hipótesis propia; VE = pedir verificación; OT = otro aporte.

**Resultados:** OK = pasa las pruebas ejecutadas; INC = salida incorrecta; COM = no compila; EJE = falla al ejecutar; LIM = excede tiempo o memoria; SP = sin probar; SC = sin código; ND = no disponible. Añadir `+H` si se probó después de editar manualmente. OK no garantiza aceptación del juez.

## 3. Al terminar

| Dato | Respuesta |
| --- | --- |
| Hora de cierre | 10:45 |
| Total de interacciones con IA, incluidas las de otros chats | 3 |
| Conversaciones completas | entrega/conversacion.md |
| Primer código IA sin editar | entrega/primera_ia.py — I01 |
| Último código IA sin editar | entrega/ultima_ia.py — I03 |
| Código final | entrega/final.py |
| ¿Qué cambiaron manualmente en el código? | Ninguno |
| Principal obstáculo | Tiempo o memoria |
| Incidentes ajenos al código | Ninguno |

**Un ejemplo concreto de lo que aprendimos:**

- Fallo que detectamos o duda que investigamos: La primera solución descartaba rutas que llegaban a una ciudad con más combustible pero mayor costo acumulado.
- Qué cambiamos en el prompt o en el código: Propusimos representar cada estado como ciudad y combustible disponible y pedimos justificar la complejidad.
- Cómo lo comprobamos y qué pasó: La última versión pasó el contraejemplo pequeño, pero excedió el límite de tiempo en nuestra prueba grande; entregamos esa versión sin resolver el rendimiento.

Antes de entregar:

- [x] La conversación incluye todos los chats utilizados, con sus prompts y respuestas.
- [x] Los archivos de código están identificados como primer código IA, último código IA y entrega final.
- [x] Entregamos la bitácora aunque el reto haya quedado incompleto.
