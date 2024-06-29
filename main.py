from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionSmallResultItem import ExtensionSmallResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.utils.fuzzy_search import get_score

from util import cliphist_list, set_clipboard

class Cliphist(Extension):
    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())


class KeywordQueryEventListener(EventListener):
    THRESHOLD = 40
    LIMIT = 15

    def get_list(self, arg):
        for number, preview in cliphist_list():
            try:
                preview = preview.decode()
            except:
                continue

            if arg is not None:
               score = get_score(arg, preview)
            else:
                score = 100

            if score <= self.THRESHOLD:
                continue
            
            yield number, preview, score

    def on_event(self, event, extension):
        arg = event.get_argument()
        history = sorted(self.get_list(arg), key=lambda item: item[2], reverse=True)[:self.LIMIT]
        return RenderResultListAction([
                ExtensionSmallResultItem(name=preview,
                                         on_enter=ExtensionCustomAction(number))
                for number, preview, score in history
              ])


class ItemEnterEventListener(EventListener):
    def on_event(self, event, extension):
        data = event.get_data()
        set_clipboard(data)

if __name__ == '__main__':
    Cliphist().run()

