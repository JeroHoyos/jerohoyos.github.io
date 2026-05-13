# ╔══════════════════════════════════════════════════════════════════╗
# ║                  CONTENT.PY — Solo edita este archivo            ║
# ║  Después de cambiar algo, corre:  python build.py                ║
# ╚══════════════════════════════════════════════════════════════════╝

# ── IDENTIDAD ────────────────────────────────────────────────────────
NOMBRE      = "Jerónimo<br>Hoyos Botero"
TITULO      = "Data Scientist"
TITULO_EN   = "Data Scientist"
EMAIL       = "jerohoyos1@gmail.com"
CV_PDF      = "cv.pdf"
CIUDAD      = "Medellín"
PAIS        = "Colombia"
AÑO         = "2025"

# ── REDES ─────────────────────────────────────────────────────────────
GITHUB    = "https://github.com/JeroHoyos"
LINKEDIN  = "https://www.linkedin.com/in/jerónimo-hoyos-botero-8b692928b/"
KAGGLE    = "https://www.kaggle.com/scratchbox"

# ── BIO (párrafos en ES y EN) ─────────────────────────────────────────
BIO_ES = [
    "Soy <strong>Jerónimo Hoyos</strong>, estudiante de Ingeniería en Sistemas e Informática en la Universidad Nacional de Colombia con una obsesión por entender los problemas antes de resolverlos.",
    "Trabajo en la intersección de la <strong>estadística</strong>, el <strong>álgebra lineal</strong> y el <strong>aprendizaje automático</strong>. Lo que me motiva no es solo que un modelo funcione, sino comprender por qué funciona y qué dice sobre la estructura del problema.",
    "Me mantengo al día con el estado del arte en IA y aplico <strong>GPU-accelerated computing</strong> cuando la escala lo exige. Fuera del código me encuentras leyendo, con mis gatos o pensando en matemáticas.",
]
BIO_EN = [
    "I'm <strong>Jerónimo Hoyos</strong>, a Systems and Computer Engineering student at Universidad Nacional de Colombia, obsessed with understanding problems before solving them.",
    "I work at the intersection of <strong>statistics</strong>, <strong>linear algebra</strong>, and <strong>machine learning</strong>. What drives me isn't just building models that work — it's understanding why they work and what they reveal about the problem's structure.",
    "I keep up with the AI state of the art and apply <strong>GPU-accelerated computing</strong> when scale demands it. Outside of code you'll find me reading, with my cats, or thinking about math.",
]

# ── EDUCACIÓN ─────────────────────────────────────────────────────────
# Lista de dicts: year, name_es, name_en, institution
EDUCACION = [
    {
        "year_es": "2024 - Actualidad",
        "year_en": "2024 - Present",
        "name_es": "Ingeniería en Sistemas e Informática",
        "name_en": "Systems and Computer Engineering",
        "institution": "Universidad Nacional de Colombia",
    },
]

# ── TECH STACK ────────────────────────────────────────────────────────
# Categorías con nombre ES/EN, clase CSS de chip, y lista de tecnologías
STACK = [
    {
        "label_es": "Lenguajes",
        "label_en": "Languages",
        "chip_class": "chip-lang",
        "items": ["Python", "C++", "R","SQL", "Rust"],
    },
    {
        "label_es": "Datos & Feature Engineering",
        "label_en": "Data & Feature Engineering",
        "chip_class": "chip-data",
        "items": ["NumPy", "Pandas", "Polars", "DuckDB", "Apache Spark"],
    },
    {
        "label_es": "Visualización",
        "label_en": "Visualization",
        "chip_class": "chip-viz",
        "items": ["Matplotlib", "Plotly", "Seaborn", "Streamlit"],
    },
    {
        "label_es": "Machine Learning",
        "label_en": "Machine Learning",
        "chip_class": "chip-ml",
        "items": ["PyTorch", "scikit-learn", "XGBoost", "LightGBM", "Transformers", "Foundation Models"],
    },
    {
        "label_es": "MLOps",
        "label_en": "MLOps",
        "chip_class": "chip-ops",
        "items": ["Docker", "FastAPI", "Git", "Linux", "Jupyter", "MLflow"],
    },
    {
        "label_es": "Aceleración GPU",
        "label_en": "GPU Acceleration",
        "chip_class": "chip-gpu",
        "items": ["CUDA", "cuDF", "cuML", "cuGraph", "RAPIDS", "TensorRT", "NVIDIA NIM"],
    },
]

