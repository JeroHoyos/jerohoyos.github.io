NOMBRE      = "Jerónimo<br>Hoyos Botero"
TITULO      = "Data Scientist · ML Engineer"
EMAIL       = "jerohoyos1@gmail.com"
CIUDAD      = "Medellín"
PAIS        = "Colombia"
AÑO         = "2025"

GITHUB    = "https://github.com/JeroHoyos"
LINKEDIN  = "https://www.linkedin.com/in/jeronimo-hoyos-botero/"
KAGGLE    = "https://www.kaggle.com/scratchbox"

BIO_ES = [
    "Soy <strong>Jerónimo Hoyos</strong>, estudiante de Ingeniería en Sistemas e Informática en la Universidad Nacional de Colombia con una obsesión por entender los problemas antes de resolverlos. Trabajo en la intersección de la <strong>probabilidad</strong>, el <strong>álgebra lineal</strong> y las <strong>ciencias de la computación</strong>.",
    "Lo que me motiva no es solo que un modelo funcione, sino comprender por qué funciona y qué dice sobre la estructura del problema. Me mantengo al día con el estado del arte en IA, y fuera del código me encuentras leyendo, viendo videos de gatos o jugando.",
]
BIO_EN = [
    "I'm <strong>Jerónimo Hoyos</strong>, a Computer Software Engineering student at Universidad Nacional de Colombia, obsessed with understanding problems before solving them. I work at the intersection of <strong>probability</strong>, <strong>linear algebra</strong>, and <strong>computer science</strong>.",
    "What drives me isn't just building models that work, but understanding why they work and what they reveal about the structure of the problem. I keep up with the state of the art in AI, and outside of code you'll find me reading, watching cat videos, or gaming.",
]

EDUCACION = [
    {
        "year_es": "2024 - Actualidad",
        "year_en": "2024 - Present",
        "name_es": "Ingeniería en Sistemas e Informática",
        "name_en": "Computer Software Engineering",
        "institution": "Universidad Nacional de Colombia",
    },
]

