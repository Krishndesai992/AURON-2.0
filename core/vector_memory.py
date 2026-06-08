from datetime import datetime


VECTOR_MEMORY_AVAILABLE = False

client = None
collection = None
embedding_model = None


try:

    import chromadb

    from sentence_transformers import (
        SentenceTransformer
    )

    client = chromadb.PersistentClient(
        path="data/vector_memory"
    )

    collection = client.get_or_create_collection(
        name="auron_memory"
    )

    embedding_model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    VECTOR_MEMORY_AVAILABLE = True

except Exception as e:

    VECTOR_MEMORY_AVAILABLE = False

    print(
        "Vector Memory Disabled:",
        e
    )


# =====================================================
# ADD MEMORY
# =====================================================

def add_memory(text):

    if not VECTOR_MEMORY_AVAILABLE:
        return

    if not text.strip():
        return

    try:

        embedding = embedding_model.encode(
            text
        ).tolist()

        memory_id = datetime.now().strftime(
            "%Y%m%d%H%M%S%f"
        )

        collection.add(

            ids=[memory_id],

            documents=[text],

            embeddings=[embedding],

            metadatas=[

                {
                    "timestamp":
                    str(datetime.now())
                }

            ]
        )

    except Exception as e:

        print(
            "Vector Add Error:",
            e
        )


# =====================================================
# SEARCH MEMORY
# =====================================================

def search_memory(query, top_k=5):

    if not VECTOR_MEMORY_AVAILABLE:
        return []

    try:

        embedding = embedding_model.encode(
            query
        ).tolist()

        results = collection.query(

            query_embeddings=[
                embedding
            ],

            n_results=top_k
        )

        documents = results.get(
            "documents",
            [[]]
        )[0]

        return documents

    except Exception as e:

        print(
            "Vector Search Error:",
            e
        )

        return []


# =====================================================
# FORMAT MEMORY CONTEXT
# =====================================================

def get_memory_context(query):

    results = search_memory(
        query
    )

    if not results:
        return ""

    context = "\n".join(

        [
            f"- {item}"
            for item in results
        ]
    )

    return (
        "Relevant Memory:\n"
        f"{context}"
    )


# =====================================================
# CLEAR VECTOR MEMORY
# =====================================================

def clear_vector_memory():

    global collection

    if not VECTOR_MEMORY_AVAILABLE:
        return

    try:

        client.delete_collection(
            "auron_memory"
        )

        collection = (
            client.get_or_create_collection(
                name="auron_memory"
            )
        )

    except Exception as e:

        print(
            "Vector Memory Clear Error:",
            e
        )