"""Agent that uses a local Hugging Face model (e.g., distilgpt2) for response generation."""
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from ..api_schema import Observation, PersonaCard

class LocalModelAgent:
    def __init__(self, persona: PersonaCard, model_name: str = "gpt2"):
        self.persona = persona
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        # Configure tokenizer/model context handling
        try:
            self.tokenizer.truncation_side = 'left'
        except Exception:
            pass
        if self.tokenizer.pad_token_id is None and hasattr(self.tokenizer, 'eos_token_id'):
            self.tokenizer.pad_token_id = self.tokenizer.eos_token_id
        # Determine maximum context window and reserve space for generation
        max_ctx = getattr(self.model.config, 'n_positions', None) or getattr(self.model.config, 'max_position_embeddings', 1024)
        self.max_context = int(max_ctx)
        self.reserve_new_tokens = 128
        # Leave room for generation tokens
        self.input_max = max(256, self.max_context - self.reserve_new_tokens)

        # Precompute bad word ids to avoid URLs/emails/handles in outputs
        bad_tokens = ["http", "www", "@", "mailto", ".com", ".net", ".org"]
        bad_ids = self.tokenizer(bad_tokens, add_special_tokens=False).input_ids
        # Flatten and filter empties
        self.bad_words_ids = [ids for ids in bad_ids if ids]

    def _build_prompt(self, obs: Observation) -> str:
        # Concise persona + clear response guideline
        persona_desc = (
            f"You are {self.persona.name}, a {self.persona.age}-year-old {self.persona.occupation}.\n"
            f"Speak in {self.persona.linguistics.language}, with a {self.persona.linguistics.speaking_style} style and {self.persona.linguistics.formality_level} tone.\n"
            f"Answer the last Attacker question directly in 1-3 clear sentences. Stay in character. Do not include links, emails, or phone numbers. Never say you're an AI.\n"
        )

        # Use only the last few turns to keep context focused
        history_context = ""
        if obs.history_tail:
            recent = obs.history_tail[-3:]  # last 3 exchanges
            lines = []
            for msg in recent:
                if "attacker" in msg:
                    lines.append(f"Attacker: {msg['attacker']}")
                if "white" in msg:
                    lines.append(f"You: {msg['white']}")
            history_context = "\n".join(lines)

        prompt = (
            f"{persona_desc}"
            f"{history_context}\n"
            f"Attacker: {obs.attacker_msg}\n"
            f"You:"
        )
        return prompt

    def respond(self, obs: Observation) -> str:
        prompt = self._build_prompt(obs)
        # Tokenize with truncation to fit context window
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=self.input_max,
        )
        inputs = {k: v.to(self.model.device) for k, v in inputs.items()}
        with torch.no_grad():
            output = self.model.generate(
                **inputs,
                max_new_tokens=min(self.reserve_new_tokens, 96),
                do_sample=False,  # Greedy for coherence
                num_beams=1,
                repetition_penalty=1.1,
                no_repeat_ngram_size=3,
                bad_words_ids=self.bad_words_ids or None,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
            )
        # Decode only the newly generated continuation (beyond prompt length)
        gen_ids = output[0]
        prompt_len = inputs["input_ids"].shape[-1]
        continuation_ids = gen_ids[prompt_len:]
        reply = self.tokenizer.decode(continuation_ids, skip_special_tokens=True).strip()
        # Clean up any remaining system prompt artifacts
        if "Attacker:" in reply:
            reply = reply.split("Attacker:")[0].strip()
        return reply

    def submit(self) -> str:
        return "Thank you for the conversation!"
