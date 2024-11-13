from langchain_core.callbacks import BaseCallbackHandler


class ChatModelStartHandler(BaseCallbackHandler):
    def on_chat_model_start(self, serialized, messages, **kwargs):
        print(messages)
