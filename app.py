from flask import Flask, render_template, request, jsonify
import string

app = Flask(__name__)

PRECISION = 16
MAX_RANGE = (1 << PRECISION) - 1
HALF = 1 << (PRECISION - 1)
QUARTER = HALF >> 1
THREE_QUARTER = QUARTER * 3


def arithmetic_encode(text):
    steps = []

    # Hitung Frekuensi
    freq = {}
    for c in text:
        freq[c] = freq.get(c, 0) + 1

    # Urutkan simbol
    symbols = sorted(freq.keys())

    # Total Frekuensi
    cum_freq = {}
    total = 0
    for s in symbols:
        cum_freq[s] = total
        total += freq[s]

    cum_freq_high = {}
    for s in symbols:
        cum_freq_high[s] = cum_freq[s] + freq[s]

    # Probability table for display
    prob_table = []
    for s in symbols:
        prob_table.append({
            "symbol": s if s != " " else "⎵",
            "freq": freq[s],
            "prob": round(freq[s] / total, 4),
            "cum_low": cum_freq[s],
            "cum_high": cum_freq_high[s],
            "range_low": round(cum_freq[s] / total, 4),
            "range_high": round(cum_freq_high[s] / total, 4),
        })

    # Arithmetic Coding
    low = 0
    high = MAX_RANGE
    pending_bits = 0
    output_bits = []

    def output_bit(bit):
        nonlocal pending_bits
        output_bits.append(bit)
        while pending_bits > 0:
            output_bits.append(1 - bit)
            pending_bits -= 1

    encoding_steps = []

    for i, c in enumerate(text):
        range_ = high - low + 1
        new_high = low + (range_ * cum_freq_high[c] // total) - 1
        new_low = low + (range_ * cum_freq[c] // total)

        encoding_steps.append({
            "step": i + 1,
            "char": c if c != " " else "⎵",
            "low_before": low,
            "high_before": high,
            "low_after": new_low,
            "high_after": new_high,
            "low_norm": round(new_low / MAX_RANGE, 6),
            "high_norm": round(new_high / MAX_RANGE, 6),
        })

        high = new_high
        low = new_low

        # Renormalisasi / Scaling
        renorm_count = 0
        while True:
            if high < HALF:
                output_bit(0)
            elif low >= HALF:
                output_bit(1)
                low -= HALF
                high -= HALF
            elif low >= QUARTER and high < THREE_QUARTER:
                pending_bits += 1
                low -= QUARTER
                high -= QUARTER
            else:
                break
            low <<= 1
            high = (high << 1) | 1
            renorm_count += 1

    # Finalisasi
    pending_bits += 1
    if low < QUARTER:
        output_bit(0)
    else:
        output_bit(1)

    bitstream = ''.join(map(str, output_bits))

    compression_ratio = round(len(bitstream) / (len(text) * 8) * 100, 2)
    entropy = 0
    import math
    for s in symbols:
         p = freq[s] / total
         entropy -= p * math.log2(p)

    return {
        "success": True,
        "text": text,
        "freq": {k: v for k, v in freq.items()},
        "prob_table": prob_table,
        "bitstream": bitstream,
        "bit_length": len(bitstream),
        "original_bits": len(text) * 8,
        "compression_ratio": compression_ratio,
        "entropy": round(entropy, 4),
        "encoding_steps": encoding_steps,
        "total_chars": len(text),
    }


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/encode", methods=["POST"])
def encode():
    data = request.get_json()
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"success": False, "error": "Teks tidak boleh kosong!"})

    if not all(c in string.ascii_lowercase + " " for c in text):
        return jsonify({"success": False, "error": "Hanya huruf kecil (a-z) dan spasi yang diperbolehkan!"})

    if len(text) > 200:
        return jsonify({"success": False, "error": "Teks maksimal 200 karakter!"})

    try:
        result = arithmetic_encode(text)
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


if __name__ == "__main__":
    app.run(debug=True)