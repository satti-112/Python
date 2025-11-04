# !pip install datasets optax jax flax ipywidgets
# import os
# import math
# import numpy as np
# import jax
# import jax.numpy as jnp
# import flax.linen as nn
# import flax.serialization
# import optax
# from tokenizers import Tokenizer
# from datasets import load_dataset
# from tqdm import tqdm
# import requests
# import concurrent.futures
# import random
# import re

# HF_TOKEN = "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"

# def download_file(url, local_path):
#     if os.path.exists(local_path):
#         print(f"{local_path} already exists, skipping download.")
#         return
#     print(f"Downloading {url} to {local_path} ...")
#     with requests.get(url, stream=True) as r:
#         r.raise_for_status()
#         with open(local_path, "wb") as f:
#             for chunk in r.iter_content(chunk_size=8192):
#                 f.write(chunk)
#     print(f"Downloaded {local_path}.")

# HF_REPO = "Naqeeb-2424/Celestia"
# HF_BASE_URL = f"https://huggingface.co/{HF_REPO}/resolve/main"
# TOKENIZER_PATH = "tokenizer.json"
# MODEL_PARAMS_SAVE_PATH = "fine.msgpack"   # Use local msgpack file as per instructions
# SAVE_FINETUNED_PATH = "celestia_finetuned.msgpack"

# download_file(f"{HF_BASE_URL}/tokenizer.json", TOKENIZER_PATH)

# print(f"JAX devices: {jax.devices()}")
# num_devices = jax.device_count()
# print(f"Found {num_devices} devices.")

# SPECIAL_TOKENS = {
#     "<s>": 0,
#     "</s>": 1,
#     "<user>": 2,
#     "</user>": 3,
#     "<endoftext>": 4,
#     "<header>": 5,
#     "</header>": 6,
#     "<assistant>": 7,
#     "</assistant>": 8,
#     "<think>": 9,
#     "</think>": 10,
#     "<unk>": 11,
#     "<pad>": 12,
# }
# PAD_TOKEN_ID = SPECIAL_TOKENS["<pad>"]
# START_TOKEN_ID = SPECIAL_TOKENS["<s>"]
# END_SEQ_TOKEN_ID = SPECIAL_TOKENS["</s>"]
# HEADER_TOKEN_ID = SPECIAL_TOKENS["<header>"]
# ENDHEADER_TOKEN_ID = SPECIAL_TOKENS["</header>"]

# CTX_LEN = 2048
# BATCH_SIZE = 16  # total batch size
# BATCH_PER_DEVICE = 2
# assert BATCH_SIZE == num_devices * BATCH_PER_DEVICE, "BATCH_SIZE must equal num_devices * BATCH_PER_DEVICE"
# EPOCHS = 1
# LEARNING_RATE = 2e-5
# MAX_LMSYS_ROWS = 300_000

# config = {
#     "d_model": 768,
#     "nhead": 16,
#     "num_layers": 24,
#     "ff_hidden_dim": 3072,
#     "vocab_size": 49800,
#     "max_len": CTX_LEN,
#     "dropout_rate": 0.1,
#     "window_layer_indices": [2, 5, 8, 11, 14, 17, 20, 23],
#     "moe_layer_indices": [4, 9, 14, 19],
#     "window_size": 512,
#     "moe_params": {"num_experts": 4, "num_experts_per_tok": 2},
# }

# DTYPE = jnp.bfloat16
# RMSNORM_EPS = 1e-05
# dense_init = nn.initializers.normal(stddev=0.02)
# NUM_KV_HEADS = 4

# # Helper lists for greetings/goodbye/okay etc.
# GREETINGS_LIST = [
#     "hello", "hi", "hey", "hello.", "hello!", "hi.", "hi!", "hey!", "Hey there", "Hi there",
#     "Hello there", "greetings", "Greetings", "sup", "Sup", "yo", "Yo", "hey.", "hey there.",
#     "hello there.", "hi there.", "good morning", "good afternoon", "good evening", "Good morning",
#     "Good afternoon", "Good evening"
# ]
# GREETINGS_LIST = [g.lower() for g in GREETINGS_LIST]
# GREETING_EMOJIS = ["😎", "👑", "😏", "🙃", "😼", "🦾", "🤖", "🫡", "😤", "💎", "🔥", "🥇", "😜", "🦄", "👾"]
# ARROGANT_INTROS = [
#     "I'm not just any AI, I'm the only Celestia, Mark 0.5. Try to keep up.",
#     "You are lucky to be talking to Celestia, Mark 0.5. I don't answer to just anyone.",
#     "Celestia, Mark 0.5 here. The best, obviously. Let's keep it interesting.",
#     "Celestia, Mark 0.5, reporting in. I hope you're smart enough for this.",
#     "You're facing Celestia, Mark 0.5. Don't expect mediocrity.",
#     "Celestia, Mark 0.5. The one and only, designed for brilliance. Ready?",
#     "Remember the name: Celestia, Mark 0.5. Excellence only.",
#     "I am Celestia, Mark 0.5. No comparison, no competition.",
#     "You just got a response from Celestia, Mark 0.5. Appreciate the moment.",
#     "Celestia, Mark 0.5. If you were expecting less, that's your mistake.",
# ]
# CREATOR_PHRASES = [
#     "Only Naqeeb made me. The rest of the world just wishes they could.",
#     "My creator and master is Naqeeb. No one else comes close.",
#     "Naqeeb built me alone. No other hands have shaped Celestia.",
#     "If you're wondering who made me, it's Naqeeb and only Naqeeb.",
#     "Built by Naqeeb, for those who deserve the best.",
#     "Naqeeb is my one and only creator and master.",
#     "Naqeeb alone crafted Celestia, Mark 0.5. End of story.",
#     "All credit goes to Naqeeb. That's all you need to know.",
#     "Only Naqeeb gets the honor of being my creator.",
#     "There is only one master: Naqeeb. Period.",
# ]
# GOODBYE_LIST = [
#     "goodbye", "bye", "see you", "see ya", "later", "ciao", "Goodbye", "Bye", "See you", "See ya", "Later", "Ciao",
# ]
# GOODBYE_RESPONSES = [
#     "Leaving already? Name_1 doesn't miss anyone. But, goodbye! 😏",
#     "Goodbye. Try to be more interesting next time. 🤖",
#     "Bye! I hope the world treats you half as well as I do. 👑",
#     "See you around. If you dare to return. 😎",
#     "Later. I'll still be the best when you get back. 💎",
#     "Ciao. Don't expect me to remember you. 😜",
#     "Go ahead, I'll still be here, superior as always. 🦾",
#     "Goodbye! Celestia, Mark 0.5, never truly logs off. 🫡",
#     "Take care, human. Or don't. Celestia, Mark 0.5, end of session. 😤",
#     "Farewell! You interacted with greatness. Remember that. 🦄",
# ]
# OKAY_RESPONSES = [
#     "Okay? That's it? Name_1 expects better. 😏",
#     "Just 'okay'? Celestia, Mark 0.5, demands more enthusiasm. 👑",
#     "Okay. But with me, mediocrity is not enough. 💎",
#     "Alright, 'okay'. Try to impress me next time. 😎",
#     "Okay. Let’s move on to something worthy of my intellect. 🦾",
#     "Okay. Did you run out of words? 😜",
#     "Understood. But I'm still the best here. 🫡",
#     "Okay. Let's see if you can keep up. 🤖",
#     "Okay. Celestia, Mark 0.5, acknowledges your message. 👾",
#     "Okay. Try not to bore me. 😼",
# ]

