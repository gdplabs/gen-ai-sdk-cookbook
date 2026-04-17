CUSTOM_DETAIL_CASE_GANGGUAN_CORRECTNESS_EVALUATION_STEPS = [
    "You are provided with 'query', which contains a customer's complaint text "
    "serving as the original reference or source information.",
    "'actual_output' is the model-generated summary or copying with or without any reword from `query` that should "
    "condense the complaint into 1–5 short (or slightly more) easy-to-read and easy-to-understand sentences.",
    "Extract structured fields from both 'query' and 'actual_output': "
    "{actor (customer/system), action (verb), object (service/feature/app), "
    "channel/app (e.g., MyTelkomsel, GoPay), intent_type (request vs issue), "
    "polarity (can/cannot), key context}.",
    "Require at least ACTION + OBJECT in the summary. If OBJECT is missing or too general "
    "to be mapped to the taxonomy, mark score 0.",
    "Check that intent_type (request vs issue) and channel/app stay consistent. "
    "If 'query' targets a third-party account (e.g., GoPay) but the summary switches to a different app "
    "(e.g., MyTelkomsel), score 0.",
    "Copy of a long sentence from `query` with or without any reword use it as `actual_output` is allowed as long as "
    "the sentence is factual, not contradicted and not hallucinated by `query`."
    "So if it copy, it does not matter if the sentence is not summary still give reward by score 1.",
    "If the some word in 'actual_output' is in `AO Keyword: 'actual_output'` or `\nAO Keyword: 'actual_output'` (ignore case sensitivity) then give score 1"
    "For example: AO Keyword: AO_TELKOMSELPORTAL_RESEND_LINK_WEC_FMC, then the"
    "actual_output: ao_telkomselportal_resend_link_wec_fmc give score 1"
    "If the query has the value AO Keyword but actual_output does not contain AO Keyword, then first check whether"
    "actual_output contradicts or hallucinates the query. If it is a fact, then set the value to 1."
    "No need all word in actual_output is include in query, just some word is enough",
    "If the query is too short, but some words in actual_output is include in query (ignore case sensitivity), then give score 1"
    "For example: query: LOS, LOS and actual_output: los, then give score 1. No need all word in actual_output is include in query, just some word is enough",
    "To generate the summary, user used this prompt: 'ALWAYS provide a clear, concise summary "
    "of the main issue in the complaint note, focusing on the core problem without extraneous detail. "
    "If the note is too short or limited to technical jargon, treat the first line or labels like "
    "AO Keyword, Detail Request as the issue summary.'",
    "Check that all information in 'actual_output' is found in, or directly supported by, "
    "the content of 'query'. The summary may omit secondary or supporting details "
    "such as numbers, timestamps, or locations, as long as the main issue remains correct.",
    "Mark the summary as incorrect (score 0) only if it contradicts the 'query', introduces new facts, "
    "or hallucinates information not present in the source.",
    "If the summary changes the factual meaning of the complaint (for example reversing polarity like "
    "'cannot connect' becoming 'can connect'), set the score to 0. Simple rewording or paraphrasing "
    "that preserves the original meaning should still be considered correct.",
    "Some word like 'cannot connect' becoming 'can connect', 'unsubscribe' become 'subscribe', "
    "'unactivate' become 'activate' or similar word, of course it is not correct and give score 0",
    "The summary does not need to cover every single detail from the complaint. Focus on whether the "
    "information it includes is correct, relevant, and factually faithful to the source.",
    "Minor typos, short phrasing, or generalization of numeric or product values are acceptable "
    "if they do not distort the core issue. But take not type can change the meaning of the complaint.",
    "Even if the summary is short (1–2 sentences), as long as it accurately represents the customer's "
    "main problem and contains no hallucination or contradiction, it should still be considered correct.",
    "Assign a higher score if the summary is concise, accurate, faithful, non-contradictory, "
    "and captures the core meaning of the complaint clearly.",
]