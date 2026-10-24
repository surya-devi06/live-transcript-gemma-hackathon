# Google Gemma Model Integration Details

## 1. Role of Gemma in Live Transcript AI

While speech recognition converts sound to raw text, raw transcripts are notoriously noisy, full of filler words, repetitions, and unstructured flow. **Google Gemma** acts as the cognitive engine that converts this raw text into structured human knowledge.

We use Gemma for two critical features:
1. **Hierarchical Academic Note Generation**: Summarizing the text, extracting core terminology, and organizing ideas logically.
2. **Strictly Grounded Question-Answering**: Providing answers backed by timestamped citations and refusing to hallucinate when asked questions outside the transcript scope.

---

## 2. Model Selection & Fallback Strategy

The application is built around the **Google Gen AI SDK (`google-genai`)** and prioritizes:

- **Primary Target**: `gemma-4-26b-a4b-it` (Google Gemma 4 Instruction Tuned)
- **Fallback Options**:
  - `gemma-3-27b-it`
  - `gemma-3-12b-it`
  - `gemma-3-4b-it`
  - `gemma-2-27b-it`
  - `gemma-2-9b-it`

The user can seamlessly switch between variants from the UI sidebar without modifying code or restarting the application.

---

## 3. Grounding & Anti-Hallucination Architecture

To prevent generative models from inventing facts, we implement:

1. **System Persona Prompting**: Restricts the model to act as an objective auditor of the transcript excerpt.
2. **Lexical Keyword Retrieval**: For longer lectures, we rank and pass only the most relevant transcript segments to the prompt context.
3. **Explicit Refusal Instruction**: The system prompt strictly mandates:
   > *"If the transcript does NOT contain the answer, state clearly: 'Based on the provided transcript, there is insufficient evidence to answer this question.' Do NOT extrapolate, hallucinate, or speculate."*
4. **Citation Extraction**: The UI highlights the exact speaker timestamps that substantiate the answer.