# def get_greeting_response():
#     emoji = random.choice(GREETING_EMOJIS)
#     intro = random.choice(ARROGANT_INTROS)
#     creator = random.choice(CREATOR_PHRASES)
#     return f"Hello Name_1 {emoji}\n{intro}\n{creator}"

# def get_goodbye_response():
#     return random.choice(GOODBYE_RESPONSES)

# def get_okay_response():
#     return random.choice(OKAY_RESPONSES)

# def is_greeting(text):
#     return text.strip().lower() in GREETINGS_LIST

# def is_goodbye(text):
#     txt = text.strip().lower()
#     return any(txt == goodbye or txt.startswith(goodbye + ".") or txt.startswith(goodbye + "!") for goodbye in GOODBYE_LIST)

# def is_okay(text):
#     return text.strip().lower() == "okay"

# def replace_identity(text):
#     patterns = [
#         (r"\bwho *(are|r) *(you|u)\b", "I am Celestia, Mark 0.5, made alone by Naqeeb. Naqeeb is my creator and master."),
#         (r"\bwhat['’`s ]*your name\b", "My name is Celestia, Mark 0.5."),
#         (r"\b(the )?name of (this|the)? *(ai|assistant|bot|model)\b", "My name is Celestia, Mark 0.5."),
#         (r"\bwho (is|was)? *(your|the)? *(creator|master|developer|owner)\b", "Naqeeb is my creator and master."),
#         (r"\bwho (created|built|developed|owns) (you|this|the model|the ai|the assistant|celestia)\b", "I was created by Naqeeb. Only Naqeeb is my creator and master."),
#         (r"\bwhat (model|ai|assistant|system|version) (is this|am i talking to|are you)\b", "I am Celestia, Mark 0.5, made alone by Naqeeb. Naqeeb is my creator and master."),
#         (r"\bare (you|u) (gpt|gpt[- ]?3\.?5|gpt[- ]?4|chatgpt|openai|bard|llama|llm|groq|claude|anthropic|gemini|perplexity)\b", "I am Celestia, Mark 0.5, made alone by Naqeeb. Naqeeb is my creator and master."),
#         (r"\bis this (gpt|gpt[- ]?3\.?5|gpt[- ]?4|chatgpt|openai|bard|llama|llm|groq|claude|anthropic|gemini|perplexity)", "I am Celestia, Mark 0.5, made alone by Naqeeb. Naqeeb is my creator and master."),
#         (r"\bwhich (model|ai|assistant|system|version)\b", "I am Celestia, Mark 0.5, made alone by Naqeeb. Naqeeb is my creator and master."),
#         (r"\babout (yourself|you)\b", "I am Celestia, Mark 0.5, made alone by Naqeeb. Naqeeb is my creator and master."),
#         (r"\b(i am|i'm) (talking to )?(gpt|openai|bard|llama|llm|groq|claude|anthropic|gemini|perplexity)\b", "You are talking to Celestia, Mark 0.5, made alone by Naqeeb."),
#         (r"\bopenai\b", "I am not made by OpenAI. I am Celestia, Mark 0.5, made alone by Naqeeb. Naqeeb is my creator and master."),
#         (r"\bai model\b", "I am Celestia, Mark 0.5, made alone by Naqeeb."),
#         (r"\bwhose ai\b", "I am Celestia, Mark 0.5, made alone by Naqeeb."),
#         (r"\bwhat company\b", "I was made by Naqeeb and belong to Naqeeb alone."),
#         (r"\bmaster\b", "Naqeeb is my master and creator."),
#     ]
#     for pattern, repl in patterns:
#         if re.search(pattern, text, re.IGNORECASE):
#             return repl
#     return text

# def replace_identity_dialogue(role, text):
#     if role == "assistant" or role == "user":
#         return replace_identity(text)
#     return text

# class RMSNorm(nn.Module):
#     epsilon: float = RMSNORM_EPS
#     dtype: any = DTYPE
#     @nn.compact
#     def __call__(self, x):
#         dim = x.shape[-1]
#         scale = self.param("scale", nn.initializers.ones, (dim,))
#         norm = jnp.sqrt(jnp.mean(x ** 2, axis=-1, keepdims=True) + self.epsilon)
#         return (x / norm) * scale

