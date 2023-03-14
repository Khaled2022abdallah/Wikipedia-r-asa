from typing import Any, Text, Dict, List, cast
import wikipedia
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionWikipediaSearch(Action):
    def name(self) -> Text:
        return "action_wikipedia_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        sci = tracker.latest_message["entities"][0]["value"]
        dispatcher.utter_message("Trying to retrieve info on " + sci)
        wiki_wiki = wikipedia.set_lang('en')
        try:
            page_py = wiki_wiki.page(sci)
            if page_py.exists():
                sentences = page_py.summary.split(".")
                # get 4 sentences of the summary
                text = ".".join(sentences[:4]) + "."
                dispatcher.utter_message(text=text)
            else:
                dispatcher.utter_message("Sorry, I couldn't find any information on " + sci)
        except Exception as e:
            dispatcher.utter_message(text=f"Sorry, there was an error while searching Wikipedia: {e}")
        return []
