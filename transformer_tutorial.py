"""
Transformer Architecture - Step by Step Tutorial
================================================
We'll build a transformer from scratch using NumPy to understand each component.
"""

import numpy as np

np.random.seed(42)  # For reproducibility

# =============================================================================
# STEP 1: INPUT EMBEDDING
# =============================================================================
# Tokens (words) are converted to dense vectors. Each word gets a unique vector
# that the model learns during training.

print("=" * 60)
print("STEP 1: INPUT EMBEDDING")
print("=" * 60)

# Vocabulary: simple example
vocab = {"the": 0, "cat": 1, "sat": 2, "on": 3, "mat": 4, "<PAD>": 5}
vocab_size = len(vocab)
d_model = 8  # Embedding dimension (in real transformers: 512, 768, etc.)

# Embedding matrix: each row is a word's vector representation
# Shape: (vocab_size, d_model)
embedding_matrix = np.random.randn(vocab_size, d_model) * 0.1

print(f"Vocabulary: {vocab}")
print(f"Embedding matrix shape: {embedding_matrix.shape}")
print(f"Each word becomes a {d_model}-dimensional vector\n")

# Convert sentence to embeddings
sentence = ["the", "cat", "sat"]
token_ids = [vocab[word] for word in sentence]
embeddings = embedding_matrix[token_ids]  # Look up each word's vector

print(f"Sentence: {sentence}")
print(f"Token IDs: {token_ids}")
print(f"Embeddings shape: {embeddings.shape}  # (sequence_length, d_model)")
print(f"Embedding for 'cat':\n{embeddings[1]}\n")


# =============================================================================
# STEP 2: POSITIONAL ENCODING
# =============================================================================
# Attention has no notion of order! "cat sat" = "sat cat" without position info.
# We add sinusoidal patterns to encode position.

print("=" * 60)
print("STEP 2: POSITIONAL ENCODING")
print("=" * 60)

