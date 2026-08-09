# Léxico de Friends

Vocabulario en inglés extraído episodio a episodio de las diez temporadas de
*Friends*, con transcripción fonética, traducción al español y frecuencia de
aparición. Pensado como material de apoyo para aprender inglés viendo la serie.

**5.307 palabras · 227 episodios · 100 % con traducción**

El proyecto entrega cuatro cosas: los datos en CSV, una tabla consultable en
Excel, un mazo de Anki listo para importar y una aplicación web publicable en
GitHub Pages.

---

## Qué contiene

```
├── app/                          aplicación web (publicable tal cual)
│   ├── index.html
│   ├── datos/
│   │   ├── episodios.json        índice de los 227 capítulos
│   │   ├── lexico.json           las 5.307 palabras
│   │   ├── t01.json … t10.json   frecuencias por temporada
│   │   ├── miau.webp, miau.mp3   recursos de un huevo de pascua
│   │   └── LICENCIA-DATOS.md
│   └── generar_app_json.py       regenera la app desde los CSV
│
├── vocabulario_por_episodio.zip  227 CSV, uno por capítulo, más el pipeline
├── consolidado.csv               las 15.204 filas en un solo archivo
├── lemas_unicos.csv / .xlsx      tabla deduplicada, una fila por palabra
├── friends_vocabulario.apkg      mazo de Anki (1.000 + 25 tarjetas)
└── index.html                    variante de la app en un solo archivo
```

### Columnas de los CSV por episodio

| Campo | Contenido |
|---|---|
| `episodio` | `S01E01`. Los dobles se marcan `S10E17-18` |
| `lema` | Forma lematizada, en minúscula |
| `pos` | `NOUN`, `VERB`, `ADJ` o `ADV` |
| `ipa` | Transcripción fonética entre barras |
| `espanol` | Hasta tres acepciones separadas por punto y coma |
| `forma_estandar` | Solo en coloquialismos: `dunno` → *don't know* |
| `idioma_origen` | Solo en extranjerismos: `frances`, `italiano`… |
| `frec_episodio` | Apariciones en ese capítulo |
| `frec_total` | Apariciones en toda la serie |

---

## Cómo usarlo

### Aplicación web

Sube el contenido de `app/` a un repositorio, con `index.html` en la raíz y la
carpeta `datos/` junto a él, y activa GitHub Pages en Settings → Pages.

En local necesita servirse por HTTP, porque el navegador bloquea las peticiones
`fetch` sobre `file://`:

```bash
cd app && python3 -m http.server
# abrir http://localhost:8000
```

Navegación por temporada y capítulo, filtros por categoría gramatical,
palabras nuevas, coloquialismos y extranjerismos, pronunciación por voz del
sistema con velocidad y repeticiones ajustables, y tema claro u oscuro. Las
flechas ← y → saltan de episodio.

Si prefieres abrirla con doble clic sin levantar un servidor, usa el
`index.html` de la raíz: es la misma app con los datos incrustados.

### Mazo de Anki

Doble clic sobre el `.apkg` con Anki abierto. Se instalan dos submazos bajo
`Friends`: **Vocabulario** con las 1.000 palabras más frecuentes de la serie
—las que cubren dos tercios de las apariciones— y **Extranjerismos** con 25
términos que en la serie se pronuncian en otro idioma, cada uno con su audio
incrustado.

Las tarjetas llevan etiquetas por categoría gramatical, banda de frecuencia y
registro coloquial, de modo que puedes estudiar por bloques o suspender lo que
no te interese.

### Hojas de cálculo

`lemas_unicos.xlsx` trae la tabla completa con autofiltro y una hoja de resumen
calculada por fórmulas, que se recalcula si filtras o editas los datos.

---

## Cómo se construyó

El pipeline parte de transcripciones públicas de aficionados y produce datos
léxicos derivados. No conserva ni redistribuye diálogo.

1. **Limpieza.** Se retiran marcas HTML, acotaciones escénicas entre corchetes,
   etiquetas de personaje y créditos de transcripción.
2. **Análisis.** spaCy lematiza y etiqueta cada palabra.
3. **Filtro de vocabulario básico.** Se descarta lo demasiado común usando la
   escala **Zipf** de `wordfreq`, que es el logaritmo de la frecuencia por mil
   millones de palabras. El umbral es 4,3, equivalente a una aparición cada
   50.000 palabras: `coffee` (4,86) queda fuera, `shoe` (4,24) entra.
4. **Descartes.** Nombres propios detectados por ratio de mayúsculas y por
   entidades NER, interjecciones y restos de tokenización.
5. **Traducción en cascada.** Correcciones auditadas → diccionario manual →
   Apertium → Wiktionary invertido → FreeDict. Si falla todo, se desmonta la
   palabra por sufijos y se reintenta con la raíz.
6. **Fonética.** CMUdict, con espeak-ng para lo que queda fuera.

### Regenerar los datos

```bash
pip install spacy wordfreq eng-to-ipa
python -m spacy download en_core_web_sm
apt-get install espeak-ng

python procesar_v5.py      # 227 CSV + consolidado
python tabla_lemas.py      # tabla deduplicada
python generar_app_json.py # datos de la app web
```

Los scripts van dentro de `vocabulario_por_episodio.zip`.

---

## Calidad de los datos

La traducción automática de diccionarios bilingües acierta el sentido pero
falla en el registro. Auditando el resultado aparecieron cuatro clases de error
que se corrigieron a mano:

- **Lematización.** `pant`, la palabra más frecuente del corpus con 130
  apariciones, venía de *pants* y salía traducida como «jadeo».
- **Sentido y registro.** Apertium elegía acepciones raras: `roommate` como
  «conviviente», `jerk` como «cacaseno», `buck` como «corcovo» en vez de
  «dólar».
- **Concordancia de género.** `grandmother` daba «abuelo»; `bride`, «novio».
- **Extranjerismos.** El detector automático marcó 132 términos, de los que
  solo **25 eran reales**. El resto eran palabras inglesas mal clasificadas
  —`sorta`, `loin`, `academia`— o fragmentos de tokenización.

En total: 377 traducciones escritas a mano, 83 correcciones auditadas y 164
descartes. Todo queda en `lex_manual.json` y `correcciones.json`, que encabezan
la cascada, de modo que cualquier reejecución las reutiliza.

**Lo que no está verificado.** Se revisó a fondo el centenar de palabras más
frecuentes y todos los desajustes entre categoría gramatical y traducción, pero
las 2.491 palabras que aparecen una sola vez en toda la serie conservan la
traducción automática sin comprobar una por una. Si detectas errores, añadirlos
a `correcciones.json` y reejecutar el pipeline es inmediato.

---

## Licencia

Los datos se publican bajo **CC BY-SA 4.0**, condición heredada de las glosas
de Wiktionary. Las atribuciones completas, la tabla de fuentes y una nota sobre
la incompatibilidad entre las licencias GPL y CC BY-SA que conviven en el
conjunto están en [`app/datos/LICENCIA-DATOS.md`](app/datos/LICENCIA-DATOS.md).

*Friends* y sus marcas asociadas son propiedad de Warner Bros. Entertainment
Inc. Este proyecto no está afiliado a sus titulares ni cuenta con su respaldo.
Es un trabajo con finalidad educativa y sin ánimo de lucro; los archivos
contienen datos léxicos derivados, no los guiones.
