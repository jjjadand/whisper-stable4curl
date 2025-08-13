
recommend option to compile:
```bash
# build the project
cmake -B build -DGGML_CUDA=1 -DGGML_CUDA=1
cmake --build build -j --config Release

# transcribe an audio file
./build/bin/whisper-cli -f samples/jfk.wav
```

Real-time audio input example:
```bash
./build/bin/whisper-stream -m ./models/ggml-base.en-q5_1.bin -t 8 --step 600 --length 5000 -vth 5 --keep 1200
```

or:
```bash
./build/bin/whisper-stream -m ./models/ggml-base.en-q5_1.bin -t 8 --step 0 --length 7000 -vth 0.7 --keep 1200
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

## Memory usage

| Model  | Disk    | Mem     |
| ------ | ------- | ------- |
| tiny   | 75 MiB  | ~273 MB |
| base   | 142 MiB | ~388 MB |
| small  | 466 MiB | ~852 MB |
| medium | 1.5 GiB | ~2.1 GB |
| large  | 2.9 GiB | ~3.9 GB |

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


## Controlling the length of the generated text segments (experimental)

For example, to limit the line length to a maximum of 16 characters, simply add `-ml 16`:

```text
$ ./build/bin/whisper-cli -m ./models/ggml-base.en.bin -f ./samples/jfk.wav -ml 16

whisper_model_load: loading model from './models/ggml-base.en.bin'
...
system_info: n_threads = 4 / 10 | AVX2 = 0 | AVX512 = 0 | NEON = 1 | FP16_VA = 1 | WASM_SIMD = 0 | BLAS = 1 |

main: processing './samples/jfk.wav' (176000 samples, 11.0 sec), 4 threads, 1 processors, lang = en, task = transcribe, timestamps = 1 ...

[00:00:00.000 --> 00:00:00.850]   And so my
[00:00:00.850 --> 00:00:01.590]   fellow
[00:00:01.590 --> 00:00:04.140]   Americans, ask
[00:00:04.140 --> 00:00:05.660]   not what your
[00:00:05.660 --> 00:00:06.840]   country can do
[00:00:06.840 --> 00:00:08.430]   for you, ask
[00:00:08.430 --> 00:00:09.440]   what you can do
[00:00:09.440 --> 00:00:10.020]   for your
[00:00:10.020 --> 00:00:11.000]   country.
```

## Word-level timestamp (experimental)

The `--max-len` argument can be used to obtain word-level timestamps. Simply use `-ml 1`:

```text
$ ./build/bin/whisper-cli -m ./models/ggml-base.en.bin -f ./samples/jfk.wav -ml 1

whisper_model_load: loading model from './models/ggml-base.en.bin'
...
system_info: n_threads = 4 / 10 | AVX2 = 0 | AVX512 = 0 | NEON = 1 | FP16_VA = 1 | WASM_SIMD = 0 | BLAS = 1 |

main: processing './samples/jfk.wav' (176000 samples, 11.0 sec), 4 threads, 1 processors, lang = en, task = transcribe, timestamps = 1 ...

[00:00:00.000 --> 00:00:00.320]
[00:00:00.320 --> 00:00:00.370]   And
[00:00:00.370 --> 00:00:00.690]   so
[00:00:00.690 --> 00:00:00.850]   my
[00:00:00.850 --> 00:00:01.590]   fellow
[00:00:01.590 --> 00:00:02.850]   Americans
[00:00:02.850 --> 00:00:03.300]  ,
[00:00:03.300 --> 00:00:04.140]   ask
[00:00:04.140 --> 00:00:04.990]   not
[00:00:04.990 --> 00:00:05.410]   what
[00:00:05.410 --> 00:00:05.660]   your
[00:00:05.660 --> 00:00:06.260]   country
[00:00:06.260 --> 00:00:06.600]   can
[00:00:06.600 --> 00:00:06.840]   do
[00:00:06.840 --> 00:00:07.010]   for
[00:00:07.010 --> 00:00:08.170]   you
[00:00:08.170 --> 00:00:08.190]  ,
[00:00:08.190 --> 00:00:08.430]   ask
[00:00:08.430 --> 00:00:08.910]   what
[00:00:08.910 --> 00:00:09.040]   you
[00:00:09.040 --> 00:00:09.320]   can
[00:00:09.320 --> 00:00:09.440]   do
[00:00:09.440 --> 00:00:09.760]   for
[00:00:09.760 --> 00:00:10.020]   your
[00:00:10.020 --> 00:00:10.510]   country
[00:00:10.510 --> 00:00:11.000]  .
```

## Speaker segmentation via tinydiarize (experimental)

More information about this approach is available here: https://github.com/ggml-org/whisper.cpp/pull/1058

Sample usage:

```py
# download a tinydiarize compatible model
./models/download-ggml-model.sh small.en-tdrz