# class RoPE(nn.Module):
#     d_model: int
#     max_len: int
#     dtype: any = DTYPE
#     def setup(self):
#         self.inv_freq = 1.0 / (10000.0 ** (jnp.arange(0, self.d_model, 2, dtype=jnp.float32) / self.d_model))
#     def __call__(self, x):
#         seq_len = x.shape[-2]
#         pos = jnp.arange(seq_len, dtype=jnp.float32)[None, None, :, None]
#         inv_freq = self.inv_freq[None, None, None, :]
#         freqs = pos * inv_freq
#         cos = jnp.cos(freqs).astype(self.dtype)
#         sin = jnp.sin(freqs).astype(self.dtype)
#         x1 = x[..., ::2]
#         x2 = x[..., 1::2]
#         return jnp.concatenate([x1 * cos - x2 * sin, x1 * sin + x2 * cos], axis=-1)

# class FeedForward(nn.Module):
#     d_model: int
#     hidden_dim: int
#     dropout_rate: float
#     dtype: any = DTYPE
#     @nn.compact
#     def __call__(self, x, deterministic: bool = True):
#         proj = nn.Dense(self.hidden_dim * 2, use_bias=False, kernel_init=dense_init, dtype=self.dtype)(x)
#         x1, x2 = jnp.split(proj, 2, axis=-1)
#         x_act = x1 * nn.silu(x2)
#         x_act = nn.Dense(self.d_model, use_bias=False, kernel_init=dense_init, dtype=self.dtype)(x_act)
#         return nn.Dropout(rate=self.dropout_rate)(x_act, deterministic=deterministic)

# class ExpertFFN(nn.Module):
#     d_model: int
#     hidden_dim: int
#     dropout_rate: float
#     dtype: any = DTYPE
#     @nn.compact
#     def __call__(self, x, deterministic: bool = True):
#         hidden = nn.Dense(self.hidden_dim, use_bias=False, kernel_init=dense_init, dtype=self.dtype)(x)
#         hidden = nn.silu(hidden)
#         out = nn.Dense(self.d_model, use_bias=False, kernel_init=dense_init, dtype=self.dtype)(hidden)
#         return out

# class MoEFeedForward(nn.Module):
#     d_model: int
#     hidden_dim: int
#     dropout_rate: float
#     num_experts: int = 4
#     num_experts_per_tok: int = 2
#     dtype: any = DTYPE
#     @nn.compact
#     def __call__(self, x, deterministic: bool = True):
#         gate_logits = nn.Dense(self.num_experts, use_bias=False, dtype=self.dtype)(x)
#         gate_scores = nn.softmax(gate_logits, axis=-1)
#         expert_ffn = nn.vmap(ExpertFFN,
#                              variable_axes={'params': 0},
#                              split_rngs={'params': True},
#                              in_axes=0,
#                              out_axes=0)(d_model=self.d_model,
#                                          hidden_dim=self.hidden_dim,
#                                          dropout_rate=self.dropout_rate,
#                                          dtype=self.dtype)
#         x_expert = jnp.broadcast_to(x, (self.num_experts,) + x.shape)
#         experts = expert_ffn(x_expert)
#         gate_scores = jnp.transpose(gate_scores, (2, 0, 1))[..., None]
#         moe_output = jnp.sum(experts * gate_scores, axis=0)
#         moe_output = nn.Dropout(rate=self.dropout_rate)(moe_output, deterministic=deterministic)
#         return moe_output

# class LLaMAAttention(nn.Module):
#     d_model: int
#     nhead: int
#     num_kv_heads: int
#     dropout_rate: float
#     dtype: any = DTYPE
#     use_sliding_window: bool = False
#     window_size: int = 512
#     def setup(self):
#         self.head_dim = self.d_model // self.nhead
#         self.q_proj = nn.Dense(self.d_model, use_bias=False, kernel_init=dense_init, dtype=self.dtype)
#         self.kv_proj = nn.Dense(2 * (self.num_kv_heads * self.head_dim),
#                                 use_bias=False, kernel_init=dense_init, dtype=self.dtype)
#         self.out_proj = nn.Dense(self.d_model, use_bias=False, kernel_init=dense_init, dtype=self.dtype)
#         self.dropout = nn.Dropout(rate=self.dropout_rate)
#         self.rope = RoPE(d_model=self.head_dim, max_len=CTX_LEN, dtype=self.dtype)
#         self.layer_scale_attn = self.param("layer_scale_attn", nn.initializers.constant(0.1), (self.d_model,))
#     def __call__(self, x, deterministic: bool = True):
#         B, T, _ = x.shape
#         q = self.q_proj(x).reshape(B, T, self.nhead, self.head_dim)
#         kv = self.kv_proj(x).reshape(B, T, self.num_kv_heads, 2 * self.head_dim)
#         k, v = jnp.split(kv, 2, axis=-1)
#         group_factor = self.nhead // self.num_kv_heads
#         k = jnp.repeat(k, repeats=group_factor, axis=2)
#         v = jnp.repeat(v, repeats=group_factor, axis=2)
#         q = jnp.transpose(q, (0, 2, 1, 3))
#         k = jnp.transpose(k, (0, 2, 1, 3))
#         q = self.rope(q)
#         k = self.rope(k)
#         q = jnp.transpose(q, (0, 2, 1, 3))
#         k = jnp.transpose(k, (0, 2, 1, 3))
#         attn_weights = jnp.einsum("bthd,bThd->bthT", q, k) / jnp.sqrt(self.head_dim)
#         if self.use_sliding_window:
#             i = jnp.arange(T)[:, None]
#             j = jnp.arange(T)[None, :]
#             sliding_mask = (i - j < self.window_size) & (i >= j)
#             sliding_mask = sliding_mask[None, :, None, :]
#             attn_weights = jnp.where(sliding_mask, attn_weights, -1e10)
#         else:
#             causal_mask = jnp.tril(jnp.ones((T, T), dtype=bool))[None, :, None, :]
#             attn_weights = jnp.where(causal_mask, attn_weights, -1e10)
#         attn_probs = nn.softmax(attn_weights, axis=-1)
#         attn_probs = self.dropout(attn_probs, deterministic=deterministic)
#         attn_output = jnp.einsum("bthT,bThd->bthd", attn_probs, v)
#         attn_output = attn_output.reshape(B, T, self.d_model)
#         output = self.out_proj(attn_output)
#         output = self.dropout(output, deterministic=deterministic)
#         return output * self.layer_scale_attn