# ── PROYECTOS ─────────────────────────────────────────────────────────
# featured=True → tarjeta grande con stats; featured=False → tarjeta normal
PROYECTOS = [
    {
        "featured": True,
        "url": "https://github.com/JeroHoyos/Molinete-AI",
        "lang": "Python · Rust",
        "title": "Molinete-AI",
        "body_es": "Modelo de lenguaje tipo GPT-2 implementado desde cero. Arquitectura transformer completa: multi-head attention, positional encoding, feed-forward layers y tokenizador BPE propio. Sin frameworks de alto nivel — matemáticas puras traducidas a código eficiente en Rust.",
        "body_en": "A GPT-2–style language model built from scratch. Full transformer architecture: multi-head attention, positional encoding, feed-forward layers and a custom BPE tokenizer. No high-level frameworks — pure math translated into efficient Rust.",
        "badges": ["Transformer", "Self-Attention", "Autoregressive LM", "BPE Tokenizer"],
        "stats_es": [
            ("Arquitectura", "GPT-2"),
            ("Lenguajes", "Python + Rust"),
            ("GitHub Stars", "★ 4"),
            ("Enfoque", "Desde cero"),
        ],
        "stats_en": [
            ("Architecture", "GPT-2"),
            ("Languages", "Python + Rust"),
            ("GitHub Stars", "★ 4"),
            ("Approach", "From scratch"),
        ],
    },
    {
        "featured": False,
        "url": "https://github.com/JeroHoyos/Expected-Growth-of-the-Country-s-Companies-by-Sector",
        "lang": "Jupyter Notebook",
        "title_es": "Crecimiento Esperado por Sector",
        "title_en": "Expected Growth by Sector",
        "desc_es": "Análisis estadístico del crecimiento proyectado de empresas colombianas por sector. Regresión múltiple, intervalos de confianza, bootstrapping y visualizaciones comparativas por industria.",
        "desc_en": "Statistical analysis of projected growth of Colombian companies by sector. Multiple regression, confidence intervals, bootstrapping and comparative visualizations by industry.",
        "badges": ["Regresión", "Pandas", "Matplotlib", "statsmodels"],
        "meta_es": "★ 2 · 1 fork · Dataset empresas CO",
        "meta_en": "★ 2 · 1 fork · Colombian companies dataset",
    },
    {
        "featured": False,
        "url": "https://github.com/JeroHoyos/Analisis-stats-y-tipos-pokemon",
        "lang": "Jupyter Notebook",
        "title_es": "Análisis Pokémon",
        "title_en": "Pokémon Analysis",
        "desc_es": "EDA completo presentado en Turing Box EAFIT. Clustering K-Means y jerárquico, análisis de correlación, reducción con PCA y visualizaciones interactivas sobre 800+ registros.",
        "desc_en": "Full EDA presented at Turing Box EAFIT. K-Means and hierarchical clustering, correlation analysis, PCA reduction and interactive visualizations over 800+ records.",
        "badges": ["EDA", "Clustering", "PCA", "scikit-learn"],
        "meta_es": "Turing Box · EAFIT · 800+ registros",
        "meta_en": "Turing Box · EAFIT · 800+ records",
    },
    {
        "featured": False,
        "url": "https://github.com/JeroHoyos/Operacion_Desgastar_al_Rival-Retro_Game",
        "lang": "Python",
        "title_es": "Operación Desgastar al Rival",
        "title_en": "Operation Wear Down the Rival",
        "desc_es": "Juego retro con motor de física 2D e IA de enemigos como máquina de estados finitos. Arquitectura modular orientada a componentes con patrón Entity-Component-System.",
        "desc_en": "Retro game with 2D physics engine and finite state machine enemy AI. Modular component-oriented architecture using the Entity-Component-System pattern.",
        "badges": ["Pygame", "State Machine", "Game AI", "ECS"],
        "meta_es": "★ 2 · FSM-based AI",
        "meta_en": "★ 2 · FSM-based AI",
    },
    {
        "featured": False,
        "url": "https://github.com/JeroHoyos/clase-teoria-de-grafos",
        "lang": "Jupyter Notebook",
        "title_es": "Teoría de Grafos",
        "title_en": "Graph Theory",
        "desc_es": "Notebooks educativos con implementación desde cero de BFS, DFS, Dijkstra, Bellman-Ford, flujo máximo Ford-Fulkerson y detección de componentes conexas con visualizaciones.",
        "desc_en": "Educational notebooks implementing BFS, DFS, Dijkstra, Bellman-Ford, Ford-Fulkerson max flow and connected components detection from scratch with visualizations.",
        "badges": ["BFS/DFS", "Dijkstra", "Max Flow", "NetworkX"],
        "meta_es": "Graph Theory · 5+ algoritmos",
        "meta_en": "Graph Theory · 5+ algorithms",
    },
]

