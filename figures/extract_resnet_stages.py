"""Extract real ResNet50 intermediate activations for the embedding slide.

Runs in the `visatlas` conda env (TensorFlow 2.8). Uses the official released
weights (11250.h5 + forvis2.h5) and the exact app.py preprocessing:

    RGB -> white-pad to 2:1 -> resize 256x128 (BILINEAR) -> model
    (Rescaling 1/127.5, offset -1 inside the model)

Saves to /tmp/opencode/act/:
    input.npy   preprocessed network input (128, 256, 3), uint8
    conv1.npy   conv1_relu,       3 selected channels (3, 64, 128)
    mid.npy     conv3_block4_out, 3 selected channels (3, 16, 32)
    deep.npy    conv5_block3_out, 3 selected channels (3, 4, 8)
    gap.npy     global average pooling output (2048,)
    probs.npy   ensemble probabilities in released class order (11,)
    meta.json   channel indices, class order, source image, top class

Run:
    source /home/yaojunhe/miniconda3/etc/profile.d/conda.sh
    conda activate visatlas
    export LD_LIBRARY_PATH=$CONDA_PREFIX/lib:/usr/lib/wsl/lib:$LD_LIBRARY_PATH
    python figures/extract_resnet_stages.py
"""

import json
import os

import numpy as np
import tensorflow as tf
from PIL import Image

BACKEND = "/home/yaojunhe/repro/VisAtlas-Code/Backend"
IMAGE = ("/home/yaojunhe/repro/data/train/Crawled data/point/506.png")
OUT = "/tmp/opencode/act"

CLASSES = ["circle", "point", "net", "line", "area", "bar",
           "map", "matrix", "table", "word", "diagram"]
N_CHANNELS = 3


def build_model(weights):
    base = tf.keras.applications.ResNet50(input_shape=(128, 256, 3),
                                          include_top=False, weights=None)
    inputs = tf.keras.Input(shape=(128, 256, 3))
    x = tf.keras.layers.Rescaling(1. / 127.5, offset=-1)(inputs)
    x = base(x)
    gap = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.Dropout(0.2)(gap)
    logits = tf.keras.layers.Dense(11)(x)
    model = tf.keras.Model(inputs, logits)
    model.load_weights(os.path.join(BACKEND, weights))
    return model, base, tf.keras.Model(inputs, gap)


def preprocess(path):
    im = Image.open(path).convert("RGB")
    width, height = im.size
    if width >= 2 * height:
        top = (width // 2 - height) // 2
        im1 = Image.new("RGB", (width, width // 2), (255, 255, 255))
        im1.paste(im, (0, top))
    else:
        left = (2 * height - width) // 2
        im1 = Image.new("RGB", (2 * height, height), (255, 255, 255))
        im1.paste(im, (left, 0))
    ref = im1.resize((256, 128), Image.BILINEAR)
    return np.asarray(ref, dtype=np.uint8)


def softmax(x):
    e = np.exp(x - x.max())
    return e / e.sum()


def top_channels(feat, k=N_CHANNELS):
    score = feat.reshape(feat.shape[-1], -1).std(axis=1)
    return np.argsort(score)[::-1][:k]


def main():
    os.makedirs(OUT, exist_ok=True)
    tf.get_logger().setLevel("ERROR")

    model_a, base_a, _ = build_model("11250.h5")
    model_b, _, _ = build_model("forvis2.h5")

    x_img = preprocess(IMAGE)
    x = x_img[None].astype(np.float32)
    xr = x / 127.5 - 1.0

    feats = [base_a.get_layer(n).output for n in
             ("conv1_relu", "conv3_block4_out", "conv5_block3_out")]
    gap_out = tf.keras.layers.GlobalAveragePooling2D()(feats[2])
    act = tf.keras.Model(base_a.input, feats + [gap_out])

    conv1, mid, deep, gap = act.predict(xr, verbose=0)
    probs = (2 * softmax(model_a.predict(x, verbose=0)[0])
             + softmax(model_b.predict(x, verbose=0)[0])) / 3.0

    chans = {"conv1": top_channels(conv1[0]),
             "mid": top_channels(mid[0]),
             "deep": top_channels(deep[0])}

    np.save(f"{OUT}/input.npy", x_img)
    np.save(f"{OUT}/conv1.npy", conv1[0][..., chans["conv1"]].transpose(2, 0, 1))
    np.save(f"{OUT}/mid.npy", mid[0][..., chans["mid"]].transpose(2, 0, 1))
    np.save(f"{OUT}/deep.npy", deep[0][..., chans["deep"]].transpose(2, 0, 1))
    np.save(f"{OUT}/gap.npy", gap[0])
    np.save(f"{OUT}/probs.npy", probs)
    meta = {
        "image": IMAGE,
        "classes": CLASSES,
        "channels": {k: [int(i) for i in v] for k, v in chans.items()},
        "shapes": {"conv1": list(conv1.shape[1:]),
                   "mid": list(mid.shape[1:]),
                   "deep": list(deep.shape[1:]),
                   "gap": int(gap.shape[1])},
        "top_class": CLASSES[int(np.argmax(probs))],
        "top_prob": float(np.max(probs)),
    }
    with open(f"{OUT}/meta.json", "w") as f:
        json.dump(meta, f, indent=2)
    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main()
