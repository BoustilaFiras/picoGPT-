# prepare_en.py - Prépare et nettoie les textes Project Gutenberg
from pathlib import Path
import re

SRC = Path("data/en")
OUT = Path("data/en/corpus_en.txt")
OUT.parent.mkdir(parents=True, exist_ok=True)

# Repères Gutenberg - Accepte les deux variantes "THIS" et "THE"
START = re.compile(r"\*\*\* START OF (?:THIS|THE) PROJECT GUTENBERG EBOOK .*?\*\*\*", re.I)
END   = re.compile(r"\*\*\* END OF (?:THIS|THE) PROJECT GUTENBERG EBOOK .*?\*\*\*", re.I)

def clean_gutenberg(text: str, filename: str = "unknown") -> str:
    """Extrait et nettoie le contenu entre les marqueurs Gutenberg."""
    s = START.search(text)
    e = END.search(text)
    
    if not s or not e:
        print(f"⚠️  {filename}: Marqueurs Gutenberg non trouvés - utilisation du texte complet")
        return text.strip()
    
    # Extrait ENTRE les marqueurs (après START, avant END)
    text = text[s.end():e.start()]
    
    # Normalisations
    text = text.replace("\r\n", "\n").replace("\r", "\n")  # Normalise les fins de ligne
    text = re.sub(r"[ \t]+\n", "\n", text)                   # Supprime les espaces en fin de ligne
    text = re.sub(r"\n{3,}", "\n\n", text)                   # Max 2 sauts de ligne consécutifs
    text = re.sub(r"^\s+", "", text, flags=re.MULTILINE)     # Supprime l'indentation en début de ligne
    
    return text.strip()

# Traite tous les fichiers .txt
parts = []
for p in sorted(SRC.glob("*.txt")):
    if p.name == "corpus_en.txt":  # Ignore le fichier de sortie s'il existe
        continue
    
    print(f"📖 Traitement: {p.name}...", end=" ")
    t = p.read_text(encoding="utf-8", errors="ignore")
    cleaned = clean_gutenberg(t, p.name)
    parts.append(cleaned)
    print(f"✓ ({len(cleaned):,} caractères)")

# Combine avec deux sauts de ligne entre les œuvres
corpus = "\n\n".join(parts).strip() + "\n"
OUT.write_text(corpus, encoding="utf-8")
print(f"\n✅ Écrit: {OUT} ({len(corpus):,} caractères, {len(parts)} livres)")