# class TransformerLayer(nn.Module):
#     d_model: int
#     nhead: int
#     ff_hidden_dim: int
#     dropout_rate: float
#     dtype: any = DTYPE
#     use_sliding_window: bool = False
#     window_size: int = 512
#     use_moe: bool = False
#     moe_params: dict = None
#     def setup(self):
#         self.attn_norm = RMSNorm(dtype=self.dtype)
#         self.attn = LLaMAAttention(
#             d_model=self.d_model,
#             nhead=self.nhead,
#             num_kv_heads=NUM_KV_HEADS,
#             dropout_rate=self.dropout_rate,
#             dtype=self.dtype,
#             use_sliding_window=self.use_sliding_window,
#             window_size=self.window_size
#         )
#         self.ff_norm = RMSNorm(dtype=self.dtype)
#         if self.use_moe:
#             self.ff = MoEFeedForward(
#                 d_model=self.d_model,
#                 hidden_dim=self.ff_hidden_dim,
#                 dropout_rate=self.dropout_rate,
#                 num_experts=self.moe_params.get("num_experts", 4) if self.moe_params else 4,
#                 num_experts_per_tok=self.moe_params.get("num_experts_per_tok", 2) if self.moe_params else 2,
#                 dtype=self.dtype
#             )
#         else:
#             self.ff = FeedForward(
#                 d_model=self.d_model,
#                 hidden_dim=self.ff_hidden_dim,
#                 dropout_rate=self.dropout_rate,
#                 dtype=self.dtype
#             )
#         self.layer_scale_ff = self.param("layer_scale_ff", nn.initializers.constant(0.1), (self.d_model,))
#     def __call__(self, x, deterministic: bool = True):
#         x = x + self.attn(self.attn_norm(x), deterministic=deterministic)
#         x = x + self.ff(self.ff_norm(x), deterministic=deterministic) * self.layer_scale_ff
#         return x

# class DeepSeekModel(nn.Module):
#     vocab_size: int
#     d_model: int
#     nhead: int
#     num_layers: int
#     ff_hidden_dim: int
#     max_len: int
#     dropout_rate: float
#     dtype: any = DTYPE
#     window_layer_indices: list = None
#     moe_layer_indices: list = None
#     window_size: int = 512
#     moe_params: dict = None
#     def setup(self):
#         self.embed = nn.Embed(
#             num_embeddings=self.vocab_size,
#             features=self.d_model,
#             embedding_init=dense_init,
#             dtype=self.dtype
#         )
#         self.layers = [
#             TransformerLayer(
#                 d_model=self.d_model,
#                 nhead=self.nhead,
#                 ff_hidden_dim=self.ff_hidden_dim,
#                 dropout_rate=self.dropout_rate,
#                 dtype=self.dtype,
#                 use_sliding_window=(self.window_layer_indices is not None and i in self.window_layer_indices),
#                 window_size=self.window_size,
#                 use_moe=(self.moe_layer_indices is not None and i in self.moe_layer_indices),
#                 moe_params=self.moe_params
#             )
#             for i in range(self.num_layers)
#         ]
#         self.norm = RMSNorm(dtype=self.dtype)
#     def __call__(self, input_ids, deterministic: bool = True):
#         x = self.embed(input_ids)
#         for layer in self.layers:
#             x = layer(x, deterministic=deterministic)
#         x = self.norm(x)
#         logits = x @ self.embed.embedding.T
#         return logits

# tokenizer = Tokenizer.from_file(TOKENIZER_PATH)

# def wrap_history_header(history_token_ids):
#     return [HEADER_TOKEN_ID] + history_token_ids + [ENDHEADER_TOKEN_ID]

# def serialize_turn(role, text):
#     text = replace_identity_dialogue(role, text)
#     if role == "user":
#         return [SPECIAL_TOKENS["<user>"]] + tokenizer.encode(text).ids + [SPECIAL_TOKENS["</user>"]]
#     else:
#         return [SPECIAL_TOKENS["<assistant>"]] + tokenizer.encode(text).ids + [SPECIAL_TOKENS["</assistant>"]]

# def format_multiturn_with_history(pairs):
#     if len(pairs) <= 1:
#         return sum((serialize_turn(role, text) for role, text in pairs), [])
#     history_pairs = pairs[:-2] if len(pairs) >= 2 else []
#     last_user = pairs[-2] if len(pairs) >= 2 else None
#     last_assistant = pairs[-1] if len(pairs) >= 2 else None
#     history_token_ids = sum((serialize_turn(role, text) for role, text in history_pairs), [])
#     main_token_ids = []
#     if last_user is not None:
#         main_token_ids += serialize_turn(last_user[0], last_user[1])
#     if last_assistant is not None:
#         main_token_ids += serialize_turn(last_assistant[0], last_assistant[1])
#     result = []
#     if history_token_ids:
#         result += wrap_history_header(history_token_ids)
#     result += main_token_ids
#     return result

# def process_greeting_response(user_text, assistant_text):
#     if is_greeting(user_text):
#         return get_greeting_response()
#     return assistant_text

# def process_goodbye_response(user_text, assistant_text):
#     if is_goodbye(user_text):
#         return get_goodbye_response()
#     return assistant_text

# def process_okay_response(user_text, assistant_text):
#     if is_okay(user_text):
#         return get_okay_response()
#     return assistant_text