# ── BLOG ──────────────────────────────────────────────────────────────
# Los artículos se gestionan desde blog/posts/*.md
# build.py los escanea automáticamente — no editar esta lista.
BLOG = []

# ── ARTE ──────────────────────────────────────────────────────────────
# Agrega imágenes con: {"tipo": "imagen", "url": "dibujos/archivo.jpg",
#                        "titulo_es": "Título", "titulo_en": "Title"}
ARTE = [
    {"tipo": "imagen", "url": "dibujos/pokemon.webp", "titulo_es": "Pokémon",  "titulo_en": "Pokémon"},
    {"tipo": "imagen", "url": "dibujos/cato.webp",    "titulo_es": "Cato",     "titulo_en": "Cato"},
    {"tipo": "imagen", "url": "dibujos/foxy.webp",    "titulo_es": "Foxy",     "titulo_en": "Foxy"},
    {"tipo": "imagen", "url": "dibujos/tryk.webp",    "titulo_es": "Tryk",     "titulo_en": "Tryk"},
    {"tipo": "imagen", "url": "dibujos/monster.webp", "titulo_es": "Monster",  "titulo_en": "Monster"},
]

# ── IDIOMAS ───────────────────────────────────────────────────────────
IDIOMAS = [
    {"name": "Español", "level_es": "Nativo",  "level_en": "Native"},
    {"name": "Inglés",  "level_es": "B1",       "level_en": "B1"},
]

# ── PROYECTOS ─────────────────────────────────────────────────────────
PROYECTOS_SUB_ES = "Código que construye, modela y explora — de transformers desde cero hasta juegos retro."
PROYECTOS_SUB_EN = "Code that builds, models and explores — from scratch transformers to retro games."

# ── BLOG ──────────────────────────────────────────────────────────────
BLOG_SUB_ES = "Notas sobre matemáticas, modelos y todo lo que me parece interesante pensar en voz alta."
BLOG_SUB_EN = "Notes on math, models and everything I find interesting to think out loud about."

# ── ARTE ──────────────────────────────────────────────────────────────
ARTE_SUB_ES = "Dibujos digitales hechos en ratos libres. Personajes, criaturas y lo que salga."
ARTE_SUB_EN = "Digital drawings made in my spare time. Characters, creatures and whatever comes out."

# ── CONTACTO ──────────────────────────────────────────────────────────
CONTACTO_TITULO_ES = "HABLEMOS"
CONTACTO_TITULO_EN = "LET'S TALK"
CONTACTO_SUB_ES    = "Si tienes alguna pregunta, propuesta u oportunidad de colaboración, no dudes en contactarme."
CONTACTO_SUB_EN    = "If you have a question, proposal, or collaboration opportunity, don't hesitate to reach out."
