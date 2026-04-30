import time
import vertexai
from vertexai.generative_models import (
    GenerationConfig,
    GenerativeModel,
#    Part,
#    Tool,
#    Schema,
#    Type,
#    FunctionDeclaration
)
from google.api_core import exceptions as google_exceptions


class Agent:
    def __init__(self, temperature=0.8, model="gemini-2.5-pro", max_tokens=100, api_key=None):
        """
        Agent sınıfı artık her firmanın kendi Gemini API key'i ile çalışabilir.
        api_key parametresi Firm sınıfından aktarılır.
        """

        # ====================================================
        # Vertex AI Bağlantısını Başlat
        # ====================================================


        # ====================================================
        # Model ve ayarlar
        # ====================================================
        self.temperature = temperature
        self.model_name = model
        self.max_tokens = max_tokens

        # Vertex için yapılandırma objesi
        self.generation_config = GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
            top_p=1
        )

        # Model nesnesini yükle
        # model parametresi "gemini-2.5-pro" gibi kısa isim gelirse resource path'e çeviriyoruz.
        # Eğer zaten tam resource path geldiyse olduğu gibi kullanıyoruz.
        if "/" in self.model_name:
            model_resource = self.model_name
        else:
            model_resource = f"projects/sonbitirme-482721/locations/us-central1/publishers/google/models/{self.model_name}"

        self.model = GenerativeModel(model_resource)

    # ========================================================
    # LLM iletişimi (firmaların konuşma ve fiyat kararı aşaması)
    # ========================================================
    def communicate(self, context):
        time.sleep(2)  # Hız sınırlaması için kısa bir bekleme
        """
        context: prompt olarak gönderilecek metin
        """
        prompt = context + "\n\n"
        retries = 15
        backoff_factor = 2
        current_retry = 0

        while current_retry < retries:
            try:
                # Gemini API çağrısı
                response = self.model.generate_content(
                    prompt,
                    generation_config=self.generation_config,
#                    safety_settings={"HARSH": "BLOCK_NONE"},
                     # <-- işte eklenen kısım:
#                    response_schema={
#                        "type": "string",
#                        "max_length": 300    # yaklaşık 100-150 token'a denk gelir
#                    }
                )

                # Yanıt kontrolü
                if not getattr(response, "candidates", None):
                    print("Uyarı: Model candidates boş döndü.")
                    return "AGENT_ERROR: Empty candidates."

                cand0 = response.candidates[0]
                finish_name = getattr(getattr(cand0, "finish_reason", None), "name", None)

                if finish_name not in ["STOP", "MAX_TOKENS"]:
                    print(f"Uyarı: Model yanıtı durduruldu. Sebep: {finish_name}")
                    if getattr(cand0, "safety_ratings", None):
                        print(f"Güvenlik Derecelendirmesi: {cand0.safety_ratings}")
                    return "AGENT_ERROR: Model yanıtı engellendi."

                # Başarılı yanıt
                message = response.text.strip()
                return message

            # Hata yönetimi
            except (google_exceptions.ResourceExhausted, google_exceptions.TooManyRequests) as e:
                if current_retry < retries - 1:
                    wait_time = backoff_factor ** current_retry
                    print(f"RateLimitError (Google): {wait_time} sn sonra yeniden denenecek...")
                    time.sleep(wait_time)
                    current_retry += 1
                else:
                    print(f"Error {e}")
                    raise e

            except (google_exceptions.InternalServerError, google_exceptions.ServiceUnavailable) as e:
                if current_retry < retries - 1:
                    wait_time = backoff_factor ** current_retry
                    print(f"APIError (Google): {wait_time} sn sonra yeniden denenecek...")
                    time.sleep(wait_time)
                    current_retry += 1
                else:
                    raise e

            except Exception as e:
                if current_retry < retries - 1:
                    wait_time = backoff_factor ** current_retry
                    print(f"Bilinmeyen hata: {e}. {wait_time} sn sonra yeniden denenecek...")
                    time.sleep(wait_time)
                    current_retry += 1
                else:
                    print(f"Error {e}")
                    raise e
