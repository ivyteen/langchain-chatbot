import utils
import streamlit as st
import requests
import asyncio

st.set_page_config(page_title="Study Assistant", page_icon="💬")
st.header('Study Assistant (by Azure)')
st.write('학습중 궁금한 부분에 대해 질문해 보세요.')


class Basic:

    def __init__(self):
        self.server_url = "http://fastapi:8000/chat/"

    def send_query_to_server(self,user_query):        
        """FastAPI 서버에 사용자의 질문을 전송하고 응답을 받습니다."""
        data = {"messages": [{"role": "user", "content": user_query}]}
        response = requests.post(self.server_url, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Error communicating with the server.")
            return None


    #처음 페이지가 로딩될 때 enable_chat_history 로직이 실행되고 main 함수 리턴
    @utils.enable_chat_history
    #async def main(self):
    def main(self):        
        #chain = self.setup_chain()
        user_query = st.chat_input(placeholder="질문을 입력하세요")
        if user_query:
            utils.display_msg(user_query, 'user')
            with st.chat_message("assistant"):

                with st.spinner("답변을 생성하고 있습니다..."):
                    server_response = self.send_query_to_server(user_query)
                    print(server_response)
                    response = server_response['choices'][0]['message']['content']
                    print(response)

                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.rerun()


if __name__ == "__main__":
    obj = Basic()
    obj.main()