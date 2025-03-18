#!/bin/bash
#need to have run gen_secrets if not already done
docker run --rm -v ./decoder/:/decoder -v ./global.secrets:/global.secrets:ro -v ./deadbeef_build:/out -e DECODER_ID=0xdeadbeef build-decoder
python -m ectf25.utils.flash ./deadbeef_build/max78000.bin /dev/ttyACM0

sleep 1

python -m ectf25_design.gen_subscription global.secrets deadbeef_c1.sub 0xDEADBEEF 0 0 1 -f
python -m ectf25.tv.subscribe deadbeef_c1.sub /dev/ttyACM0

sleep 1

python -m ectf25.utils.stress_test --test-size 1000 --channels=1 encode global.secrets --dump frames/dump.json
python -m ectf25.utils.stress_test --test-size 1000 --channel=1 decode /dev/ttyACM0 frames/dump.json