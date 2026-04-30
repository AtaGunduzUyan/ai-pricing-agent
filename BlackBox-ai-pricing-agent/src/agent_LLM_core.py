import os
import time
import vertexai
from vertexai.generative_models import GenerationConfig, GenerativeModel
from google.api_core import exceptions as google_exceptions


class Agent:
    def __init__(
        self,
        temperature: float = 0.8,
        model: str = "gemini-2.5-pro",
        max_tokens: int = 100,
        api_key=None
    ):
        """
        LLM Agent (Vertex AI / Gemini)
        - Project hard-code yoktur
        - GCP_PROJECT env varsa onu kullanır
        """

        # ====================================================
        # Vertex AI init (PROJECT BURADA ÇÖZÜLÜYOR)
        # ====================================================
        project_id = os.environ.get("GCP_PROJECT", "sustained-opus-477620-t0")
        location = os.environ.get("GCP_LOCATION", "us-central1")

        vertexai.init(
            project=project_id,
            location=location
        )

        # ====================================================
        # Model ve ayarlar
        # ====================================================
        self.temperature = temperature
        self.model_name = model
        self.max_tokens = max_tokens

        self.generation_config = GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
            top_p=1
        )

        # ====================================================
        # Model resource path çözümü
        # ====================================================
        if "/" in self.model_name:
            # Tam resource path verilmişse aynen kullan
            model_resource = self.model_name
        else:
            # Kısa isim geldiyse project'e göre resource üret
            model_resource = (
                f"projects/{project_id}/locations/{location}/"
                f"publishers/google/models/{self.model_name}"
            )

        self.model = GenerativeModel(model_resource)

    # ========================================================
    # LLM iletişimi
    # ========================================================
    def communicate(self, context: str) -> str:
        """
        context: prompt olarak gönderilecek metin
        """
        prompt = context + "\n\n"
        retries = 15
        backoff_factor = 2
        attempt = 0

        # Hafif rate-limit koruması
        time.sleep(2)

        while attempt < retries:
            try:
                response = self.model.generate_content(
                    prompt,
                    generation_config=self.generation_config
                )

                # Yanıt güvenliği
                if not getattr(response, "candidates", None):
                    print("[Agent] Uyarı: candidates boş döndü.")
                    return "AGENT_ERROR: Empty candidates."

                cand = response.candidates[0]
                finish_reason = getattr(
                    getattr(cand, "finish_reason", None),
                    "name",
                    None
                )

                if finish_reason not in ["STOP", "MAX_TOKENS", None]:
                    print(f"[Agent] Yanıt durduruldu. Sebep: {finish_reason}")
                    return "AGENT_ERROR: Blocked response."

                text = response.text.strip()
                if not text:
                    return "AGENT_ERROR: Empty response text."

                return text

            # -----------------------------
            # Rate limit / quota
            # -----------------------------
            except (
                google_exceptions.ResourceExhausted,
                google_exceptions.TooManyRequests
            ) as e:
                wait_time = backoff_factor ** attempt
                print(
                    f"[Agent] Rate limit ({attempt+1}/{retries}) → "
                    f"{wait_time} sn bekleniyor..."
                )
                time.sleep(wait_time)
                attempt += 1

            # -----------------------------
            # Sunucu hataları
            # -----------------------------
            except (
                google_exceptions.InternalServerError,
                google_exceptions.ServiceUnavailable
            ) as e:
                wait_time = backoff_factor ** attempt
                print(
                    f"[Agent] Server error ({attempt+1}/{retries}) → "
                    f"{wait_time} sn bekleniyor..."
                )
                time.sleep(wait_time)
                attempt += 1

            # -----------------------------
            # Diğer hatalar
            # -----------------------------
            except Exception as e:
                wait_time = backoff_factor ** attempt
                print(
                    f"[Agent] Beklenmeyen hata ({attempt+1}/{retries}): {e} → "
                    f"{wait_time} sn bekleniyor..."
                )
                time.sleep(wait_time)
                attempt += 1

        # Buraya geldiysek tamamen başarısız
        raise RuntimeError("LLM çağrısı tüm denemelerde başarısız oldu.")
