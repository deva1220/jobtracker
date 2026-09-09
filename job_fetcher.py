import requests
from bs4 import BeautifulSoup


def fetch_job_description(url):
    try:
        response = requests.get(
            url,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove unwanted elements
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        # Find the job description starting from "Description"
        description_heading = soup.find(
            lambda tag: tag.name in ["h1", "h2", "h3", "h4"]
            and "description" in tag.get_text(strip=True).lower()
        )

        if description_heading:
            job_text = []

            # Collect content after Description
            for element in description_heading.find_all_next():
                text = element.get_text(" ", strip=True)

                if text:
                    job_text.append(text)

                # Stop before unrelated footer/job-sharing sections
                if "job details" in text.lower():
                    break

            return "\n".join(job_text)

        # Fallback if Description heading is not found
        main = soup.find(["article", "main"])

        if main:
            return main.get_text(
                separator="\n",
                strip=True
            )

        return soup.get_text(
            separator="\n",
            strip=True
        )

    except requests.RequestException as e:
        return f"Error fetching job page: {e}"