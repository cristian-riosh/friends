# Licencia y atribuciones de los datos

## Qué contiene esta carpeta

Datos léxicos derivados del vocabulario que aparece en la serie *Friends*:
listas de palabras lematizadas, su categoría gramatical, transcripción
fonética, traducción al español y frecuencia de aparición por episodio.

**No contiene guiones, diálogo ni fragmento alguno de la obra audiovisual.**
Los archivos son el resultado de un proceso de extracción estadística: se
tokenizó el texto, se lematizó, se descartó el vocabulario básico mediante un
umbral de frecuencia y se conservó únicamente el inventario de formas con sus
recuentos. La expresión original no es recuperable a partir de estos datos.

## Licencia

Los datos se publican bajo **Creative Commons Reconocimiento-CompartirIgual
4.0 Internacional (CC BY-SA 4.0)**.

https://creativecommons.org/licenses/by-sa/4.0/deed.es

Esto significa que puedes copiarlos, redistribuirlos y adaptarlos, incluso con
fines comerciales, siempre que cites la procedencia y distribuyas cualquier
obra derivada bajo esta misma licencia.

Se ha elegido CC BY-SA porque parte de las traducciones procede de glosas de
Wiktionary, cuyo contenido está bajo CC BY-SA 4.0 y cuya condición de
CompartirIgual se propaga a las obras derivadas.

## Fuentes utilizadas

| Fuente | Uso | Licencia |
|---|---|---|
| Transcripciones públicas de aficionados | Corpus de partida para la extracción de vocabulario | Uso transformativo; no se redistribuye el texto |
| [Apertium](https://apertium.org) `eng-spa` | Diccionario bilingüe base | GPL |
| [Wiktionary](https://es.wiktionary.org) (vía `doozan/spanish_data`) | Glosas español–inglés invertidas | CC BY-SA 4.0 |
| [FreeDict](https://freedict.org) `spa-eng` | Traducciones de respaldo | GPL |
| [CMUdict](http://www.speech.cs.cmu.edu/cgi-bin/cmudict) | Transcripción fonética | Licencia tipo BSD |
| [espeak-ng](https://github.com/espeak-ng/espeak-ng) | Fonética de palabras fuera de CMUdict | GPL v3 |
| [wordfreq](https://github.com/rspeer/wordfreq) | Escala Zipf para el filtro de vocabulario básico | MIT |
| [spaCy](https://spacy.io) + `en_core_web_sm` | Lematización y etiquetado gramatical | MIT |

Las correcciones manuales del archivo `correcciones.json` y el diccionario de
excepciones `lex_manual.json` son aportación propia de este proyecto y se
publican bajo la misma licencia CC BY-SA 4.0.

## Advertencia sobre compatibilidad de licencias

Conviene señalarlo con franqueza: el conjunto combina material derivado de
fuentes bajo **GPL** (Apertium, FreeDict) y bajo **CC BY-SA** (Wiktionary).
Ambas son licencias de tipo copyleft, pero no son mutuamente compatibles, de
modo que un conjunto que mezcle ambas procedencias se encuentra en una
situación jurídicamente incómoda.

Se han adoptado dos medidas para que quien reutilice los datos pueda
resolverlo:

1. La columna `fuente_es` de cada archivo CSV indica el origen de cada
   traducción (`apertium`, `wiktionary`, `freedict`, `manual`, `auditado`), lo
   que permite filtrar por procedencia y quedarse solo con el subconjunto que
   convenga.
2. Los archivos `lex_manual.json` y `correcciones.json` son aportación
   original y pueden usarse sin restricciones heredadas.

Este apartado es informativo y no constituye asesoramiento legal.

## Marcas y titularidad de la obra

*Friends* y sus marcas asociadas son propiedad de Warner Bros. Entertainment
Inc. Este proyecto no está afiliado a sus titulares ni cuenta con su respaldo.
Se trata de un trabajo con finalidad educativa, orientado al aprendizaje de
inglés como lengua extranjera, sin ánimo de lucro.

La licencia CC BY-SA 4.0 se aplica exclusivamente a los datos léxicos
derivados y a las aportaciones propias de este proyecto; no se extiende ni
podría extenderse a la obra audiovisual original.

## Recursos multimedia

- `miau.webp` y `miau.mp3` acompañan a un elemento decorativo de la interfaz.
  Verifica sus condiciones de uso antes de redistribuirlos y añade aquí la
  atribución que corresponda si su procedencia la exige.

---

## Summary in English

Derived lexical data (word lists, part of speech, IPA, Spanish translations and
per-episode frequencies) extracted from *Friends*. **No dialogue or script
excerpts are included**; the original expression cannot be reconstructed from
these files.

Released under **CC BY-SA 4.0**, since part of the translations derives from
Wiktionary glosses. Built with Apertium (GPL), Wiktionary (CC BY-SA), FreeDict
(GPL), CMUdict, espeak-ng (GPL v3), wordfreq (MIT) and spaCy (MIT). See the
`fuente_es` column in each CSV to filter entries by provenance.

*Friends* and related trademarks are the property of Warner Bros. Entertainment
Inc. This project is unaffiliated and unendorsed, and is intended for
non-commercial language-learning use.