# run as usual, adding the "-tdrz" command-line argument
./build/bin/whisper-cli -f ./samples/a13.wav -m ./models/ggml-small.en-tdrz.bin -tdrz
...
main: processing './samples/a13.wav' (480000 samples, 30.0 sec), 4 threads, 1 processors, lang = en, task = transcribe, tdrz = 1, timestamps = 1 ...
...
[00:00:00.000 --> 00:00:03.800]   Okay Houston, we've had a problem here. [SPEAKER_TURN]
[00:00:03.800 --> 00:00:06.200]   This is Houston. Say again please. [SPEAKER_TURN]
[00:00:06.200 --> 00:00:08.260]   Uh Houston we've had a problem.
[00:00:08.260 --> 00:00:11.320]   We've had a main beam up on a volt. [SPEAKER_TURN]
[00:00:11.320 --> 00:00:13.820]   Roger main beam interval. [SPEAKER_TURN]
[00:00:13.820 --> 00:00:15.100]   Uh uh [SPEAKER_TURN]
[00:00:15.100 --> 00:00:18.020]   So okay stand, by thirteen we're looking at it. [SPEAKER_TURN]
[00:00:18.020 --> 00:00:25.740]   Okay uh right now uh Houston the uh voltage is uh is looking good um.
[00:00:27.620 --> 00:00:29.940]   And we had a a pretty large bank or so.
```

## Karaoke-style movie generation (experimental)

The [whisper-cli](examples/cli) example provides support for output of karaoke-style movies, where the
currently pronounced word is highlighted. Use the `-owts` argument and run the generated bash script.
This requires to have `ffmpeg` installed.

Here are a few _"typical"_ examples:

```bash
./build/bin/whisper-cli -m ./models/ggml-base.en.bin -f ./samples/jfk.wav -owts
source ./samples/jfk.wav.wts
ffplay ./samples/jfk.wav.mp4
```

https://user-images.githubusercontent.com/1991296/199337465-dbee4b5e-9aeb-48a3-b1c6-323ac4db5b2c.mp4

---

```bash
./build/bin/whisper-cli -m ./models/ggml-base.en.bin -f ./samples/mm0.wav -owts
source ./samples/mm0.wav.wts
ffplay ./samples/mm0.wav.mp4
```

https://user-images.githubusercontent.com/1991296/199337504-cc8fd233-0cb7-4920-95f9-4227de3570aa.mp4

---

```bash
./build/bin/whisper-cli -m ./models/ggml-base.en.bin -f ./samples/gb0.wav -owts
source ./samples/gb0.wav.wts
ffplay ./samples/gb0.wav.mp4
```

https://user-images.githubusercontent.com/1991296/199337538-b7b0c7a3-2753-4a88-a0cd-f28a317987ba.mp4

---

## Video comparison of different models

Use the [scripts/bench-wts.sh](https://github.com/ggml-org/whisper.cpp/blob/master/scripts/bench-wts.sh) script to generate a video in the following format:

```bash
./scripts/bench-wts.sh samples/jfk.wav
ffplay ./samples/jfk.wav.all.mp4
```

https://user-images.githubusercontent.com/1991296/223206245-2d36d903-cf8e-4f09-8c3b-eb9f9c39d6fc.mp4

---

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

## [Bindings](https://github.com/ggml-org/whisper.cpp/discussions/categories/bindings)

- [x] Rust: [tazz4843/whisper-rs](https://github.com/tazz4843/whisper-rs) | [#310](https://github.com/ggml-org/whisper.cpp/discussions/310)
- [x] JavaScript: [bindings/javascript](bindings/javascript) | [#309](https://github.com/ggml-org/whisper.cpp/discussions/309)
  - React Native (iOS / Android): [whisper.rn](https://github.com/mybigday/whisper.rn)
- [x] Go: [bindings/go](bindings/go) | [#312](https://github.com/ggml-org/whisper.cpp/discussions/312)
- [x] Java:
  - [GiviMAD/whisper-jni](https://github.com/GiviMAD/whisper-jni)
- [x] Ruby: [bindings/ruby](bindings/ruby) | [#507](https://github.com/ggml-org/whisper.cpp/discussions/507)
- [x] Objective-C / Swift: [ggml-org/whisper.spm](https://github.com/ggml-org/whisper.spm) | [#313](https://github.com/ggml-org/whisper.cpp/discussions/313)
  - [exPHAT/SwiftWhisper](https://github.com/exPHAT/SwiftWhisper)
- [x] .NET: | [#422](https://github.com/ggml-org/whisper.cpp/discussions/422)
  - [sandrohanea/whisper.net](https://github.com/sandrohanea/whisper.net)
  - [NickDarvey/whisper](https://github.com/NickDarvey/whisper)
- [x] Python: | [#9](https://github.com/ggml-org/whisper.cpp/issues/9)
  - [stlukey/whispercpp.py](https://github.com/stlukey/whispercpp.py) (Cython)
  - [AIWintermuteAI/whispercpp](https://github.com/AIWintermuteAI/whispercpp) (Updated fork of aarnphm/whispercpp)
  - [aarnphm/whispercpp](https://github.com/aarnphm/whispercpp) (Pybind11)
  - [abdeladim-s/pywhispercpp](https://github.com/abdeladim-s/pywhispercpp) (Pybind11)
- [x] R: [bnosac/audio.whisper](https://github.com/bnosac/audio.whisper)
- [x] Unity: [macoron/whisper.unity](https://github.com/Macoron/whisper.unity)

## XCFramework
The XCFramework is a precompiled version of the library for iOS, visionOS, tvOS,
and macOS. It can be used in Swift projects without the need to compile the
library from source. For example, the v1.7.5 version of the XCFramework can be
used as follows:

```swift
// swift-tools-version: 5.10
// The swift-tools-version declares the minimum version of Swift required to build this package.

import PackageDescription

let package = Package(
    name: "Whisper",
    targets: [
        .executableTarget(
            name: "Whisper",
            dependencies: [
                "WhisperFramework"
            ]),
        .binaryTarget(
            name: "WhisperFramework",
            url: "https://github.com/ggml-org/whisper.cpp/releases/download/v1.7.5/whisper-v1.7.5-xcframework.zip",
            checksum: "c7faeb328620d6012e130f3d705c51a6ea6c995605f2df50f6e1ad68c59c6c4a"
        )
    ]
)
```

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


