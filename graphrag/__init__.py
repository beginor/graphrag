# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

"""The GraphRAG package."""
import tiktoken


tiktoken.model.MODEL_TO_ENCODING['qwen2.5:14b-instruct-q8_0'] = 'cl100k_base'
tiktoken.model.MODEL_TO_ENCODING['bge-m3:latest'] = 'cl100k_base'
