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
    {
        "featured": False,
        "url": GITHUB,
        "lang": "GitHub",
        "title_es": "Ver todos los repositorios →",
        "title_en": "See all repositories →",
        "desc_es": "16 repositorios públicos cubriendo ML, Data Science, Algoritmia, Scientific Computing y sistemas de simulación.",
        "desc_en": "16 public repositories covering ML, Data Science, Algorithms, Scientific Computing and simulation systems.",
        "badges": ["16 repos", "Open Source"],
        "meta_es": "JeroHoyos",
        "meta_en": "JeroHoyos",
    },
]

# ── BLOG ──────────────────────────────────────────────────────────────
# Lista de artículos. url puede ser relativa ("blog-rmt.html") o absoluta.
BLOG = [
    {
        "url": "blog/rmt.html",
        "date_es": "Mayo 2025",
        "date_en": "May 2025",
        "tags": ["Matemáticas", "Random Matrix Theory", "Probabilidad", "ML"],
        "title_es": "El camino a través de Random Matrix Theory: de la ley del semicírculo a covariance estimation",
        "title_en": "The Road Through Random Matrix Theory: from the semicircle law to covariance estimation",
        "excerpt_es": "Una bitácora honesta de lo que significa aprender RMT desde cero siendo data scientist: los teoremas que me rompieron la cabeza, los momentos en que todo conectó, y cómo esta teoría —nacida en física nuclear— termina siendo una herramienta sorprendentemente práctica para entender matrices de alta dimensión en ML.",
        "excerpt_en": "An honest log of what it means to learn RMT from scratch as a data scientist: the theorems that broke my brain, the moments when everything clicked, and how this theory — born in nuclear physics — turns out to be a surprisingly practical tool for understanding high-dimensional matrices in ML.",
        "read_es": "Leer artículo →",
        "read_en": "Read article →",
    },
]

# ── ARTE ──────────────────────────────────────────────────────────────
# tipo "generativo" → animación canvas (id debe coincidir con src/js.py)
# tipo "imagen"     → imagen estática desde la carpeta dibujos/
#
# Ejemplo de dibujo:
# {
#     "tipo": "imagen",
#     "url": "dibujos/mi-dibujo.jpg",
#     "titulo_es": "Sin título",
#     "titulo_en": "Untitled",
#     "desc_es": "Descripción del dibujo.",
#     "desc_en": "Drawing description.",
#     "año": "2025",
#     "medio_es": "Lápiz · Papel",
#     "medio_en": "Pencil · Paper",
# }
ARTE = [
    {
        "tipo": "imagen",
        "url": "dibujos/pokemon.jpg",
        "titulo_es": "Pokémon",
        "titulo_en": "Pokémon",
        "año": "2025",
    },
    {
        "tipo": "imagen",
        "url": "dibujos/cato.jpg",
        "titulo_es": "Cato",
        "titulo_en": "Cato",
        "año": "2025",
    },
    {
        "tipo": "imagen",
        "url": "dibujos/foxy.jpg",
        "titulo_es": "Foxy",
        "titulo_en": "Foxy",
        "año": "2025",
    },
    {
        "tipo": "imagen",
        "url": "dibujos/tryk.jpg",
        "titulo_es": "Tryk",
        "titulo_en": "Tryk",
        "año": "2025",
    },
    {
        "tipo": "imagen",
        "url": "dibujos/monster.jpg",
        "titulo_es": "Monster",
        "titulo_en": "Monster",
        "año": "2025",
    },
]

# ── CONTACTO ──────────────────────────────────────────────────────────
CONTACTO_TITULO_ES = "HABLEMOS"
CONTACTO_TITULO_EN = "GET IN TOUCH"