PROYECTOS = [
    {
        "featured": True,
        "url": "https://github.com/JeroHoyos/Molinete-AI",
        "img": "proyectos/molinete.png",
        "lang": "Python · Rust",
        "title": "Molinete-AI",
        "body_es": "Transformer desarrollado desde cero en Rust, enfocado en implementación eficiente de arquitecturas de deep learning y operaciones tensoriales. Presentado en la comunidad Medellín IA en la oficina de EPAM Medellín.",
        "body_en": "Transformer built from scratch in Rust, focused on efficient implementation of deep learning architectures and tensor operations. Presented at the Medellín IA community at EPAM Medellín's office.",
        "badges": ["Transformer", "Rust", "Deep Learning", "Tensors"],
        "stats_es": [
            ("Arquitectura", "Transformer"),
            ("Lenguajes", "Python + Rust"),
            ("Presentado en", "Medellín IA"),
            ("Enfoque", "Desde cero"),
        ],
        "stats_en": [
            ("Architecture", "Transformer"),
            ("Languages", "Python + Rust"),
            ("Presented at", "Medellín IA"),
            ("Approach", "From scratch"),
        ],
    },
    {
        "featured": False,
        "url": "https://github.com/SudoerJteheran/ResearchAgent-DataHack2026",
        "img": "proyectos/investigia.png",
        "lang": "Python · LangGraph",
        "title_es": "InvestigIA",
        "title_en": "InvestigIA",
        "desc_es": "Asistente autónomo para investigación científica construido con LangGraph y Ollama. Análisis de literatura académica con inferencia completamente local. Tercer lugar en DataHack 2026.",
        "desc_en": "Autonomous scientific research assistant built with LangGraph and Ollama. Academic literature analysis with fully local inference. Third place at DataHack 2026.",
        "badges": ["LangGraph", "Ollama", "Agents", "RAG"],
        "meta_es": "3er lugar · DataHack 2026",
        "meta_en": "3rd place · DataHack 2026",
    },
    {
        "featured": False,
        "url": "https://www.kaggle.com/code/scratchbox/analysis-and-modeling-of-smoking",
        "img": "proyectos/smoking.png",
        "lang": "Python · Jupyter",
        "title_es": "Analysis and Modeling of Smoking",
        "title_en": "Analysis and Modeling of Smoking",
        "desc_es": "Análisis exploratorio y modelado de machine learning sobre el dataset Body Signals of Smoking para predecir hábitos de tabaquismo a partir de señales fisiológicas.",
        "desc_en": "Exploratory analysis and ML modeling on the Body Signals of Smoking dataset to predict smoking habits from physiological signals.",
        "badges": ["EDA", "scikit-learn", "Pandas", "Kaggle"],
        "meta_es": "Kaggle · Body Signals of Smoking",
        "meta_en": "Kaggle · Body Signals of Smoking",
    },
    {
        "featured": False,
        "url": "https://github.com/JeroHoyos/Efficient-Krylov-Sequence-Computation-in-GPU",
        "img": "proyectos/krylov.png",
        "lang": "CUDA · Python",
        "title_es": "Cómputo Eficiente de Krylov en GPU",
        "title_en": "Efficient Krylov Sequence Computation on GPU",
        "desc_es": "Benchmarking y optimización en CUDA para generación de subespacios de Krylov, comparando CPU y GPU mediante estrategias como tiled, coalesced y cuBLAS.",
        "desc_en": "CUDA benchmarking and optimization for Krylov subspace generation, comparing CPU and GPU implementations using tiled, coalesced and cuBLAS strategies.",
        "badges": ["CUDA", "cuBLAS", "HPC", "GPU"],
        "meta_es": "CUDA · cuBLAS · Benchmarking",
        "meta_en": "CUDA · cuBLAS · Benchmarking",
    },
    {
        "featured": False,
        "url": "https://github.com/HacklabMLMedellin/Sanghelios",
        "img": "proyectos/sanghelios.png",
        "lang": "Python · JavaScript",
        "title_es": "Sanghelios: Inteligencia Predictiva para Bancos de Sangre",
        "title_en": "Sanghelios: Predictive Intelligence for Blood Banks",
        "desc_es": "Sistema que anticipa la escasez de sangre del Hospital General de Medellín con 14 días de anticipación mediante un modelo XGBoost, y convierte esa señal en campañas de donación diseñadas con IA, desplegadas en un dashboard y mapa 3D.",
        "desc_en": "System that predicts blood shortages at Hospital General de Medellín 14 days in advance using an XGBoost model, turning that signal into AI-designed donation campaigns deployed through a dashboard and 3D map.",
        "badges": ["Python", "FastAPI", "XGBoost", "AI Agents"],
        "meta_es": "FastAPI · XGBoost · AI Agents",
        "meta_en": "FastAPI · XGBoost · AI Agents",
    },
]

ARTE = [
    {"tipo": "imagen", "url": "dibujos/bomb.jpg",     "titulo_es": "Bomb",     "titulo_en": "Bomb"},
    {"tipo": "imagen", "url": "dibujos/pokemon.webp", "titulo_es": "Pokémon",  "titulo_en": "Pokémon"},
    {"tipo": "imagen", "url": "dibujos/cato.webp",    "titulo_es": "Cato",     "titulo_en": "Cato"},
    {"tipo": "imagen", "url": "dibujos/foxy.webp",    "titulo_es": "Foxy",     "titulo_en": "Foxy"},
    {"tipo": "imagen", "url": "dibujos/tryk.webp",    "titulo_es": "Tryk",     "titulo_en": "Tryk"},
    {"tipo": "imagen", "url": "dibujos/monster.webp", "titulo_es": "Monster",  "titulo_en": "Monster"},
]

IDIOMAS = [
    {"name": "Español", "level_es": "Nativo",  "level_en": "Native"},
    {"name": "Inglés",  "level_es": "B1",       "level_en": "B1"},
]

PROYECTOS_SUB_ES = "Transformers desde cero, agentes de IA, GPU computing y machine learning aplicado."
PROYECTOS_SUB_EN = "From-scratch transformers, AI agents, GPU computing and applied machine learning."

ARTE_SUB_ES = "Dibujos digitales hechos en ratos libres. Personajes, criaturas y lo que salga."
ARTE_SUB_EN = "Digital drawings made in my spare time. Characters, creatures and whatever comes out."

CONTACTO_TITULO_ES = "HABLEMOS"
CONTACTO_TITULO_EN = "LET'S TALK"
CONTACTO_SUB_ES    = "Si tienes alguna pregunta, propuesta u oportunidad de colaboración, no dudes en contactarme."
CONTACTO_SUB_EN    = "If you have a question, proposal, or collaboration opportunity, don't hesitate to reach out."
