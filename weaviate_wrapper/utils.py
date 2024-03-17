def generate_headers(environment: dict) -> dict:
    headers = {}
    if "OPENAI_APIKEY" in environment:
        headers["X-Openai-Api-Key"] = environment["OPENAI_APIKEY"]
    if headers == {}:
        raise Exception("Must provide api keys of at least one embedding provider")
    return headers