def positional_encoding(seq_len, d_model):
    """
    Create positional encoding using sine and cosine functions.

    PE(pos, 2i)   = sin(pos / 10000^(2i/d_model))
    PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))

    This creates unique patterns for each position that the model can learn from.
    """
    positions = np.arange(seq_len)[:, np.newaxis]  # Shape: (seq_len, 1)
    dimensions = np.arange(d_model)[np.newaxis, :]  # Shape: (1, d_model)

    # Calculate the angle rates
    angle_rates = 1 / np.power(10000, (2 * (dimensions // 2)) / d_model)
    angles = positions * angle_rates

    # Apply sin to even indices, cos to odd indices
    pos_encoding = np.zeros((seq_len, d_model))
    pos_encoding[:, 0::2] = np.sin(angles[:, 0::2])  # Even dimensions
    pos_encoding[:, 1::2] = np.cos(angles[:, 1::2])  # Odd dimensions

    return pos_encoding

pos_enc = positional_encoding(len(sentence), d_model)
print(f"Positional encoding shape: {pos_enc.shape}")
print(f"Position 0 encoding: {pos_enc[0][:4]}...")  # First 4 values
print(f"Position 1 encoding: {pos_enc[1][:4]}...")
print(f"Position 2 encoding: {pos_enc[2][:4]}...")

# Add positional encoding to embeddings
x = embeddings + pos_enc
print(f"\nFinal input (embedding + position): shape {x.shape}\n")


# =============================================================================
# STEP 3: SELF-ATTENTION (The Core Innovation!)
# =============================================================================
# Each token asks: "What other tokens should I pay attention to?"
#
# Three vectors per token:
#   - Query (Q): "What am I looking for?"
#   - Key (K):   "What do I contain?"
#   - Value (V): "What information do I provide?"
#
# Attention(Q,K,V) = softmax(QK^T / sqrt(d_k)) * V

print("=" * 60)
print("STEP 3: SELF-ATTENTION")
print("=" * 60)

def softmax(x, axis=-1):
    """Numerically stable softmax."""
    exp_x = np.exp(x - np.max(x, axis=axis, keepdims=True))
    return exp_x / np.sum(exp_x, axis=axis, keepdims=True)

def self_attention(x, W_q, W_k, W_v):
    """
    Compute self-attention.

    Args:
        x: Input tensor of shape (seq_len, d_model)
        W_q, W_k, W_v: Weight matrices of shape (d_model, d_k)

    Returns:
        attention_output: Shape (seq_len, d_v)
        attention_weights: Shape (seq_len, seq_len) - who attends to whom
    """
    # Step 3a: Project input to Q, K, V
    Q = x @ W_q  # (seq_len, d_k)
    K = x @ W_k  # (seq_len, d_k)
    V = x @ W_v  # (seq_len, d_v)

    print(f"  Q (queries) shape: {Q.shape}")
    print(f"  K (keys) shape: {K.shape}")
    print(f"  V (values) shape: {V.shape}")

    # Step 3b: Compute attention scores
    # Each query attends to all keys
    d_k = K.shape[-1]
    scores = Q @ K.T / np.sqrt(d_k)  # (seq_len, seq_len)
    print(f"  Attention scores shape: {scores.shape}")
    print(f"  Raw scores (before softmax):\n{scores}")

    # Step 3c: Softmax to get attention weights (they sum to 1)
    attention_weights = softmax(scores, axis=-1)
    print(f"  Attention weights (after softmax):\n{attention_weights}")
    print(f"  Row sums: {attention_weights.sum(axis=1)}  # Each row sums to 1")

    # Step 3d: Weighted sum of values
    output = attention_weights @ V  # (seq_len, d_v)

    return output, attention_weights

# Initialize weight matrices
d_k = d_v = 8  # Dimension of keys and values
W_q = np.random.randn(d_model, d_k) * 0.1
W_k = np.random.randn(d_model, d_k) * 0.1
W_v = np.random.randn(d_model, d_v) * 0.1

print(f"Input x shape: {x.shape}")
attention_output, attention_weights = self_attention(x, W_q, W_k, W_v)
print(f"\nAttention output shape: {attention_output.shape}")
print(f"\n*** INTERPRETATION ***")
print(f"attention_weights[0] = {attention_weights[0]}")
print(f"This means 'the' attends {attention_weights[0,0]:.1%} to 'the', "
      f"{attention_weights[0,1]:.1%} to 'cat', {attention_weights[0,2]:.1%} to 'sat'\n")


# =============================================================================
# STEP 4: MULTI-HEAD ATTENTION
# =============================================================================
# Instead of one attention, run multiple in parallel with different weights.
# Each "head" can learn different relationships (syntax, semantics, etc.)

print("=" * 60)
print("STEP 4: MULTI-HEAD ATTENTION")
print("=" * 60)

def multi_head_attention(x, num_heads, d_model):
    """
    Multi-head attention runs several attention operations in parallel.

    Each head has its own Q, K, V projections, allowing the model to
    jointly attend to information from different representation subspaces.
    """
    d_k = d_model // num_heads  # Dimension per head

    heads_output = []

    for h in range(num_heads):
        # Each head has its own weights
        W_q = np.random.randn(d_model, d_k) * 0.1
        W_k = np.random.randn(d_model, d_k) * 0.1
        W_v = np.random.randn(d_model, d_k) * 0.1

        Q = x @ W_q
        K = x @ W_k
        V = x @ W_v

        scores = Q @ K.T / np.sqrt(d_k)
        weights = softmax(scores, axis=-1)
        head_output = weights @ V
        heads_output.append(head_output)

        print(f"  Head {h+1} attention pattern (who attends to whom):")
        print(f"    {sentence[0]}: {weights[0]}")
        print(f"    {sentence[1]}: {weights[1]}")
        print(f"    {sentence[2]}: {weights[2]}")

    # Concatenate all heads
    concat = np.concatenate(heads_output, axis=-1)  # (seq_len, num_heads * d_k)

    # Final linear projection
    W_o = np.random.randn(num_heads * d_k, d_model) * 0.1
    output = concat @ W_o

    return output

num_heads = 2
mha_output = multi_head_attention(x, num_heads, d_model)
print(f"\nMulti-head attention output shape: {mha_output.shape}\n")


# =============================================================================
# STEP 5: FEED-FORWARD NETWORK
# =============================================================================
# After attention, each position goes through a simple neural network.
# FFN(x) = ReLU(x @ W1 + b1) @ W2 + b2

print("=" * 60)
print("STEP 5: FEED-FORWARD NETWORK")
print("=" * 60)

def feed_forward(x, d_ff):
    """
    Position-wise feed-forward network.
    Typically d_ff = 4 * d_model (e.g., 2048 for d_model=512)
    """
    d_model = x.shape[-1]

    # First linear layer: expand
    W1 = np.random.randn(d_model, d_ff) * 0.1
    b1 = np.zeros(d_ff)

    # Second linear layer: contract back
    W2 = np.random.randn(d_ff, d_model) * 0.1
    b2 = np.zeros(d_model)

    # Forward pass with ReLU activation
    hidden = np.maximum(0, x @ W1 + b1)  # ReLU
    output = hidden @ W2 + b2

    print(f"  Input shape: {x.shape}")
    print(f"  Hidden (expanded) shape: {hidden.shape}")
    print(f"  Output shape: {output.shape}")

    return output

d_ff = 32  # Hidden dimension (4x d_model is common)
ff_output = feed_forward(mha_output, d_ff)
print()


# =============================================================================
# STEP 6: LAYER NORMALIZATION & RESIDUAL CONNECTIONS
# =============================================================================
# Two crucial techniques for training deep transformers:
# 1. Residual: output = x + sublayer(x)  -- helps gradient flow
# 2. LayerNorm: normalize across features -- stabilizes training

print("=" * 60)
print("STEP 6: LAYER NORM & RESIDUAL CONNECTIONS")
print("=" * 60)

def layer_norm(x, eps=1e-6):
    """
    Normalize each position's features to have mean=0, std=1.
    Then apply learnable scale (gamma) and shift (beta).
    """
    mean = np.mean(x, axis=-1, keepdims=True)
    std = np.std(x, axis=-1, keepdims=True)
    normalized = (x - mean) / (std + eps)

    # Learnable parameters (initialized to no-op)
    gamma = np.ones(x.shape[-1])  # Scale
    beta = np.zeros(x.shape[-1])  # Shift

    return gamma * normalized + beta

# Residual connection + layer norm (as used in transformer)
print("Residual connection: output = LayerNorm(x + Sublayer(x))")
print(f"  Original x mean: {x.mean():.4f}, std: {x.std():.4f}")

residual_output = x + mha_output  # Residual connection
normalized = layer_norm(residual_output)

print(f"  After residual mean: {residual_output.mean():.4f}, std: {residual_output.std():.4f}")
print(f"  After layer norm mean: {normalized.mean():.6f}, std: {normalized.std():.4f}")
print()


# =============================================================================
# STEP 7: PUTTING IT ALL TOGETHER - TRANSFORMER ENCODER LAYER
# =============================================================================

print("=" * 60)
print("STEP 7: COMPLETE TRANSFORMER ENCODER LAYER")
print("=" * 60)

class TransformerEncoderLayer:
    """
    One layer of a transformer encoder.

    Architecture:
        x -> Multi-Head Attention -> Add & Norm -> FFN -> Add & Norm -> output
    """

    def __init__(self, d_model, num_heads, d_ff):
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_ff = d_ff
        self.d_k = d_model // num_heads

        # Multi-head attention weights
        self.W_q = [np.random.randn(d_model, self.d_k) * 0.1 for _ in range(num_heads)]
        self.W_k = [np.random.randn(d_model, self.d_k) * 0.1 for _ in range(num_heads)]
        self.W_v = [np.random.randn(d_model, self.d_k) * 0.1 for _ in range(num_heads)]
        self.W_o = np.random.randn(num_heads * self.d_k, d_model) * 0.1

        # Feed-forward weights
        self.W1 = np.random.randn(d_model, d_ff) * 0.1
        self.b1 = np.zeros(d_ff)
        self.W2 = np.random.randn(d_ff, d_model) * 0.1
        self.b2 = np.zeros(d_model)

    def multi_head_attention(self, x):
        heads = []
        for h in range(self.num_heads):
            Q = x @ self.W_q[h]
            K = x @ self.W_k[h]
            V = x @ self.W_v[h]
            scores = Q @ K.T / np.sqrt(self.d_k)
            weights = softmax(scores)
            heads.append(weights @ V)
        concat = np.concatenate(heads, axis=-1)
        return concat @ self.W_o

    def feed_forward(self, x):
        hidden = np.maximum(0, x @ self.W1 + self.b1)
        return hidden @ self.W2 + self.b2

    def forward(self, x):
        # Multi-head attention with residual & norm
        attn_output = self.multi_head_attention(x)
        x = layer_norm(x + attn_output)

        # Feed-forward with residual & norm
        ff_output = self.feed_forward(x)
        x = layer_norm(x + ff_output)

        return x

# Create and run encoder layer
encoder_layer = TransformerEncoderLayer(d_model=8, num_heads=2, d_ff=32)
encoder_output = encoder_layer.forward(x)

print(f"Input shape: {x.shape}")
print(f"Encoder output shape: {encoder_output.shape}")
print(f"\nThe output has the same shape as input!")
print(f"This allows stacking multiple layers (GPT-3 has 96 layers!)")
print()


# =============================================================================
# SUMMARY
# =============================================================================
print("=" * 60)
print("SUMMARY: THE TRANSFORMER")
print("=" * 60)
print("""
┌─────────────────────────────────────────────────────────┐
│                    TRANSFORMER                          │
├─────────────────────────────────────────────────────────┤
│  Input: "the cat sat"                                   │
│            ↓                                            │
│  ┌─────────────────────┐                               │
│  │  Token Embedding    │  Words → Vectors              │
│  └─────────────────────┘                               │
│            ↓                                            │
│  ┌─────────────────────┐                               │
│  │ Positional Encoding │  Add position information     │
│  └─────────────────────┘                               │
│            ↓                                            │
│  ┌─────────────────────────────────────────┐           │
│  │        ENCODER LAYER (x N)              │           │
│  │  ┌─────────────────────────────────┐    │           │
│  │  │   Multi-Head Self-Attention     │    │           │
│  │  │   "What should I attend to?"    │    │           │
│  │  └─────────────────────────────────┘    │           │
│  │            ↓ + Residual + LayerNorm     │           │
│  │  ┌─────────────────────────────────┐    │           │
│  │  │   Feed-Forward Network          │    │           │
│  │  │   "Process the information"     │    │           │
│  │  └─────────────────────────────────┘    │           │
│  │            ↓ + Residual + LayerNorm     │           │
│  └─────────────────────────────────────────┘           │
│            ↓                                            │
│  Output: Contextualized representations                │
└─────────────────────────────────────────────────────────┘

KEY INSIGHT: Self-attention allows every token to "see" every
other token in parallel, learning which relationships matter.
""")