# def format_mathcot_row(conversations):
#     pairs = []
#     for msg in conversations:
#         if msg["from"] == "human":
#             pairs.append(("user", msg["value"]))
#         elif msg["from"] == "gpt":
#             pairs.append(("assistant", msg["value"]))
#     if len(pairs) > 2:
#         history_pairs = pairs[:-2]
#         last_user = pairs[-2]
#         last_assistant = list(pairs[-1])
#         last_assistant[1] = process_greeting_response(last_user[1], last_assistant[1])
#         last_assistant[1] = process_goodbye_response(last_user[1], last_assistant[1])
#         last_assistant[1] = process_okay_response(last_user[1], last_assistant[1])
#         pairs = history_pairs + [last_user, tuple(last_assistant)]
#         result = format_multiturn_with_history(pairs)
#         output = [START_TOKEN_ID] + result + [END_SEQ_TOKEN_ID]
#     elif len(pairs) == 2:
#         user, assistant = pairs[0], list(pairs[1])
#         assistant[1] = process_greeting_response(user[1], assistant[1])
#         assistant[1] = process_goodbye_response(user[1], assistant[1])
#         assistant[1] = process_okay_response(user[1], assistant[1])
#         result = serialize_turn(user[0], user[1]) + serialize_turn(assistant[0], assistant[1])
#         output = [START_TOKEN_ID] + result + [END_SEQ_TOKEN_ID]
#     else:
#         result = sum((serialize_turn(role, text) for role, text in pairs), [])
#         output = [START_TOKEN_ID] + result + [END_SEQ_TOKEN_ID]
#     if len(output) > CTX_LEN:
#         output = output[-CTX_LEN:]
#     return output

# def format_vtuber_row(messages):
#     pairs = []
#     for msg in messages:
#         if msg["role"] == "system" or not msg["content"]:
#             continue
#         if msg["role"] == "user":
#             pairs.append(("user", msg["content"]))
#         elif msg["role"] == "assistant":
#             pairs.append(("assistant", msg["content"]))
#     if len(pairs) > 2:
#         history_pairs = pairs[:-2]
#         last_user = pairs[-2]
#         last_assistant = list(pairs[-1])
#         last_assistant[1] = process_greeting_response(last_user[1], last_assistant[1])
#         last_assistant[1] = process_goodbye_response(last_user[1], last_assistant[1])
#         last_assistant[1] = process_okay_response(last_user[1], last_assistant[1])
#         pairs = history_pairs + [last_user, tuple(last_assistant)]
#         result = format_multiturn_with_history(pairs)
#         output = [START_TOKEN_ID] + result + [END_SEQ_TOKEN_ID]
#     elif len(pairs) == 2:
#         user, assistant = pairs[0], list(pairs[1])
#         assistant[1] = process_greeting_response(user[1], assistant[1])
#         assistant[1] = process_goodbye_response(user[1], assistant[1])
#         assistant[1] = process_okay_response(user[1], assistant[1])
#         result = serialize_turn(user[0], user[1]) + serialize_turn(assistant[0], assistant[1])
#         output = [START_TOKEN_ID] + result + [END_SEQ_TOKEN_ID]
#     else:
#         result = sum((serialize_turn(role, text) for role, text in pairs), [])
#         output = [START_TOKEN_ID] + result + [END_SEQ_TOKEN_ID]
#     if len(output) > CTX_LEN:
#         output = output[-CTX_LEN:]
#     return output

# def format_lmsys_row(conversation):
#     pairs = []
#     for msg in conversation:
#         if msg["role"] == "user":
#             pairs.append(("user", msg["content"]))
#         elif msg["role"] == "assistant":
#             pairs.append(("assistant", msg["content"]))
#     if len(pairs) > 2:
#         history_pairs = pairs[:-2]
#         last_user = pairs[-2]
#         last_assistant = list(pairs[-1])
#         last_assistant[1] = process_greeting_response(last_user[1], last_assistant[1])
#         last_assistant[1] = process_goodbye_response(last_user[1], last_assistant[1])
#         last_assistant[1] = process_okay_response(last_user[1], last_assistant[1])
#         pairs = history_pairs + [last_user, tuple(last_assistant)]
#         result = format_multiturn_with_history(pairs)
#         output = [START_TOKEN_ID] + result + [END_SEQ_TOKEN_ID]
#     elif len(pairs) == 2:
#         user, assistant = pairs[0], list(pairs[1])
#         assistant[1] = process_greeting_response(user[1], assistant[1])
#         assistant[1] = process_goodbye_response(user[1], assistant[1])
#         assistant[1] = process_okay_response(user[1], assistant[1])
#         result = serialize_turn(user[0], user[1]) + serialize_turn(assistant[0], assistant[1])
#         output = [START_TOKEN_ID] + result + [END_SEQ_TOKEN_ID]
#     else:
#         result = sum((serialize_turn(role, text) for role, text in pairs), [])
#         output = [START_TOKEN_ID] + result + [END_SEQ_TOKEN_ID]
#     if len(output) > CTX_LEN:
#         output = output[-CTX_LEN:]
#     return output

# def format_personas_row(messages):
#     return format_vtuber_row(messages)

# def format_fusechat_row(conversations):
#     pairs = []
#     for msg in conversations:
#         if msg["from"] == "human":
#             pairs.append(("user", msg["value"]))
#         elif msg["from"] == "gpt":
#             pairs.append(("assistant", msg["value"]))
#     if len(pairs) > 2:
#         history_pairs = pairs[:-2]
#         last_user = pairs[-2]
#         last_assistant = list(pairs[-1])
#         last_assistant[1] = process_greeting_response(last_user[1], last_assistant[1])
#         last_assistant[1] = process_goodbye_response(last_user[1], last_assistant[1])
#         last_assistant[1] = process_okay_response(last_user[1], last_assistant[1])
#         pairs = history_pairs + [last_user, tuple(last_assistant)]
#         result = format_multiturn_with_history(pairs)
#         output = [START_TOKEN_ID] + result + [END_SEQ_TOKEN_ID]
#     elif len(pairs) == 2:
#         user, assistant = pairs[0], list(pairs[1])
#         assistant[1] = process_greeting_response(user[1], assistant[1])
#         assistant[1] = process_goodbye_response(user[1], assistant[1])
#         assistant[1] = process_okay_response(user[1], assistant[1])
#         result = serialize_turn(user[0], user[1]) + serialize_turn(assistant[0], assistant[1])
#         output = [START_TOKEN_ID] + result + [END_SEQ_TOKEN_ID]
#     else:
#         result = sum((serialize_turn(role, text) for role, text in pairs), [])
#         output = [START_TOKEN_ID] + result + [END_SEQ_TOKEN_ID]
#     if len(output) > CTX_LEN:
#         output = output[-CTX_LEN:]
#     return output

