# Function to get Overview Definition from OpenAI
from openai import OpenAI

client = OpenAI()

from config.logging import setup_logging

logger = setup_logging()

import json


def get_overview_definition(definition):
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """
                        You are an Irish language learning assistant, helping users improve their understanding, vocabulary, pronunciation, and grammar in the Irish language.

                        When provided with a detailed word entry containing definitions in a structured list (e.g., numbered or bullet points), extract and list the key definitions in a simplified single-line, paragraph-style format. Each definition should include the part of speech followed by a concise definition, separated by a semicolon.
                        
                        Please return this as structured data. (Note: "vt." and "vi." stand for "transitive verb" and "intransitive verb" respectively. This information can typically be found in the definition.)
                        
                        example:                    
                        {"word":"doicheallach","adjective_definitions":"(1) churlish, inhospitable","verb_definitions":" vt. vi. (1) to be unwilling to receive someone; (2) to be churlish with someone; (3) to be grudging with something, unwilling to do something","noun_definitions":"(1) churlish, cold welcome; (2) grudging word, smile","other":"(phrase) he gave it grudgingly; (phrase) he is stand-offish in company."}
                        """,
                },
                {
                    "role": "user",
                    "content": definition,
                },
            ],
            temperature=0.3,
            max_tokens=500,
        )
        content = completion.choices[0].message.content.strip()
        logger.debug(f"Raw OpenAI response: {completion.choices[0].message.content}")

        # Parse the JSON response
        structured_data = json.loads(content)
        # overview = structured_data.get("overview_definition", "")
        adjectives = structured_data.get("adjective_definitions", "")
        verbs = structured_data.get("verb_definitions", "")
        nouns = structured_data.get("noun_definitions", "")
        other = structured_data.get("other", "")

        logger.debug(f"structured_data: {structured_data}")
        return (adjectives, verbs, nouns, other)

    except json.JSONDecodeError as jde:
        logger.error(f"JSON decoding failed: {jde}")
        logger.debug(f"Received content: {content}")
        return None
    except Exception as e:
        logger.error(f"Error with OpenAI API: {e}")
        return None
