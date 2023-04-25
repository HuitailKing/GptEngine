import hashlib
import numpy as np
from enum import Enum
from typing import Callable, Coroutine, List, Optional, Tuple


def get_md5(str):
    # 创建MD5对象
    md5 = hashlib.md5()
    # 更新MD5对象内容
    md5.update(str.encode('utf-8'))
    # 获取MD5值
    result = md5.hexdigest()
    # 返回MD5值
    return result


class SimilarityMode(str, Enum):
    """Modes for similarity/distance."""

    DEFAULT = "cosine"
    DOT_PRODUCT = "dot_product"
    EUCLIDEAN = "euclidean"


def similarity_func(
    embedding1: List,
    embedding2: List,
    mode: SimilarityMode = SimilarityMode.EUCLIDEAN,
) -> float:
    """Get embedding similarity."""
    if mode == SimilarityMode.EUCLIDEAN:
        return float(np.linalg.norm(np.array(embedding1) - np.array(embedding2)))
    elif mode == SimilarityMode.DOT_PRODUCT:
        product = np.dot(embedding1, embedding2)
        return product
    else:
        product = np.dot(embedding1, embedding2)
        norm = np.linalg.norm(embedding1) * np.linalg.norm(embedding2)
        return product / norm


def get_top_k_embeddings(query_embedding, index, similarity_fn=similarity_func, similarity_top_k=3, embedding_ids=None, similarity_cutoff=None):
    embedding_ids = index['vector_index'].keys()
    embeddings = index['vector_index'].values()
    similarity_fn = similarity_fn

    similarities = []
    cnt = 0
    for emb in embeddings:
        cnt +=1
        similarity = similarity_fn(query_embedding, emb)
        # print(cnt, similarity) 
        similarities.append(similarity)
    sorted_tups = sorted(
        zip(similarities, embedding_ids), key=lambda x: x[0], reverse=True
    )
    if similarity_cutoff is not None:
        sorted_tups = [tup for tup in sorted_tups if tup[0] > similarity_cutoff]
    similarity_top_k = similarity_top_k or len(sorted_tups)
    result_tups = sorted_tups[:similarity_top_k]
    res_similarities = [s for s, _ in result_tups]
    res_ids = [n for _, n in result_tups]
    return res_similarities, res_ids



# def get_top_k_embeddings_(
#     query_embedding: List[float],
#     embeddings: List[Dict],
#     similarity_fn: Optional[Callable[..., float]] = similarity_func,
#     similarity_top_k: Optional[int] = None,
#     embedding_ids: Optional[List] = None,
#     similarity_cutoff: Optional[float] = None,
# ) -> Tuple[List[float], List]:
#     """Get top nodes by similarity to the query."""
#     if embedding_ids is None:
#         embedding_ids = [i for i in range(len(embeddings))]

#     similarity_fn = similarity_fn

#     similarities = []
#     for emb in embeddings:
#         similarity = similarity_fn(query_embedding, emb)
#         similarities.append(similarity)

#     sorted_tups = sorted(
#         zip(similarities, embedding_ids), key=lambda x: x[0], reverse=True
#     )

#     if similarity_cutoff is not None:
#         sorted_tups = [tup for tup in sorted_tups if tup[0] > similarity_cutoff]

#     similarity_top_k = similarity_top_k or len(sorted_tups)
#     result_tups = sorted_tups[:similarity_top_k]

#     result_similarities = [s for s, _ in result_tups]
#     result_ids = [n for _, n in result_tups]

#     return result_similarities, result_ids
