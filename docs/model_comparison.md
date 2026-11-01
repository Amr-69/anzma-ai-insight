# Local Model Comparison

## 1. Test Environment

| Component | Specification |
|---|---|
| CPU | Intel Core i5-10300H, 4 cores / 8 threads |
| GPU | NVIDIA GTX 1650, 4 GB VRAM |
| System RAM | 7.9 GB |
| Runtime | Ollama |
| Context size | 2048 tokens |
| API | Local Ollama API |
| Execution | Local inference |

Models evaluated:
- Qwen 2.5 3B (`qwen2.5:3b`)
- Llama 3.2 3B (`llama3.2:3b`)

## 2. Model Characteristics

| Metric | Qwen 2.5 3B | Llama 3.2 3B |
|---|---|---|
| Parameters | 3B | 3B |
| Quantization | Q4_K_M | Exact quantization not recorded |
| Approximate model size | 1.9 GB | Approximately 2.0–2.3 GB |

## 3. English Performance: Cold vs. Warm

The following are preliminary single-run measurements, not statistical averages.

| Measurement | Qwen 2.5 3B | Llama 3.2 3B |
|---|---:|---:|
| Cold load time | 149.06 s | 120.85 s |
| Cold generation speed | 54.77 tokens/s | 59.46 tokens/s |
| Warm load time | 0.42 s | 0.41 s |
| Warm generation speed | 57.85 tokens/s | 58.27 tokens/s |

Cold means the model was not already loaded in memory. Warm means the model was already loaded.

## 4. Arabic vs. English Evaluation

English test prompt:

"Explain in two sentences what an access control system is."

Arabic test prompt:

"اشرح في جملتين ما هو نظام التحكم في الدخول."

Recorded Arabic measurements:

| Measurement | Qwen 2.5 3B | Llama 3.2 3B |
|---|---:|---:|
| Cold load time | 123.19 s | Not recorded |
| Generation speed | 54.40 tokens/s | Not recorded |

A complete four-way Arabic/English performance comparison was not recorded. Arabic token counts and time-to-first-token were also not measured consistently.

### Language quality observations

- Qwen generally produced more understandable Arabic, although its wording sometimes sounded unnatural or repetitive.
- Llama performed well on the English security scenario but produced mixed-language and malformed Arabic in some tests.
- Both models demonstrated limitations in following Arabic terminology consistently.

## 5. Memory and Hardware Observations

At a context size of 2048, Llama was observed using approximately 2.3 GB of GPU memory according to the recorded NVIDIA monitoring output.

At a context size of 4096, Llama required more memory and was observed running partly on CPU and partly on GPU.

Equivalent detailed memory measurements for Qwen were not recorded. Therefore, a direct memory comparison is not available.

## 6. Practical Security Scenario

Both models were tested with a synthetic scenario involving three denied access attempts at a restricted door within five minutes.

The evaluation considered:
- Identification of possible causes.
- Safe investigation recommendations.
- Clarity and organization.
- Arabic and English response quality.
- Avoidance of unsupported assumptions.

Qwen produced more understandable Arabic in the recorded tests. However, both models sometimes generated generic or unsupported recommendations.

All model-generated findings must be verified by a qualified human operator.

## 7. Selection Decision

Qwen 2.5 3B is the provisional default model because its Arabic responses were generally more understandable in the recorded tests, while its warm generation speed was close to Llama.

Llama 3.2 3B remains available as an alternative and performed slightly faster in the recorded English benchmark.

This is a preliminary engineering decision based on limited tests, not a universal model ranking.

## 8. Limitations and Further Testing

The following measurements remain incomplete:

- Repeated benchmark runs and statistical averages.
- Complete Arabic and English token counts.
- Consistent time-to-first-token measurements.
- Equivalent RAM and VRAM measurements for both models.
- Exact Llama quantization metadata.
- A controlled offline test with the network disconnected.

The recorded results should be treated as preliminary observations.
