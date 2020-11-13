import torch
from torch import nn
from torch.nn import Parameter
from textbox.module.layers import TransformerLayer
import torch.nn.functional as F


class TransformerDecoder(torch.nn.Module):
    def __init__(self,
                 input_size,
                 ffn_size,
                 num_layers,
                 num_heads,
                 attn_dropout=0.0,
                 attn_weight_dropout=0.0,
                 ffn_dropout=0.0,
                 ffn_activate_func='gelu',
                 with_external=False):
        super(TransformerDecoder, self).__init__()
        
        self.transformer_layers = nn.ModuleList()
        for _ in range(num_layers):
            self.transformer_layers.append(
                TransformerLayer(input_size, ffn_size, num_heads, attn_dropout, attn_weight_dropout,
                                 ffn_dropout, ffn_activate_func, with_external))

    def forward(self, x, kv=None,
                self_padding_mask=None, self_attn_mask=None,
                external_states=None, external_padding_mask=None):
        for idx, layer in enumerate(self.transformer_layers):
            x, _, _ = layer(x, kv, self_padding_mask, self_attn_mask, external_states, external_padding_mask)
        return x




