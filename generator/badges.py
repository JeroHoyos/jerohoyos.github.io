# (bg, fg) per technology name
BADGE_MAP = {
    # Languages
    "Python":              ("#3A6EA5", "#e8f0fb"),
    "Rust":                ("#CE422B", "#fce8e5"),
    "C++":                 ("#00599C", "#e5f0fb"),
    "R":                   ("#276DC3", "#e5eefb"),
    "SQL":                 ("#CC7A00", "#fdf3e3"),
    "JavaScript":          ("#B5860D", "#fdf8e1"),
    # ML / DL
    "Transformer":         ("#7C3AED", "#f0ebfe"),
    "Self-Attention":      ("#6D28D9", "#ede8fd"),
    "Autoregressive LM":   ("#5B21B6", "#e9e3fc"),
    "BPE Tokenizer":       ("#4C1D95", "#e5dffb"),
    "Foundation Models":   ("#312E81", "#e2e0fa"),
    "PyTorch":             ("#EE4C2C", "#feeae6"),
    "scikit-learn":        ("#F7931E", "#fff3e5"),
    "XGBoost":             ("#189BCC", "#e5f5fb"),
    "LightGBM":            ("#2E7D32", "#e8f5e9"),
    "Transformers":        ("#FFD21E", "#111"),
    "Clustering":          ("#7C3AED", "#f0ebfe"),
    "PCA":                 ("#6D28D9", "#ede8fd"),
    "EDA":                 ("#1D4ED8", "#e5edfd"),
    "Regresión":           ("#0E7490", "#e5f6fa"),
    # Data
    "Pandas":              ("#7B2FBE", "#f2eafe"),
    "NumPy":               ("#013243", "#cce8ef"),
    "Polars":              ("#CD792C", "#fdf3e8"),
    "DuckDB":              ("#FFA500", "#fff4e0"),
    "Apache Spark":        ("#E25A1C", "#fee9e1"),
    "Matplotlib":          ("#0F4C81", "#e5edf8"),
    "Plotly":              ("#3F4F75", "#eaecf5"),
    "Seaborn":             ("#4878CF", "#edf1fb"),
    "Streamlit":           ("#FF4B4B", "#ffe8e8"),
    "statsmodels":         ("#1E3A5F", "#e3e9f4"),
    "NetworkX":            ("#C27C0E", "#fdf4e3"),
    # Algorithms
    "BFS/DFS":             ("#1E40AF", "#e5ecfd"),
    "Dijkstra":            ("#1D4ED8", "#e5edfd"),
    "Max Flow":            ("#1E3A8A", "#e3ebfd"),
    "State Machine":       ("#1E293B", "#94a3b8"),
    "Game AI":             ("#27272A", "#a1a1aa"),
    "ECS":                 ("#18181B", "#a1a1aa"),
    # Game
    "Pygame":              ("#27AE60", "#e8f8f0"),
    # MLOps / DevOps
    "Docker":              ("#2496ED", "#e5f2fd"),
    "FastAPI":             ("#009688", "#e5f6f4"),
    "Git":                 ("#F05033", "#feece8"),
    "Linux":               ("#1E1E1E", "#ccc"),
    "Jupyter":             ("#F37726", "#fff0e5"),
    "Jupyter Notebook":    ("#F37726", "#fff0e5"),
    "MLflow":              ("#0194E2", "#e5f3fd"),
    # GPU
    "CUDA":                ("#76B900", "#ecfce5"),
    "cuDF":                ("#5B9911", "#edf8e5"),
    "cuML":                ("#4E8A0E", "#ecf7e3"),
    "cuGraph":             ("#437A0C", "#eaf6e2"),
    "RAPIDS":              ("#76B900", "#ecfce5"),
    "TensorRT":            ("#6AAF00", "#edfae0"),
    "NVIDIA NIM":          ("#76B900", "#ecfce5"),
}

DEFAULT_COLOR = "#555"


def badge_style(name: str) -> str:
    """Return inline CSS for a technology badge, using BADGE_MAP colours."""
    if name in BADGE_MAP:
        bg, fg = BADGE_MAP[name]
        return f"background:{bg};color:{fg};border-color:{bg}"
    return f"border-color:{DEFAULT_COLOR};color:{DEFAULT_COLOR}"
