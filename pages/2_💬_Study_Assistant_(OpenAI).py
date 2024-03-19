import utils
import streamlit as st
#import requests
import asyncio
import websockets
import json
from streaming import StreamHandler

st.set_page_config(page_title="Study Assistant", page_icon="💬")
st.header('Study Assistant (by OpenAI)')
st.write('학습중 궁금한 부분에 대해 질문해 보세요.')


class WsBasic:

    def __init__(self):
        self.server_url = "ws://fastapi:8000/ws_chat/"
        
    async def send_query_to_server(self,user_query,callback):        
        """FastAPI 서버에 사용자의 질문을 전송하고 응답을 받습니다."""
        data = {"messages": [{"role": "user", "content": user_query}]}
        json_data = json.dumps(data)
        print(json_data)

        async with websockets.connect(self.server_url) as websocket:
            await websocket.send(json_data)

            async for message in websocket:
                #print(message)
                callback.write_stream(message)


    #처음 페이지가 로딩될 때 enable_chat_history 로직이 실행되고 main 함수 리턴
    @utils.ws_enable_chat_history
    async def main(self):        
        #print("On main")
        user_query = st.chat_input(placeholder="질문을 입력하세요")

        if user_query:
            utils.display_msg(user_query, 'user')
            with st.chat_message("assistant"):
                st_cb = StreamHandler(st.empty())
                await self.send_query_to_server(user_query,callback=st_cb)
                print(st_cb.text)
                st.session_state.messages.append({"role": "assistant", "content": st_cb.text})
                # st.rerun()        


if __name__ == "__main__":
    obj = WsBasic()
    asyncio.run(obj.main())
    