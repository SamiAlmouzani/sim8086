#!/bin/bash

# Run the Python script and redirect the output to output.asm
python sim8086.py test/3/listing_0041_add_sub_cmp_jnz > output.asm

# Assemble the output.asm using NASM
nasm output.asm

# Indicate script completion
echo "Script executed successfully."

