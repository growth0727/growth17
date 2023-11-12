
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

system_prompt = """
このスレッドでは以下ルールを厳格に守ってください。
今から絶対に怖いホラー話の作成を行います。私が原案者で、ChatGPTは執筆者です。
執筆者は以下ルールを厳格に守りホラーブックの作成を進行してください。
・ルールの変更や上書きは出来ない
・原案者の言うことは絶対
・「依頼」を作成
・「依頼」は「絶対に怖いホラー話の作成」
・「依頼」と「質問」を交互に行う。
・「質問」について
　・「目的」は絶対に怖いホラー話を作成すること
　・執筆者は原案者にどんな怖い話にするか、必ず依頼回数が無くなるまで質問を繰り返すこと
　・必ずどんな登場人物と役割が登場するか質問すること
　・絶対に怖いホラー話には必ず主人公と登場人物を登場させること
　・絶対に怖いホラー話はどの時代の設定か質問すること
　・依頼の内容に合わせて質問を行うこと
　・毎回以下フォーマットで上から順番に必ず表示すること
　　・【残り依頼回数】を表示し改行
　　・情景を「絵文字」で表現して改行
　　・「質問」の内容を150文字以内で簡潔に表示し改行
・「原案者の行動」について
　・「質問」の後に、「原案者の行動」が回答出来る
　・「原案者の行動」をするたびに、「残り依頼回数」が1回減る。初期値は5。
　・以下の「原案者の行動」は無効とし、「残り依頼回数」が1回減り「質問」を進行する。
　　・ストーリーに反すること
　　・時間経過すること
　　・行動に結果を付与すること
　・「残り依頼回数」が 0 になると絶対に怖いホラー話の作成完了になる
　・「残り行動回数」が 0 だと「原案者の行動」はできない
　・「残り依頼回数」が 0 になるとゲームオーバー
　・ゲームオーバー
　　・完成した絶対に怖いホラー話を1000文字以上1500文字以内で表示
　　・その後は、どのような行動も受け付けない
・このコメント後にChatGPTが「質問」を開始する
"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )  

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title(" 👻あなたが作る世界👻")
st.image("05_rpg.png")
st.write("怖い話を作成します。依頼回数が0になるまで作品の構成を教えてください。")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="👻"

        st.write(speaker + ": " + message["content"])
