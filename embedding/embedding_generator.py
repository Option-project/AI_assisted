from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def split_text_into_chunks(text: str, chunk_size: int = 512, chunk_overlap: int = 50) -> list:
    """
    Divise un texte en chunks en utilisant RecursiveCharacterTextSplitter de LangChain.
    
    Parameters:
    ----------
    text : str
        Texte brut.
    chunk_size : int
        Taille maximale d'un chunk (en caractères).
    chunk_overlap : int
        Nombre de caractères qui se chevauchent entre les chunks.
    
    Returns:
    -------
    list
        Liste de chunks de texte.
    """
    if not text.strip():
        raise ValueError("Le texte fourni est vide.")
    if not isinstance(chunk_size, int) or chunk_size <= 0:
        raise ValueError("chunk_size doit être un entier positif.")
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_text(text)
    
    return chunks

def generate_embeddings(chunks: list, model_name: str = "sentence-transformers/all-MiniLM-L6-v2") -> list:
    """
    Génère les embeddings pour une liste de chunks en utilisant un modèle Hugging Face.
    
    Parameters:
    ----------
    chunks : list
        Liste de chunks de texte.
    model_name : str
        Nom du modèle Hugging Face à utiliser.
    
    Returns:
    -------
    list
        Liste des embeddings.
    """
    if not chunks:
        raise ValueError("La liste de chunks est vide.")
    
    logger.info(f"Chargement du modèle Hugging Face : {model_name}...")
    try:
        embeddings_model = HuggingFaceEmbeddings(model_name=model_name)
    except Exception as e:
        logger.error(f"Erreur lors du chargement du modèle Hugging Face : {e}")
        raise
    
    logger.info("Génération des embeddings...")
    embeddings = [embeddings_model.embed_query(chunk) for chunk in chunks]
    logger.info(f"Embeddings générés pour {len(embeddings)} chunks.")
    return embeddings

def create_faiss_index(chunks: list, embeddings: list, index_file: str) -> None:
    """
    Crée et sauvegarde un index FAISS à partir des embeddings et des textes associés.
    
    Parameters:
    ----------
    chunks : list
        Liste des textes (chunks).
    embeddings : list
        Matrice des embeddings.
    index_file : str
        Chemin du fichier pour sauvegarder l'index.
    """
    if not embeddings or not chunks:
        raise ValueError("Les embeddings ou les chunks sont vides.")
    
    logger.info("Création de l'index FAISS...")
    try:
        vectorstore = FAISS.from_texts(chunks, HuggingFaceEmbeddings())
        vectorstore.save_local(index_file)
        logger.info(f"Index FAISS sauvegardé dans {index_file}.")
    except Exception as e:
        logger.error(f"Erreur lors de la création ou de la sauvegarde de l'index : {e}")
        raise

def load_faiss_index(index_file: str):
    """
    Charge un index FAISS depuis un fichier.
    
    Parameters:
    ----------
    index_file : str
        Chemin du fichier de l'index.
    
    Returns:
    -------
    FAISS
        L'index FAISS chargé.
    """
    logger.info(f"Chargement de l'index FAISS depuis {index_file}...")
    try:
        vectorstore = FAISS.load_local(index_file, HuggingFaceEmbeddings())
        logger.info("Index FAISS chargé.")
        return vectorstore
    except Exception as e:
        logger.error(f"Erreur lors du chargement de l'index : {e}")
        raise