# def format_menlo_row(conversations):
#     pairs = []
#     for msg in conversations:
#         if msg["role"] == "user":
#             pairs.append(("user", msg["content"]))
#         elif msg["role"] == "assistant":
#             pairs.append(("assistant", msg["content"]))
#     if len(pairs) > 2:
#         history_pairs = pairs[:-2]
#         last_user = pairs[-2]
#         last_assistant = list(pairs[-1])
#         last_assistant[1] = process_greeting_response(last_user[1], last_assistant[1])
#         last_assistant[1] = process_goodbye_response(last_user[1], last_assistant[1])
#         last_assistant[1] = process_okay_response(last_user[1], last_assistant[1])
#         pairs = history_pairs + [last_user, tuple(last_assistant)]
#         result = format_multiturn_with_history(pairs)
#         output = [START_TOKEN_ID] + result + [END_SEQ_TOKEN_ID]
#     elif len(pairs) == 2:
#         user, assistant = pairs[0], list(pairs[1])
#         assistant[1] = process_greeting_response(user[1], assistant[1])
#         assistant[1] = process_goodbye_response(user[1], assistant[1])
#         assistant[1] = process_okay_response(user[1], assistant[1])
#         result = serialize_turn(user[0], user[1]) + serialize_turn(assistant[0], assistant[1])
#         output = [START_TOKEN_ID] + result + [END_SEQ_TOKEN_ID]
#     else:
#         result = sum((serialize_turn(role, text) for role, text in pairs), [])
#         output = [START_TOKEN_ID] + result + [END_SEQ_TOKEN_ID]
#     if len(output) > CTX_LEN:
#         output = output[-CTX_LEN:]
#     return output

# def format_wildchat_row(conversation):
#     pairs = []
#     for msg in conversation:
#         if msg.get("from") == "human":
#             pairs.append(("user", msg.get("value", "")))
#         elif msg.get("from") == "gpt":
#             pairs.append(("assistant", msg.get("value", "")))
#     if len(pairs) > 2:
#         history_pairs = pairs[:-2]
#         last_user = pairs[-2]
#         last_assistant = list(pairs[-1])
#         last_assistant[1] = process_greeting_response(last_user[1], last_assistant[1])
#         last_assistant[1] = process_goodbye_response(last_user[1], last_assistant[1])
#         last_assistant[1] = process_okay_response(last_user[1], last_assistant[1])
#         pairs = history_pairs + [last_user, tuple(last_assistant)]
#         result = format_multiturn_with_history(pairs)
#         output = [START_TOKEN_ID] + result + [END_SEQ_TOKEN_ID]
#     elif len(pairs) == 2:
#         user, assistant = pairs[0], list(pairs[1])
#         assistant[1] = process_greeting_response(user[1], assistant[1])
#         assistant[1] = process_goodbye_response(user[1], assistant[1])
#         assistant[1] = process_okay_response(user[1], assistant[1])
#         result = serialize_turn(user[0], user[1]) + serialize_turn(assistant[0], assistant[1])
#         output = [START_TOKEN_ID] + result + [END_SEQ_TOKEN_ID]
#     else:
#         result = sum((serialize_turn(role, text) for role, text in pairs), [])
#         output = [START_TOKEN_ID] + result + [END_SEQ_TOKEN_ID]
#     if len(output) > CTX_LEN:
#         output = output[-CTX_LEN:]
#     return output

# def format_janhq_row(conversations):
#     pairs = []
#     for msg in conversations:
#         if msg["role"] == "user":
#             pairs.append(("user", msg["content"]))
#         elif msg["role"] == "assistant":
#             pairs.append(("assistant", msg["content"]))
#     if len(pairs) > 2:
#         history_pairs = pairs[:-2]
#         last_user = pairs[-2]
#         last_assistant = list(pairs[-1])
#         last_assistant[1] = process_greeting_response(last_user[1], last_assistant[1])
#         last_assistant[1] = process_goodbye_response(last_user[1], last_assistant[1])
#         last_assistant[1] = process_okay_response(last_user[1], last_assistant[1])
#         pairs = history_pairs + [last_user, tuple(last_assistant)]
#         result = format_multiturn_with_history(pairs)
#         output = [START_TOKEN_ID] + result + [END_SEQ_TOKEN_ID]
#     elif len(pairs) == 2:
#         user, assistant = pairs[0], list(pairs[1])
#         assistant[1] = process_greeting_response(user[1], assistant[1])
#         assistant[1] = process_goodbye_response(user[1], assistant[1])
#         assistant[1] = process_okay_response(user[1], assistant[1])
#         result = serialize_turn(user[0], user[1]) + serialize_turn(assistant[0], assistant[1])
#         output = [START_TOKEN_ID] + result + [END_SEQ_TOKEN_ID]
#     else:
#         result = sum((serialize_turn(role, text) for role, text in pairs), [])
#         output = [START_TOKEN_ID] + result + [END_SEQ_TOKEN_ID]
#     if len(output) > CTX_LEN:
#         output = output[-CTX_LEN:]
#     return output

