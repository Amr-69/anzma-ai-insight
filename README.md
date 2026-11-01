# Anzma Tech – Local AI Chatbot

## 1. Project Overview

This project was developed as a local AI chatbot prototype for Anzma Tech. Its objective was to build, test, and evaluate a bilingual AI assistant capable of answering questions in Arabic and English while running language models locally through Ollama.

The project focused on three engineering requirements:

- **Local execution:** Run inference on the local machine without depending on cloud AI APIs or API keys.
- **Model evaluation:** Compare two quantized language models under consistent test conditions.
- **Practical application:** Develop a Python chatbot with model selection, conversation history, and Arabic/English support.

Rather than selecting a model based only on its reputation, I tested both candidates on the actual hardware and evaluated their speed, startup behavior, language quality, and ability to handle security-related scenarios.

## 2. Engineering Environment and Constraints

### Hardware

| Component | Specification |
|---|---|
| CPU | Intel Core i5-10300H |
| GPU | NVIDIA GTX 1650, 4 GB VRAM |
| RAM | Approximately 8 GB |
| Operating system | Windows |
| Python | 3.11.9 |
| Ollama | 0.40.13 |

### Storage architecture

A storage constraint was identified early: the system drive had limited available space, while the E: drive had sufficient capacity.

To avoid filling the system drive, the project and model storage were organized on E:.

- Project directory: `E:\anzma-ai-insight`
- Ollama installation: `E:\Ollama`
- Model directory: `E:\ollama-models`
- Python virtual environment: `E:\anzma-ai-insight\.venv`

The `OLLAMA_MODELS` environment variable was configured to point to the E: drive.

This was an important deployment consideration because model files can consume several gigabytes of storage.

## 3. Model Selection

Two local quantized models were selected for comparison.

| Model | Parameters | Quantization | Approximate size |
|---|---:|---|---:|
| Qwen 2.5 3B | 3B | Q4_K_M | 1.9 GB |
| Llama 3.2 3B | 3B | Local Ollama quantized build; exact quantization not recorded | 2.0 GB |

Both models were installed locally and accessed through Ollama.

The comparison used the same hardware, context setting, and general inference method to make the results as comparable as possible.

## 4. Initial Performance Benchmark: Cold vs. Warm State

The first stage of testing focused on understanding the difference between model startup time and actual generation performance.

**Cold state:** The model was not already loaded in memory. The first request included model-loading overhead.

**Warm state:** The model was already loaded, so the next request measured generation with substantially less startup overhead.

### English benchmark results

Test prompt:

> Explain in two sentences what an access control system is.

Context setting: 2048 tokens.

API method: Ollama `/api/generate`, with streaming disabled.

| Metric | Llama 3.2 3B | Qwen 2.5 3B |
|---|---:|---:|
| Cold model load | 120.85 s | 149.06 s |
| Cold generation speed | 59.46 tokens/s | 54.77 tokens/s |
| Warm model load | 0.41 s | 0.42 s |
| Warm generation speed | 58.27 tokens/s | 57.85 tokens/s |

### Initial observations

1. Llama loaded approximately 28 seconds faster in the recorded cold-start test.
2. Llama achieved a higher cold generation rate in this test.
3. Once loaded, both models generated responses at very similar speeds.
4. Warm model loading was negligible compared with cold startup.

The results showed that startup latency and generation throughput needed to be evaluated separately. Comparing only total response time would mix model-loading overhead with actual generation performance.

These are preliminary single-run measurements, not statistically averaged benchmark results.

## 5. Arabic vs. English Performance

The next stage investigated whether both models could handle Arabic and English effectively.

Arabic prompt:

> اشرح في جملتين ما هو نظام التحكم في الدخول.

English prompt:

> Explain in two sentences what an access control system is.

The purpose was to evaluate both generation performance and language quality.

### Recorded language-related measurements

| Test | Model | Cold load | Generation speed |
|---|---|---:|---:|
| English | Llama 3.2 3B | 120.85 s | 59.46 tokens/s |
| English | Qwen 2.5 3B | 149.06 s | 54.77 tokens/s |
| Arabic | Qwen 2.5 3B | 123.19 s | 54.40 tokens/s |
| Arabic | Llama 3.2 3B | Not recorded | Not recorded |

