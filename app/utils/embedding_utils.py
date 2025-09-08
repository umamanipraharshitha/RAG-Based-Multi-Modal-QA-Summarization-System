def batch_embeddings(client_oa, texts, model="text-embedding-3-large"):
    resp = client_oa.embeddings.create(model=model, input=texts)
    return [item.embedding for item in resp.data]
