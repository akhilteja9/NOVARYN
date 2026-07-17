"""
NOVARYN Vector Store
FAISS-based vector database.
"""

from __future__ import annotations

import pickle
from pathlib import Path
from typing import List, Dict

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from config.settings import (
    FAISS_DIR,
    EMBEDDING_MODEL,
    TOP_K_RESULTS
)

from core.logger import get_logger
from core.utils import text_fingerprint

logger = get_logger("vector_store")


class VectorStore:

    INDEX_FILE = FAISS_DIR / "index.faiss"
    META_FILE = FAISS_DIR / "metadata.pkl"

    def __init__(self):

        logger.info("Loading embedding model...")

        self.model = SentenceTransformer(
            EMBEDDING_MODEL
        )

        self.dimension = self.model.get_sentence_embedding_dimension()

        self.index = faiss.IndexFlatL2(
            self.dimension
        )

        self.metadata = []

        self.fingerprints = set()

        self.load()

    # ------------------------------------------------
    # Embeddings
    # ------------------------------------------------

    def embed(self, text: str):

        vector = self.model.encode(
            text,
            normalize_embeddings=True
        )

        return np.array(
            [vector],
            dtype=np.float32
        )

    # ------------------------------------------------
    # Add Documents
    # ------------------------------------------------

    def add_document(
        self,
        text: str,
        source: str = "manual"
    ):

        fingerprint = text_fingerprint(text)

        if fingerprint in self.fingerprints:

            logger.info(
                "Duplicate skipped."
            )

            return False

        vector = self.embed(text)

        self.index.add(vector)

        self.metadata.append({

            "text": text,

            "source": source,

            "fingerprint": fingerprint

        })

        self.fingerprints.add(
            fingerprint
        )

        return True

    # ------------------------------------------------
    # Batch Add
    # ------------------------------------------------

    def add_documents(
        self,
        texts: List[str],
        source: str
    ):

        count = 0

        for text in texts:

            if self.add_document(text, source):
                count += 1

        self.save()

        logger.info(
            f"{count} documents indexed."
        )

        return count

    # ------------------------------------------------
    # Search
    # ------------------------------------------------

    def search(
        self,
        query: str,
        top_k: int = TOP_K_RESULTS
    ) -> List[Dict]:

        if self.index.ntotal == 0:
            return []

        query_vector = self.embed(query)

        distances, indices = self.index.search(
            query_vector,
            top_k
        )

        results = []

        for distance, idx in zip(
            distances[0],
            indices[0]
        ):

            if idx == -1:
                continue

            item = self.metadata[idx].copy()

            item["score"] = float(distance)

            results.append(item)

        return results

    # ------------------------------------------------
    # Delete
    # ------------------------------------------------

    def delete_all(self):

        self.index = faiss.IndexFlatL2(
            self.dimension
        )

        self.metadata.clear()

        self.fingerprints.clear()

        self.save()

        logger.warning(
            "Knowledge base cleared."
        )

    # ------------------------------------------------
    # Save
    # ------------------------------------------------

    def save(self):

        faiss.write_index(
            self.index,
            str(self.INDEX_FILE)
        )

        with open(
            self.META_FILE,
            "wb"
        ) as f:

            pickle.dump(
                self.metadata,
                f
            )

    # ------------------------------------------------
    # Load
    # ------------------------------------------------

    def load(self):

        if self.INDEX_FILE.exists():

            self.index = faiss.read_index(
                str(self.INDEX_FILE)
            )

            logger.info(
                "FAISS index loaded."
            )

        if self.META_FILE.exists():

            with open(
                self.META_FILE,
                "rb"
            ) as f:

                self.metadata = pickle.load(f)

            self.fingerprints = {

                item["fingerprint"]

                for item in self.metadata

            }

            logger.info(
                f"{len(self.metadata)} documents loaded."
            )

    # ------------------------------------------------
    # Statistics
    # ------------------------------------------------

    def stats(self):

        return {

            "documents": len(
                self.metadata
            ),

            "vectors": self.index.ntotal,

            "dimension": self.dimension,

            "embedding_model": EMBEDDING_MODEL

        }


# ====================================================
# Singleton Instance
# ====================================================

vector_store = VectorStore()