**Measurement limitation:** The Arabic and English tests were not fully captured as a four-way benchmark. In particular, a matching Arabic benchmark record for Llama and a warm Arabic benchmark record for Qwen were not retained. Exact generated token counts for each response were also not retained.

Therefore, these figures should be treated as recorded generation throughput, not as a complete Arabic-versus-English token-count comparison.

### Language quality observations

The initial tests revealed that speed alone was insufficient to select the best model.

- Qwen produced understandable Arabic, although some responses were awkward or technically weak.
- Llama performed well in the tested English security scenario.
- Llama's initial Arabic security response contained substantial mixed-language text and malformed words.
- Qwen initially had an Arabic encoding issue. This was investigated and corrected by sending UTF-8 encoded request data.

This separated two different problems: terminal/request encoding and the model's actual Arabic generation quality.

## 6. Python Application: Building from a Fresh Start

After establishing the model comparison, I developed the chatbot application in Python.

The implementation uses the local Ollama HTTP API rather than a cloud AI service.

### Application architecture

1. The user starts the Python application.
2. The application displays a model-selection menu.
3. The selected model is sent to the local Ollama chat endpoint.
4. User messages and previous conversation messages are included in the request.
5. Ollama generates a response locally.
6. The application displays the response and stores it in the conversation history.

### Main technologies

- Python 3.11
- Requests
- Ollama
- Local HTTP endpoint: `http://localhost:11434/api/chat`
- UTF-8 input/output handling

### Model selection implementation

The application allows the user to select either model without changing the source code:

```python
MODELS = {
    "1": "qwen2.5:3b",
    "2": "llama3.2:3b"
}
```

### Local API communication

The chatbot sends its conversation to Ollama using the following approach:

```python
payload = {
    "model": model,
    "messages": conversation,
    "stream": False,
    "options": {
        "num_ctx": 2048
    }
}

response = requests.post(
    "http://localhost:11434/api/chat",
    json=payload,
    timeout=300
)

response.raise_for_status()
result = response.json()
answer = result["message"]["content"]
```

### Application features

- Interactive model selection.
- Arabic and English input.
- Conversation history.
- Same-language response instructions.
- UTF-8 terminal support.
- Local Ollama communication.
- Connection and timeout error handling.
- Conversation-history management.
- Exit command.

The implementation was kept intentionally lightweight to make the application easy to run and demonstrate.

## 7. System Prompt Engineering and Iterative Improvement

The first implementation used a security-focused system prompt.

Testing revealed that the prompt and model behavior both influenced the quality of the answers.

For example, when asked a general AI question, the assistant could overemphasize security-related topics because the original prompt strongly specialized it in physical security.

The Arabic tests also revealed that asking a model to respond in Arabic was not enough to guarantee natural Arabic output.

### Problems identified

- Mixing English technical terms into Arabic sentences.
- Producing malformed or incomplete Arabic words.
- Giving generic or repetitive recommendations.
- Inventing technical details.
- Failing to distinguish possible causes from confirmed causes.
- Over-specializing answers even when the user asked a general question.

### Prompt improvement

The system prompt was revised to include explicit language and answer-quality rules.

The updated prompt instructs the model to:

1. Detect the language of the user's message.
2. Respond in the same language.
3. Use clear, professional Modern Standard Arabic for Arabic questions.
4. Avoid unnecessary English words in Arabic sentences.
5. Translate technical terms and provide their English equivalents in parentheses when necessary.
6. Avoid inventing facts, system features, or incidents.
7. Distinguish possible causes from confirmed causes.
8. Recommend safe and authorized investigation steps.
9. Use previous conversation messages when answering follow-up questions.
10. Admit when information is not available in the conversation.

### Results after prompt improvement

The same synthetic security scenario was used to evaluate both models:

> يوجد ثلاث محاولات دخول مرفوضة إلى باب منطقة محظورة خلال خمس دقائق. اشرح الأسباب المحتملة واقترح خطوات آمنة للتحقيق في الواقعة.

**Qwen 2.5 3B:**

- Produced understandable Arabic.
- Organized the response into possible causes and investigation steps.
- Still included generic or repetitive recommendations.
- Mentioned company-specific legal procedures that had not been supplied to the model.
- Needed better technical precision.

**Llama 3.2 3B:**

- Produced substantially less reliable Arabic.
- Included malformed words and mixed Arabic-English sentences.
- Suggested irrelevant or unclear technical checks.
- Did not consistently provide actionable investigation steps.

