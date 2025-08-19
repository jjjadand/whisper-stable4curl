## Quickly start
**Including voice activation, automatic input termination detection, stream output, WAV output, and automatic device recognition.**

download model:

```bash
./models/download-ggml-model.sh base.en-q5_1
```

recommend option to compile:

```bash
export PATH=/usr/local/cuda-12.6/bin${PATH:+:${PATH}}
export LD_LIBRARY_PATH=/usr/local/cuda-12.6/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
```

```bash
sudo apt install libsdl2-dev
sudo apt install nlohmann-json3-dev
sudo apt-get install libjsoncpp-dev
```

```bash
# build the project
cmake -B build -DGGML_CUDA=1 -DWHISPER_SDL2=ON
cmake --build build -j --config Release

# transcribe an audio file
./build/bin/whisper-cli -f samples/jfk.wav
```

Real-time audio input example:
```bash
sudo ./build/bin/whisper-stream -m ./models/ggml-base.en-q5_1.bin -t 8 --step 600 --length 5000 -vth 5 --keep 1200
```

or:
```bash
sudo ./build/bin/whisper-stream -m ./models/ggml-base.en-q5_1.bin -t 8 --step 0 --length 7000 -vth 0.7 --keep 1200
```

---

For a quick demo, simply run `make base.en`.

The command downloads the `base.en` model converted to custom `ggml` format and runs the inference on all `.wav` samples in the folder `samples`.

For detailed usage instructions, run: `./build/bin/whisper-cli -h`

Note that the [whisper-cli](examples/cli) example currently runs only with 16-bit WAV files, so make sure to convert your input before running the tool.
For example, you can use `ffmpeg` like this:

```bash
ffmpeg -i input.mp3 -ar 16000 -ac 1 -c:a pcm_s16le output.wav
```

## More audio samples

If you want some extra audio samples to play with, simply run:

```
make -j samples
```

This will download a few more audio files from Wikipedia and convert them to 16-bit WAV format via `ffmpeg`.

You can download and run the other models as follows:

```
make -j tiny.en
make -j tiny
make -j base.en
make -j base
make -j small.en
make -j small
make -j medium.en
make -j medium
make -j large-v1
make -j large-v2
make -j large-v3
make -j large-v3-turbo
```


## POWER VSX Intrinsics

`whisper.cpp` supports POWER architectures and includes code which
significantly speeds operation on Linux running on POWER9/10, making it
capable of faster-than-realtime transcription on underclocked Raptor
Talos II. Ensure you have a BLAS package installed, and replace the
standard cmake setup with:

```bash
# build with GGML_BLAS defined
cmake -B build -DGGML_BLAS=1
cmake --build build -j --config Release
./build/bin/whisper-cli [ .. etc .. ]
```

## Quantization

`whisper.cpp` supports integer quantization of the Whisper `ggml` models.
Quantized models require less memory and disk space and depending on the hardware can be processed more efficiently.

Here are the steps for creating and using a quantized model:

```bash
# quantize a model with Q5_0 method
cmake -B build
cmake --build build -j --config Release
./build/bin/quantize models/ggml-base.en.bin models/ggml-base.en-q5_0.bin q5_0

# run the examples as usual, specifying the quantized model file
./build/bin/whisper-cli -m models/ggml-base.en-q5_0.bin ./samples/gb0.wav
```


## NVIDIA GPU compile

With NVIDIA cards the processing of the models is done efficiently on the GPU via cuBLAS and custom CUDA kernels.
First, make sure you have installed `cuda`: https://developer.nvidia.com/cuda-downloads

Now build `whisper.cpp` with CUDA support:

```
cmake -B build -DGGML_CUDA=1
cmake --build build -j --config Release
```

or for newer NVIDIA GPU's (RTX 5000 series):
```
cmake -B build -DGGML_CUDA=1 -DCMAKE_CUDA_ARCHITECTURES="86"
cmake --build build -j --config Release
```


## Benchmarks

In order to have an objective comparison of the performance of the inference across different system configurations,
use the [whisper-bench](examples/bench) tool. The tool simply runs the Encoder part of the model and prints how much time it
took to execute it. The results are summarized in the following Github issue:

[Benchmark results](https://github.com/ggml-org/whisper.cpp/issues/89)

Additionally a script to run whisper.cpp with different models and audio files is provided [bench.py](scripts/bench.py).

You can run it with the following command, by default it will run against any standard model in the models folder.

```bash
python3 scripts/bench.py -f samples/jfk.wav -t 2,4,8 -p 1,2
```

It is written in python with the intention of being easy to modify and extend for your benchmarking use case.

It outputs a csv file with the results of the benchmarking.

## `ggml` format

The original models are converted to a custom binary format. This allows to pack everything needed into a single file:

- model parameters
- mel filters
- vocabulary
- weights

You can download the converted models using the [models/download-ggml-model.sh](models/download-ggml-model.sh) script
or manually from here:

- https://huggingface.co/ggerganov/whisper.cpp

For more details, see the conversion script [models/convert-pt-to-ggml.py](models/convert-pt-to-ggml.py) or [models/README.md](models/README.md).

## Voice Activity Detection (VAD)
Support for Voice Activity Detection (VAD) can be enabled using the `--vad`
argument to `whisper-cli`. In addition to this option a VAD model is also
required.

The way this works is that first the audio samples are passed through
the VAD model which will detect speech segments. Using this information the
only the speech segments that are detected are extracted from the original audio
input and passed to whisper for processing. This reduces the amount of audio
data that needs to be processed by whisper and can significantly speed up the
transcription process.