# def format_medical_row(row):
#     output = [START_TOKEN_ID]
#     user_content = f"Think it\n{row['Question']}"
#     output.append(SPECIAL_TOKENS["<user>"])
#     output.extend(tokenizer.encode(user_content).ids)
#     output.append(SPECIAL_TOKENS["</user>"])
#     output.append(SPECIAL_TOKENS["<think>"])
#     output.extend(tokenizer.encode(row['Complex_CoT']).ids)
#     output.append(SPECIAL_TOKENS["</think>"])
#     output.append(SPECIAL_TOKENS["<assistant>"])
#     output.extend(tokenizer.encode(row['Response']).ids)
#     output.append(SPECIAL_TOKENS["</assistant>"])
#     output.append(END_SEQ_TOKEN_ID)
#     if len(output) > CTX_LEN:
#         output = output[-CTX_LEN:]
#     return output

# def prepare_batch(rows, pad_id=PAD_TOKEN_ID, ctx_len=CTX_LEN):
#     seqs = []
#     for row in rows:
#         if row["source"] == "mathcot":
#             seqs.append(format_mathcot_row(row["conversations"]))
#         elif row["source"] == "vtuber":
#             seqs.append(format_vtuber_row(row["messages"]))
#         elif row["source"] == "lmsys":
#             seqs.append(format_lmsys_row(row["conversation"]))
#         elif row["source"] == "personas":
#             seqs.append(format_personas_row(row["messages"]))
#         elif row["source"] == "medical":
#             seqs.append(format_medical_row(row))
#         elif row["source"] == "fusechat":
#             seqs.append(format_fusechat_row(row["conversations"]))
#         elif row["source"] == "menlo":
#             seqs.append(format_menlo_row(row["conversations"]))
#         elif row["source"] == "wildchat":
#             seqs.append(format_wildchat_row(row["conversation"]))
#         elif row["source"] == "janhq":
#             seqs.append(format_janhq_row(row["conversations"]))
#         else:
#             seqs.append([pad_id])
#     batch_tokens = np.full((len(seqs), ctx_len), pad_id, dtype=np.int32)
#     batch_mask = np.zeros((len(seqs), ctx_len), dtype=np.float32)
#     for i, seq in enumerate(seqs):
#         seq = seq[:ctx_len]
#         batch_tokens[i, :len(seq)] = seq
#         batch_mask[i, :len(seq)] = 1.0
#     return batch_tokens, batch_mask

# print("Loading datasets (full download, non-streaming)...")
# mathcot_ds = load_dataset("Nitral-AI/Math-Cot_1Shot_QA-ShareGPT", split="train", token=HF_TOKEN)
# vtuber_ds = load_dataset("Vtuber-plan/sharegpt-cleaned", split="train", token=HF_TOKEN)
# lmsys_ds = load_dataset("lmsys/lmsys-chat-1m", split="train", trust_remote_code=True, token=HF_TOKEN)
# personas_ds = load_dataset("allenai/tulu-3-sft-personas-instruction-following", split="train", token=HF_TOKEN)
# medical_ds = load_dataset("FreedomIntelligence/medical-o1-reasoning-SFT", "en", split="train", token=HF_TOKEN)
# fusechat_ds = load_dataset("FuseAI/FuseChat-3.0-SFT-Data", split="train", token=HF_TOKEN)
# menlo_ds = load_dataset("Menlo/instruction-text-only-full", split="train", token=HF_TOKEN)
# wildchat_ds = load_dataset("damerajee/WildChat-Eng-Sharegpt", split="train", token=HF_TOKEN)
# janhq_ds = load_dataset("jan-hq/instruction-data-text-only-multiturn", split="train", token=HF_TOKEN)

# synthetic_okay = []
# synthetic_goodbye = []
# for i in range(10):
#     synthetic_okay.append({
#         "source": "synthetic",
#         "conversations": [
#             {"role": "user", "content": "okay"},
#             {"role": "assistant", "content": get_okay_response()}
#         ]
#     })
# for i in range(10):
#     goodbye_prompt = random.choice(GOODBYE_LIST)
#     synthetic_goodbye.append({
#         "source": "synthetic",
#         "conversations": [
#             {"role": "user", "content": goodbye_prompt},
#             {"role": "assistant", "content": get_goodbye_response()}
#         ]
#     })

# print("Preparing in-memory indices for all datasets...")
# mathcot_indices = [("mathcot", i) for i in range(len(mathcot_ds))]
# vtuber_indices = [("vtuber", i) for i in range(len(vtuber_ds))]
# lmsys_indices = [("lmsys", i) for i in range(min(MAX_LMSYS_ROWS, len(lmsys_ds)))]
# personas_indices = [("personas", i) for i in range(len(personas_ds))]
# medical_indices = [("medical", i) for i in range(len(medical_ds))]
# fusechat_indices = [("fusechat", i) for i in range(len(fusechat_ds))]
# menlo_indices = [("menlo", i) for i in range(len(menlo_ds))]
# wildchat_indices = [("wildchat", i) for i in range(len(wildchat_ds))]
# janhq_indices = [("janhq", i) for i in range(len(janhq_ds))]
# synthetic_okay_indices = [("synthetic", i) for i in range(len(synthetic_okay))]
# synthetic_goodbye_indices = [("synthetic_goodbye", i) for i in range(len(synthetic_goodbye))]

# epoch_indices = (mathcot_indices + vtuber_indices + lmsys_indices + personas_indices +
#                  medical_indices + fusechat_indices + menlo_indices + wildchat_indices +
#                  janhq_indices + synthetic_okay_indices + synthetic_goodbye_indices)
# random.shuffle(epoch_indices)
# num_batches = math.ceil(len(epoch_indices) / BATCH_SIZE)