### Prompt-engineering conclusion

The revised prompt improved the clarity of Qwen's Arabic response, but it did not eliminate technical inaccuracies.

Llama continued to show significant Arabic generation problems in this test.

This demonstrated an important engineering limitation: prompt engineering can guide model behavior, but it cannot fully compensate for limitations in the underlying language model.

## 8. Model Selection Decision

Based on the recorded tests:

**Qwen 2.5 3B was selected as the provisional default model.**

Reasons:

- More readable Arabic in the tested security scenario.
- Comparable warm generation speed to Llama.
- Better overall bilingual behavior in the tests conducted.

Llama 3.2 3B remains available in the application as a comparison model and performed well in the English security scenario.

This decision is based on the project's actual test results rather than assuming that one model is universally superior.

## 9. Example Security Scenario

The application was tested with a synthetic building-security event:

> Three denied access attempts occurred at a restricted door within five minutes.

The chatbot was expected to identify possible explanations such as:

- An expired or unauthorized access credential.
- Incorrect access permissions.
- A card-reader or door-controller malfunction.
- A potentially unauthorized access attempt.

The expected investigation approach includes:

1. Preserve the relevant access-control logs.
2. Verify timestamps and credential identifiers.
3. Review relevant camera footage where authorized.
4. Check the door reader and controller status.
5. Confirm access permissions with an authorized administrator.
6. Document findings and escalate according to site procedures.

The model should not treat denied attempts alone as proof of an intrusion.

## 10. Running the Application

### Requirements

- Windows.
- Python 3.11 or compatible version.
- Ollama installed locally.
- Both comparison models downloaded.
- Python dependencies installed.

### Install Python dependencies

```powershell
pip install -r requirements.txt
```

### Start Ollama

Use the project's startup script:

```powershell
.\start-ollama.ps1
```

### Run the chatbot

```powershell
python chatbot.py
```

Select the desired model:

```text
1. Qwen 2.5 3B
2. Llama 3.2 3B
```

Type `exit` to close the conversation.

## 11. Privacy and Local Execution

The application communicates with the Ollama server through the local endpoint:

`http://localhost:11434`

No cloud AI API or API key is required by the Python application.

The models are stored locally on the E: drive.

The startup configuration includes `OLLAMA_NO_CLOUD=1`. However, a successful disconnected-network test is required before claiming that the complete setup has been independently verified to operate offline.

## 12. Limitations and Future Improvements

This prototype has several known limitations:

- Arabic technical response quality is not perfect.
- Results can vary between models and prompts.
- Benchmark measurements are preliminary single-run observations.
- Complete Arabic and English token-count records were not retained.
- Cold startup takes significantly longer than warm inference.
- The application does not connect to real access-control hardware or company security systems.
- AI-generated security recommendations require human verification.

Potential future improvements:

- Repeated benchmark runs with averages and standard deviations.
- Separate Arabic and English token-count and throughput measurements.
- Streaming responses to improve perceived responsiveness.
- More robust Arabic terminology evaluation.
- Automated test cases for conversation memory.
- A graphical user interface.
- Offline operation verification and a documented deployment procedure.

## 13. Engineering Approach and Lessons Learned

The project was approached as an engineering problem rather than simply a model-installation exercise.

The work was divided into distinct stages:

1. **Environment preparation:** Establish Python, Git, Ollama, and dedicated E: drive storage.
2. **Model acquisition:** Install two comparable local models.
3. **Performance measurement:** Separate cold-start latency from warm generation speed.
4. **Language evaluation:** Test Arabic and English rather than relying on English benchmarks alone.
5. **Application development:** Build a Python interface with model selection and conversation history.
6. **Problem diagnosis:** Investigate UTF-8 encoding and distinguish technical communication issues from model-quality issues.
7. **Prompt iteration:** Improve the system prompt based on observed failures.
8. **Comparative evaluation:** Retest both models using the same security scenario.
9. **Decision-making:** Select the provisional default model based on measured performance and observed response quality.

The main lesson was that a successful local AI application requires more than downloading a model. It requires controlled testing, resource management, application design, language evaluation, error diagnosis, and evidence-based model selection.

---

**Project status:** Prototype implementation and preliminary model evaluation. Final Git verification, live demonstration, and offline verification remain part of the delivery process.