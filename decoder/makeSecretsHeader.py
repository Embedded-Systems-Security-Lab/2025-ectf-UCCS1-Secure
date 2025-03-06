#!/usr/bin/env python3

import json
import os
from pathlib import Path
import base64


secret_file="/global.secrets"
with open(secret_file, "r") as f:
    secrets = json.load(f)

file_name = "decoder_secrets.h"
device_dir = "/decoder/inc/"

with open(os.path.join(device_dir, file_name), "w") as f:
    f.write("#pragma once\n#ifndef SECRETS_H\n#define SECRETS_H\n\n")

    f.write(f"#define SUB_KEY_SIZE {len(base64.b64decode(secrets['subscription_key']))}\n")
    f.write(f"#define VERIF_KEY_SIZE {len(base64.b64decode(secrets['verification_key']))}\n")
    f.write(f"#define CHANNEL_KEY_SIZE {len(base64.b64decode(secrets['channel_0_key']))}\n\n")
    
    f.write(f"static const uint8_t subscription_key[SUB_KEY_SIZE] = {{ {', '.join(f'0x{b:02X}' for b in base64.b64decode(secrets['subscription_key']))} }}; // subscription update key\n")
    f.write(f"static const uint8_t verification_key[VERIF_KEY_SIZE] = {{ {', '.join(f'0x{b:02X}' for b in base64.b64decode(secrets['verification_key']))} }}; // verification key\n")
    f.write(f"static const uint8_t emergency_channel_key[CHANNEL_KEY_SIZE] = {{ {', '.join(f'0x{b:02X}' for b in base64.b64decode(secrets['channel_0_key']))} }}; // emergency channel key\n")

    f.write("\n#endif // SECRETS_H\n")