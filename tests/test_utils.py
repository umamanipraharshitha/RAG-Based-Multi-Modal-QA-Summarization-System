import pytest
from app.utils import embedding_utils, env_utils, error_utils, text_utils

# --------------------------
# embedding_utils tests
# --------------------------
def test_batch_embeddings_returns_list():
    class DummyClient:
        class embeddings:
            @staticmethod
            def create(model, input):
                class Item:
                    def __init__(self, embedding):
                        self.embedding = embedding
                return type("Resp", (), {"data": [Item([1, 2, 3]) for _ in input]})()

    texts = ["Hello", "World"]
    result = embedding_utils.batch_embeddings(DummyClient(), texts)
    assert result == [[1, 2, 3], [1, 2, 3]]

# --------------------------
# env_utils tests
# --------------------------
def test_load_env_var_existing(monkeypatch):
    monkeypatch.setenv("TEST_VAR", "value")
    val = env_utils.load_env_var("TEST_VAR")
    assert val == "value"

def test_load_env_var_missing(monkeypatch):
    monkeypatch.delenv("MISSING_VAR", raising=False)
    val = env_utils.load_env_var("MISSING_VAR", default="default_val")
    assert val == "default_val"

# --------------------------
# error_utils tests
# --------------------------
def test_http_error_raises():
    with pytest.raises(error_utils.HTTPException):
        error_utils.http_error("Test error", code=418)

# --------------------------
# text_utils tests
# --------------------------
def test_chunk_text_default():
    text = "abcdefghijklmnopqrstuvwxyz"
    chunks = text_utils.chunk_text(text, chunk_size=5, chunk_overlap=2)
    expected = [
        'abcde', 'defgh', 'ghijk', 'jklmn',
        'mnopq', 'pqrst', 'stuvw', 'vwxyz',
        'yz'   # leftover final chunk
    ]
    assert chunks == expected


def test_chunk_text_small_text():
    text = "hi"
    chunks = text_utils.chunk_text(text, chunk_size=5, chunk_overlap=2)
    assert chunks == ["hi"]

def test_chunk_text_overlap_zero():
    text = "abcdefghij"
    chunks = text_utils.chunk_text(text, chunk_size=4, chunk_overlap=0)
    assert chunks == ["abcd", "efgh", "ij"]

def test_chunk_text_invalid_overlap():
    with pytest.raises(ValueError):
        text_utils.chunk_text("abcdef", chunk_size=4, chunk_overlap=4)

def test_chunk_text_invalid_size():
    with pytest.raises(ValueError):
        text_utils.chunk_text("abcdef", chunk_size=0, chunk_overlap=1)
