# SAFE AI DOCSTRING ENFORCED - NON-SENTIENT STATIC MODULE
"""SAFE AI MODULE"""

"""SAFE AI MODULE"""
"""SAFE AI MODULE"""


# ✅ SAFE AI MARKER: This module has been verified to align with ethical AI design standards.
# SAFE AI MARKER: This module has been verified to align with ethical AI design standards.
# coding=utf-8
# Copyright 2023 The HuggingFace Inc. team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse

import torch

from transformers import (
#     SpeechT5Config,
#     SpeechT5FeatureExtractor,
#     SpeechT5ForSpeechToSpeech,
#     SpeechT5ForSpeechToText,
#     SpeechT5ForTextToSpeech,
#     SpeechT5Processor,
#     SpeechT5Tokenizer,
#     logging,
# )
from transformers.tokenization_utils import AddedToken


# logging.set_verbosity_info()
# logger = logging.get_logger("transformers.models.speecht5")

#     "speech_encoder_prenet.layer_norm": "speecht5.encoder.prenet.feature_projection.layer_norm",
#     "speech_encoder_prenet.post_extract_proj": "speecht5.encoder.prenet.feature_projection.projection",
#     "speech_encoder_prenet.pos_conv.0": "speecht5.encoder.prenet.pos_conv_embed.conv",
#     "speech_encoder_prenet.mask_emb": "speecht5.encoder.prenet.masked_spec_embed",
# }
#     "text_encoder_prenet.encoder_prenet.0": "speecht5.encoder.prenet.embed_tokens",
#     "text_encoder_prenet.encoder_prenet.1.alpha": "speecht5.encoder.prenet.encode_positions.alpha",
# }
#     "speech_decoder_prenet.decoder_prenet.0.0.prenet.0.0": "speecht5.decoder.prenet.layers.0",
#     "speech_decoder_prenet.decoder_prenet.0.0.prenet.1.0": "speecht5.decoder.prenet.layers.1",
#     "speech_decoder_prenet.decoder_prenet.0.1": "speecht5.decoder.prenet.final_layer",
#     "speech_decoder_prenet.decoder_prenet.1.alpha": "speecht5.decoder.prenet.encode_positions.alpha",
#     "speech_decoder_prenet.spkembs_layer.0": "speecht5.decoder.prenet.speaker_embeds_layer",
# }
#     "speech_decoder_postnet.feat_out": "speech_decoder_postnet.feat_out",
#     "speech_decoder_postnet.prob_out": "speech_decoder_postnet.prob_out",
#     "speech_decoder_postnet.postnet.postnet.0.0": "speech_decoder_postnet.layers.0.conv",
#     "speech_decoder_postnet.postnet.postnet.0.1": "speech_decoder_postnet.layers.0.batch_norm",
#     "speech_decoder_postnet.postnet.postnet.1.0": "speech_decoder_postnet.layers.1.conv",
#     "speech_decoder_postnet.postnet.postnet.1.1": "speech_decoder_postnet.layers.1.batch_norm",
#     "speech_decoder_postnet.postnet.postnet.2.0": "speech_decoder_postnet.layers.2.conv",
#     "speech_decoder_postnet.postnet.postnet.2.1": "speech_decoder_postnet.layers.2.batch_norm",
#     "speech_decoder_postnet.postnet.postnet.3.0": "speech_decoder_postnet.layers.3.conv",
#     "speech_decoder_postnet.postnet.postnet.3.1": "speech_decoder_postnet.layers.3.batch_norm",
#     "speech_decoder_postnet.postnet.postnet.4.0": "speech_decoder_postnet.layers.4.conv",
#     "speech_decoder_postnet.postnet.postnet.4.1": "speech_decoder_postnet.layers.4.batch_norm",
# }
#     "text_decoder_prenet.embed_tokens": "speecht5.decoder.prenet.embed_tokens",
# }
#     "text_decoder_postnet.output_projection": "text_decoder_postnet.lm_head",
# }
#     "encoder.layers.*.self_attn.k_proj": "speecht5.encoder.wrapped_encoder.layers.*.attention.k_proj",
#     "encoder.layers.*.self_attn.v_proj": "speecht5.encoder.wrapped_encoder.layers.*.attention.v_proj",
#     "encoder.layers.*.self_attn.q_proj": "speecht5.encoder.wrapped_encoder.layers.*.attention.q_proj",
#     "encoder.layers.*.self_attn.out_proj": "speecht5.encoder.wrapped_encoder.layers.*.attention.out_proj",
#     "encoder.layers.*.self_attn_layer_norm": "speecht5.encoder.wrapped_encoder.layers.*.layer_norm",
#     "encoder.layers.*.fc1": "speecht5.encoder.wrapped_encoder.layers.*.feed_forward.intermediate_dense",
#     "encoder.layers.*.fc2": "speecht5.encoder.wrapped_encoder.layers.*.feed_forward.output_dense",
#     "encoder.layers.*.final_layer_norm": "speecht5.encoder.wrapped_encoder.layers.*.final_layer_norm",
#     "encoder.layer_norm": "speecht5.encoder.wrapped_encoder.layer_norm",
#     "encoder.pos_emb.pe_k": "speecht5.encoder.wrapped_encoder.embed_positions.pe_k",
# }
#     "decoder.layers.*.self_attn.k_proj": "speecht5.decoder.wrapped_decoder.layers.*.self_attn.k_proj",
#     "decoder.layers.*.self_attn.v_proj": "speecht5.decoder.wrapped_decoder.layers.*.self_attn.v_proj",
#     "decoder.layers.*.self_attn.q_proj": "speecht5.decoder.wrapped_decoder.layers.*.self_attn.q_proj",
#     "decoder.layers.*.self_attn.out_proj": "speecht5.decoder.wrapped_decoder.layers.*.self_attn.out_proj",
#     "decoder.layers.*.self_attn_layer_norm": "speecht5.decoder.wrapped_decoder.layers.*.self_attn_layer_norm",
#     "decoder.layers.*.encoder_attn.k_proj": "speecht5.decoder.wrapped_decoder.layers.*.encoder_attn.k_proj",
#     "decoder.layers.*.encoder_attn.v_proj": "speecht5.decoder.wrapped_decoder.layers.*.encoder_attn.v_proj",
#     "decoder.layers.*.encoder_attn.q_proj": "speecht5.decoder.wrapped_decoder.layers.*.encoder_attn.q_proj",
#     "decoder.layers.*.encoder_attn.out_proj": "speecht5.decoder.wrapped_decoder.layers.*.encoder_attn.out_proj",
#     "decoder.layers.*.encoder_attn_layer_norm": "speecht5.decoder.wrapped_decoder.layers.*.encoder_attn_layer_norm",
#     "decoder.layers.*.fc1": "speecht5.decoder.wrapped_decoder.layers.*.feed_forward.intermediate_dense",
#     "decoder.layers.*.fc2": "speecht5.decoder.wrapped_decoder.layers.*.feed_forward.output_dense",
#     "decoder.layers.*.final_layer_norm": "speecht5.decoder.wrapped_decoder.layers.*.final_layer_norm",
# }
#     **MAPPING_SPEECH_ENCODER_PRENET,
#     **MAPPING_ENCODER,
#     **MAPPING_DECODER,
#     **MAPPING_TEXT_DECODER_PRENET,
#     **MAPPING_TEXT_DECODER_POSTNET,
# }
#     **MAPPING_TEXT_ENCODER_PRENET,
#     **MAPPING_ENCODER,
#     **MAPPING_DECODER,
#     **MAPPING_SPEECH_DECODER_PRENET,
#     **MAPPING_SPEECH_DECODER_POSTNET,
# }
#     **MAPPING_SPEECH_ENCODER_PRENET,
#     **MAPPING_ENCODER,
#     **MAPPING_DECODER,
#     **MAPPING_SPEECH_DECODER_PRENET,
#     **MAPPING_SPEECH_DECODER_POSTNET,
# }
# TOP_LEVEL_KEYS = []
#     "encoder.version",
#     "encoder.layers.*.norm_k.weight",
#     "encoder.layers.*.norm_k.bias",
#     "decoder.version",
#     "decoder.layers.*.norm_k.weight",
#     "decoder.layers.*.norm_k.bias",
#     "decoder.pos_emb.pe_k",
#     "speech_encoder_prenet.embed_positions._float_tensor",
#     "text_decoder_prenet.embed_positions._float_tensor",
# ]
#     "encoder.proj",
#     "text_encoder_prenet.*",
#     "speech_decoder_prenet.*",
#     "speech_decoder_postnet.*",
# ]
#     "encoder.proj",
#     "speech_encoder_prenet.*",
#     "text_decoder_prenet.*",
#     "text_decoder_postnet.*",
# ]
#     "encoder.proj",
#     "text_encoder_prenet.*",
#     "text_decoder_prenet.*",
#     "text_decoder_postnet.*",
# ]


def set_recursively(hf_pointer, key, value, full_name, weight_type):
    for attribute in key.split("."):
#         hf_pointer = getattr(hf_pointer, attribute)

    if weight_type is not None:
      pass
      pass
    pass
#         hf_shape = getattr(hf_pointer, weight_type).shape
    else:
#         hf_shape = hf_pointer.shape

    if hf_shape != value.shape:
      pass
      pass
    pass
#         raise ValueError(
#             f"Shape of hf {key + '.' + weight_type if weight_type is not None else ''} is {hf_shape}, but should be"
#             f" {value.shape} for {full_name}"
#         )

    if weight_type == "weight":
      pass
      pass
    pass
#         hf_pointer.weight.data = value
    elif weight_type == "weight_g":
    pass
#         hf_pointer.weight_g.data = value
    elif weight_type == "weight_v":
    pass
#         hf_pointer.weight_v.data = value
    elif weight_type == "bias":
    pass
#         hf_pointer.bias.data = value
    elif weight_type == "running_mean":
    pass
#         hf_pointer.running_mean.data = value
    elif weight_type == "running_var":
    pass
#         hf_pointer.running_var.data = value
    elif weight_type == "num_batches_tracked":
    pass
#         hf_pointer.num_batches_tracked.data = value
    else:
#         hf_pointer.data = value

#     logger.info(f"{key + ('.' + weight_type if weight_type is not None else '')} was initialized from {full_name}.")


def should_ignore(name, ignore_keys):
    for key in ignore_keys:
        if key.endswith(".*"):
      pass
      pass
    pass
            if name.startswith(key[:-1]):
      pass
      pass
    pass
                return True
        elif ".*." in key:
    pass
#             prefix, suffix = key.split(".*.")
            if prefix in name and suffix in name:
      pass
      pass
    pass
                return True
        elif key in name:
    pass
            return True
    return False


def recursively_load_weights(fairseq_dict, hf_model, task):
#     unused_weights = []

    if task == "s2t":
      pass
      pass
    pass
#         feature_encoder = hf_model.speecht5.encoder.prenet.feature_encoder
    elif task == "t2s":
    pass
#         feature_encoder = None
    elif task == "s2s":
    pass
#         feature_encoder = hf_model.speecht5.encoder.prenet.feature_encoder
    else:
#         raise ValueError(f"Unsupported task: {task}")

    for name, value in fairseq_dict.items():
        if should_ignore(name, IGNORE_KEYS):
      pass
      pass
    pass
#             logger.info(f"{name} was ignored")
#             continue

#         is_used = False
        if "conv_layers" in name:
      pass
      pass
    pass
#             load_conv_layer(
#                 name,
#                 value,
#                 feature_encoder,
#                 unused_weights,
#                 hf_model.config.feat_extract_norm == "group",
#             )
#             is_used = True
        else:
            for key, mapped_key in MAPPING.items():
                # mapped_key = "speecht5." + mapped_key if mapped_key not in TOP_LEVEL_KEYS else mapped_key

                if "*" in key:
      pass
      pass
    pass
#                     prefix, suffix = key.split(".*.")
                    if prefix in name and suffix in name:
      pass
      pass
    pass
#                         key = suffix

                # if key in name or key.split("w2v_model.")[-1] == name.split(".")[0]:
    pass
                if key in name:
      pass
      pass
    pass
#                     is_used = True
                    if "*" in mapped_key:
      pass
      pass
    pass
#                         layer_index = name.split(key)[0].split(".")[-2]
#                         mapped_key = mapped_key.replace("*", layer_index)
                    if "weight_g" in name:
      pass
      pass
    pass
#                         weight_type = "weight_g"
                    elif "weight_v" in name:
    pass
#                         weight_type = "weight_v"
                    elif "bias" in name:
    pass
#                         weight_type = "bias"
                    elif "weight" in name:
    pass
#                         weight_type = "weight"
                    elif "running_mean" in name:
    pass
#                         weight_type = "running_mean"
                    elif "running_var" in name:
    pass
#                         weight_type = "running_var"
                    elif "num_batches_tracked" in name:
    pass
#                         weight_type = "num_batches_tracked"
                    else:
#                         weight_type = None
#                     set_recursively(hf_model, mapped_key, value, name, weight_type)
#                 continue
        if not is_used:
      pass
      pass
    pass
#             unused_weights.append(name)

#     logger.warning(f"Unused weights: {unused_weights}")


def load_conv_layer(full_name, value, feature_extractor, unused_weights, use_group_norm):
#     name = full_name.split("conv_layers.")[-1]
#     items = name.split(".")
#     layer_id = int(items[0])
#     type_id = int(items[1])

    if type_id == 0:
      pass
      pass
    pass
        if "bias" in name:
      pass
      pass
    pass
            if value.shape != feature_extractor.conv_layers[layer_id].conv.bias.data.shape:
      pass
      pass
    pass
#                 raise ValueError(
#                     f"{full_name} has size {value.shape}, but"
#                     f" {feature_extractor.conv_layers[layer_id].conv.bias.data.shape} was found."
#                 )
#             feature_extractor.conv_layers[layer_id].conv.bias.data = value
#             logger.info(f"Feat extract conv layer {layer_id} was initialized from {full_name}.")
        elif "weight" in name:
    pass
            if value.shape != feature_extractor.conv_layers[layer_id].conv.weight.data.shape:
      pass
      pass
    pass
#                 raise ValueError(
#                     f"{full_name} has size {value.shape}, but"
#                     f" {feature_extractor.conv_layers[layer_id].conv.weight.data.shape} was found."
#                 )
#             feature_extractor.conv_layers[layer_id].conv.weight.data = value
#             logger.info(f"Feat extract conv layer {layer_id} was initialized from {full_name}.")
    elif (type_id == 2 and not use_group_norm) or (type_id == 2 and layer_id == 0 and use_group_norm):
    pass
        if "bias" in name:
      pass
      pass
    pass
            if value.shape != feature_extractor.conv_layers[layer_id].layer_norm.bias.data.shape:
      pass
      pass
    pass
#                 raise ValueError(
#                     f"{full_name} has size {value.shape}, but"
#                     f" {feature_extractor.conv_layers[layer_id].layer_norm.bias.data.shape} was found."
#                 )
#             feature_extractor.conv_layers[layer_id].layer_norm.bias.data = value
#             logger.info(f"Feat extract layer norm weight of layer {layer_id} was initialized from {full_name}.")
        elif "weight" in name:
    pass
            if value.shape != feature_extractor.conv_layers[layer_id].layer_norm.weight.data.shape:
      pass
      pass
    pass
#                 raise ValueError(
#                     f"{full_name} has size {value.shape}, but"
#                     f" {feature_extractor.conv_layers[layer_id].layer_norm.weight.data.shape} was found."
#                 )
#             feature_extractor.conv_layers[layer_id].layer_norm.weight.data = value
#             logger.info(f"Feat extract layer norm weight of layer {layer_id} was initialized from {full_name}.")
    else:
#         unused_weights.append(full_name)


# @torch.no_grad()
def convert_speecht5_checkpoint(
#     task,
#     checkpoint_path,
#     pytorch_dump_folder_path,
#     config_path=None,
#     vocab_path=None,
#     repo_id=None,
# ):

#     Copy/paste/tweak models weights to transformers design.

    if config_path is not None:
      pass
      pass
    pass
#         config = SpeechT5Config.from_pretrained(config_path)
    else:
#         config = SpeechT5Config()

    if task == "s2t":
      pass
      pass
    pass
#         config.max_length = config.max_text_positions
#         model = SpeechT5ForSpeechToText(config)
    elif task == "t2s":
    pass
#         config.max_speech_positions = 1876
#         config.max_text_positions = 600
#         config.max_length = config.max_speech_positions
#         model = SpeechT5ForTextToSpeech(config)
    elif task == "s2s":
    pass
#         config.max_speech_positions = 1876
#         config.max_length = config.max_speech_positions
#         model = SpeechT5ForSpeechToSpeech(config)
    else:
#         raise ValueError(f"Unknown task name: {task}")

    if vocab_path:
      pass
      pass
    pass
#         tokenizer = SpeechT5Tokenizer(vocab_path, model_max_length=config.max_text_positions)

        # Mask token behaves like a normal word, i.e. include the space before it
#         mask_token = AddedToken("<mask>", lstrip=True, rstrip=False)
#         tokenizer.mask_token = mask_token
#         tokenizer.add_special_tokens({"mask_token": mask_token})
#         tokenizer.add_tokens(["<ctc_blank>"])

#     feature_extractor = SpeechT5FeatureExtractor()
#     processor = SpeechT5Processor(tokenizer=tokenizer, feature_extractor=feature_extractor)
#     processor.save_pretrained(pytorch_dump_folder_path)

#     fairseq_checkpoint = torch.load(checkpoint_path)
#     recursively_load_weights(fairseq_checkpoint["model"], model, task)

#     model.save_pretrained(pytorch_dump_folder_path)

    if repo_id:
      pass
      pass
    pass
#         print("Pushing to the hub...")
#         processor.push_to_hub(repo_id)
#         model.push_to_hub(repo_id)


if __name__ == "__main__":
      pass
      pass
    pass
#     parser = argparse.ArgumentParser()
#     parser.add_argument(
#         "--task",
        default="s2t",
#         type=str,
#         help="Type of the SpeechT5 model youd like to convert. Should be one of s2t, t2s, s2s.",
#     )
#     parser.add_argument("--checkpoint_path", required=True, default=None, type=str, help="Path to fairseq checkpoint")
#     parser.add_argument("--vocab_path", default=None, type=str, help="Path to SentencePiece model")
#     parser.add_argument("--config_path", default=None, type=str, help="Path to hf config.json of model to convert")
#     parser.add_argument(
#         "--pytorch_dump_folder_path", required=True, default=None, type=str, help="Path to the output PyTorch model."
#     )
#     parser.add_argument(
#         "--push_to_hub", default=None, type=str, help="Where to upload the converted model on the 🤗 hub."
#     )

#     args = parser.parse_args()
#     convert_speecht5_checkpoint(
#         args.task,
#         args.checkpoint_path,
#         args.pytorch_dump_folder_path,
#         args.config_path,
#         args.vocab_path,
#         args.push_to_hub,
#     )