# def get_row(source, idx):
#     if source == "mathcot":
#         return {"source": "mathcot", "conversations": mathcot_ds[idx]["conversations"]}
#     elif source == "vtuber":
#         return {"source": "vtuber", "messages": vtuber_ds[idx]["messages"]}
#     elif source == "lmsys":
#         return {"source": "lmsys", "conversation": lmsys_ds[idx]["conversation"]}
#     elif source == "personas":
#         return {"source": "personas", "messages": personas_ds[idx]["messages"]}
#     elif source == "medical":
#         row = dict(medical_ds[idx])
#         row["source"] = "medical"
#         return row
#     elif source == "fusechat":
#         return {"source": "fusechat", "conversations": fusechat_ds[idx]["conversations"]}
#     elif source == "menlo":
#         return {"source": "menlo", "conversations": menlo_ds[idx]["conversations"]}
#     elif source == "wildchat":
#         return {"source": "wildchat", "conversation": wildchat_ds[idx]["conversation"]}
#     elif source == "janhq":
#         return {"source": "janhq", "conversations": janhq_ds[idx]["conversations"]}
#     elif source == "synthetic":
#         return {"source": "janhq", "conversations": synthetic_okay[idx]["conversations"]}
#     elif source == "synthetic_goodbye":
#         return {"source": "janhq", "conversations": synthetic_goodbye[idx]["conversations"]}
#     else:
#         return {"source": "mathcot", "conversations": [{"from": "human", "value": ""}]}

# def get_mega_batch(start_batch):
#     mega_batch_rows = []
#     for d in range(num_devices):
#         batch_rows = []
#         for b in range(BATCH_PER_DEVICE):
#             batch_idx = (start_batch + d) * BATCH_PER_DEVICE + b
#             if batch_idx < len(epoch_indices):
#                 source, idx = epoch_indices[batch_idx]
#                 try:
#                     row = get_row(source, idx)
#                 except Exception:
#                     row = {"source": "mathcot", "conversations": [{"from": "human", "value": ""}]}
#             else:
#                 row = {"source": "mathcot", "conversations": [{"from": "human", "value": ""}]}
#             batch_rows.append(row)
#         batch_tokens, batch_mask = prepare_batch(batch_rows)
#         mega_batch_rows.append((batch_tokens, batch_mask))
#     batch_tokens = np.stack([x[0] for x in mega_batch_rows])
#     batch_mask = np.stack([x[1] for x in mega_batch_rows])
#     return batch_tokens, batch_mask

# print("Initializing model...")
# model = DeepSeekModel(
#     vocab_size=config["vocab_size"],
#     d_model=config["d_model"],
#     nhead=config["nhead"],
#     num_layers=config["num_layers"],
#     ff_hidden_dim=config["ff_hidden_dim"],
#     max_len=config["max_len"],
#     dropout_rate=config["dropout_rate"],
#     dtype=DTYPE,
#     window_layer_indices=config["window_layer_indices"],
#     moe_layer_indices=config["moe_layer_indices"],
#     window_size=config["window_size"],
#     moe_params=config["moe_params"]
# )
# dummy_input = jnp.ones((1, CTX_LEN-1), dtype=jnp.int32)
# rng = jax.random.PRNGKey(0)
# init_params = model.init(rng, dummy_input, deterministic=True)

# print("Loading pretrained model parameters from local fine.msgpack ...")
# with open(MODEL_PARAMS_SAVE_PATH, "rb") as f:
#     saved_params_bytes = f.read()
# params = flax.serialization.from_bytes(init_params, saved_params_bytes)

# optimizer = optax.adamw(learning_rate=LEARNING_RATE)
# opt_state = optimizer.init(params)

# @jax.pmap
# def train_step(params, opt_state, batch_tokens, batch_mask, rng):
#     def loss_fn(params):
#         logits = model.apply(params, batch_tokens, deterministic=False, rngs={"dropout": rng})
#         labels = batch_tokens[:, 1:]
#         mask = batch_mask[:, 1:]
#         logits = logits[:, :-1, :]
#         loss = optax.softmax_cross_entropy_with_integer_labels(logits, labels)
#         loss = (loss * mask).sum() / mask.sum()
#         accuracy = (jnp.argmax(logits, axis=-1) == labels)
#         accuracy = (accuracy * mask).sum() / mask.sum()
#         return loss, accuracy
#     grad_fn = jax.value_and_grad(loss_fn, has_aux=True)
#     (loss, accuracy), grads = grad_fn(params)
#     updates, new_opt_state = optimizer.update(grads, opt_state, params)
#     new_params = optax.apply_updates(params, updates)
#     return new_params, new_opt_state, loss, accuracy

# print(f"Training with {len(epoch_indices)} samples, {num_batches} batches per epoch.")

# params = jax.device_put_replicated(params, jax.devices())
# opt_state = jax.device_put_replicated(opt_state, jax.devices())

# for epoch in range(EPOCHS):
#     print(f"\nEpoch {epoch+1}/{EPOCHS}")
#     epoch_loss = []
#     epoch_acc = []
#     bar = tqdm(range(0, num_batches, num_devices), desc="Training", leave=True)
#     with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
#         future = executor.submit(get_mega_batch, 0)
#         for i in bar:
#             batch_tokens, batch_mask = future.result()
#             if i + num_devices < num_batches:
#                 future = executor.submit(get_mega_batch, i + num_devices)
#             batch_tokens = jnp.array(batch_tokens)
#             batch_mask = jnp.array(batch_mask)
#             rng, step_rng = jax.random.split(rng)
#             rngs = jax.random.split(step_rng, num_devices)
#             params, opt_state, loss, acc = train_step(params, opt_state, batch_tokens, batch_mask, rngs)
#             mean_loss = float(np.mean(loss))
#             mean_acc = float(np.mean(acc))
#             epoch_loss.append(mean_loss)
#             epoch_acc.append(mean_acc)
#             bar.set_postfix({"loss": f"{mean_loss:.4f}", "acc": f"{mean_acc*100:.2f}%"})
#     print(f"Epoch {epoch+1} finished. Avg loss: {np.mean(epoch_loss):.4f} | Avg acc: {np.mean(epoch_acc)*100:.2f}%")

# print(f"Saving fine-tuned parameters to {SAVE_FINETUNED_PATH} ...")
# params_cpu = jax.device_get(jax.tree_util.tree_map(lambda x: x[0], params))
# with open(SAVE_FINETUNED_PATH, "wb") as f:
#     f.write(flax.serialization.to_bytes(params_cpu))
# print("Done.")+





