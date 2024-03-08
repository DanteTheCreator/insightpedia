from openai import OpenAI


class ContentAnalyzer:
    def __init__(self, base_url="http://host.docker.internal:1234/v1"):
        self.client = OpenAI(base_url=base_url, api_key="not-needed")

    def _generate_response(self, prompt):
        stream = self.client.chat.completions.create(
            model="local-model",
            messages=[{"role": "user", "content": prompt}],
            stream=True,
        )

        response = ""
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                response += chunk.choices[0].delta.content
        return response.strip()

    def summary(self, text):
        prompt = f"Generate a concise summary of the provided Wikipedia article. Please provide a summary that captures the main points and key information from the article:\n{text}"
        return self._generate_response(prompt)

    def key_themes(self, text):
        prompt = f"Identify and list the key themes present in the provided Wikipedia article. Themes are recurring topics or subjects that are central to the article's content. Please extract and present the main themes explored in the article:\n{text}"
        return self._generate_response(prompt)

    def trends(self, text):
        prompt = f"Analyze the provided Wikipedia article to identify any notable trends or patterns. Trends may include developments, changes, or shifts discussed in the article. Please identify and summarize any significant trends observed in the article:\n{text}"
        return self._generate_response(prompt)

    def insights(self, text):
        prompt = f"Generate novel insights from the provided Wikipedia article. Insights should offer unique perspectives or interpretations of the content beyond what is explicitly stated. Please provide insightful analyses or observations based on the information presented in the article:\n{text}"
        return self._generate_response(prompt)
