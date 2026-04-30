import streamlit as st
import requests

st.set_page_config(page_title="中医图谱智能问诊", layout="wide")
st.title("💡 中医图谱·智能问诊")

# 初始化聊天记录
if "messages" not in st.session_state:
    st.session_state.messages = []

# 渲染历史记录（手动渲染，不依赖 chat_message 组件）
for message in st.session_state.messages:
    role_name = "🧑 用户" if message["role"] == "user" else "⚕️ 老中医"
    st.write(f"**{role_name}**: {message['content']}")
    st.write("---")
    

# 兼容版输入框：使用 form 确保回车即可发送
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("描述症状或查询方剂 (回车发送):", key="input")
    submit_button = st.form_submit_button(label="发送")

if submit_button and user_input:
    # 记录用户消息
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # 调用 n8n 后端
    # 必须带上 /chat！
    # 终极正确版 URL：纯血 API 接口，绝对不能带 /chat
    # 1. 换回带有 -test 的测试路线，并且结尾必须加上 /chat！
    webhook_url = "http://n8n:5678/webhook/20bf1d52-65a1-4c1c-b85d-044e0573cfae/chat"
    
    try:
        with st.spinner("老中医正在查阅典籍..."):
            # 2. 构造极其硬核的 n8n 专属 Payload！
            payload = {
                "action": "sendMessage",          # 告诉 n8n 这是一个发送消息的动作
                "sessionId": "streamlit-user-1",  # 给 n8n 一个会话 ID，这样它才能记住上下文
                "chatInput": user_input           # 你的真实问题
            }
            
            # 发送请求
            response = requests.post(webhook_url, json=payload)
            
            # 打印抓包信息
            print("🚨 状态码:", response.status_code)
            print("🚨 原始返回:", response.text)
            
            # 解析数据
            raw_data = response.json()
            # st.write("🚨 抓包到的真实JSON数据:", raw_data)
            
            # 这里的取值逻辑先随便写一个备用，如果拿到了真实数据我们再改
            ans = raw_data.get("output", raw_data.get("text", "抓到数据了，但不知道是哪个字段！"))
            
            st.session_state.messages.append({"role": "assistant", "content": ans})
            st.experimental_rerun()
    except Exception as e:
        st.error(f"连接后端失败: {e}")