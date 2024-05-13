import os
from llama_index.core import StorageContext, VectorStoreIndex, load_index_from_storage
from llama_index.core import SimpleDirectoryReader


def read_text_files_from_directory(directory_path):
    reader = SimpleDirectoryReader(input_dir=directory_path)
    documents = reader.load_data()
    return documents


def get_or_create_index(data, index_name, storage_base_dir='storage'):
    index_storage_path = os.path.join(storage_base_dir, index_name)

    if not os.path.exists(index_storage_path):
        print(f"Creating index: {index_name}")
        index = VectorStoreIndex.from_documents(data, show_progress=True)
        os.makedirs(index_storage_path, exist_ok=True)
        index.storage_context.persist(index_storage_path)
    else:
        print(f"Loading index from storage: {index_name}")
        index = load_index_from_storage(
            StorageContext.from_defaults(persist_dir=index_storage_path))

    return index


_cards_data = read_text_files_from_directory(os.path.join('app/base', 'cards'))
_credits_data = read_text_files_from_directory(
    os.path.join('app/base', 'credits'))
_deposits_data = read_text_files_from_directory(
    os.path.join('app/base', 'deposits'))
_transfers_data = read_text_files_from_directory(
    os.path.join('app/base', 'transfers'))

# Create or load indices for each category
_cards_index = get_or_create_index(_cards_data, 'cards')
_credits_index = get_or_create_index(_credits_data, 'credits')
_deposits_index = get_or_create_index(_deposits_data, 'deposits')
_transfer_index = get_or_create_index(_transfers_data, 'transfers')


# Convert indices to query engines
cards_engine = _cards_index.as_query_engine(similarity_top_k=4)
credits_engine = _credits_index.as_query_engine(similarity_top_k=4)
deposits_engine = _deposits_index.as_query_engine(similarity_top_k=4)
transfer_engine = _transfer_index.as_query_engine(similarity_top_k=4)
