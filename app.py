# app.py

from flask import Flask, request, Response, jsonify
from flask_cors import CORS
from rag_chain import get_rag_chain
import json

# 初始化 Flask 应用
app = Flask(__name__)
# 设置 CORS，允许所有来源的跨域请求
CORS(app)

# 在服务启动时，立即加载并初始化 RAG 链
# 这可以避免第一次 API 请求时漫长的加载等待
print("正在初始化 RAG 问答链，请稍候...")
try:
    rag_chain = get_rag_chain()
    print("\n✅ 服务已就绪，可以接收请求。")
except Exception as e:
    print(f"❌ 初始化 RAG 链失败: {e}")
    rag_chain = None

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    处理聊天请求的 API 端点。
    接收一个包含 "question" 字段的 JSON 请求体。
    以 Server-Sent Events (SSE) 的形式流式返回响应。
    """
    if rag_chain is None:
        return jsonify({"error": "RAG chain 未初始化，请检查服务器日志。"}), 500

    data = request.get_json()
    if not data or 'question' not in data:
        return jsonify({"error": "请求体中缺少 'question' 字段"}), 400

    question = data['question']
    print(f"收到流式请求问题: {question}")

    def generate():
        """
        生成器函数，用于流式地从 RAG 链获取数据并发送。
        """
        try:
            # 使用 .stream() 方法来获取流式响应
            stream = rag_chain.stream({"input": question})
            
            # 迭代处理流中的每一个数据块
            for chunk in stream:
                # 'answer' 数据块包含了AI生成的回答片段
                if "answer" in chunk:
                    answer_piece = chunk["answer"]
                    # 将回答片段封装成 SSE 格式发送给前端
                    # event: answer_chunk (自定义事件名)
                    # data: {"content": "片段内容"}
                    yield f'event: answer_chunk\ndata: {json.dumps({"content": answer_piece})}\n\n'

                # 'context' 数据块包含了答案所参考的来源文档
                if "context" in chunk and chunk["context"] is not None:
                    sources = []
                    for doc in chunk["context"]:
                        source_url = doc.metadata.get('source', '未知来源')
                        source_title = doc.metadata.get('title', '无标题')
                        sources.append({
                            "title": source_title,
                            "url": source_url
                        })
                    
                    # 将来源信息封装成 SSE 格式发送给前端
                    # event: sources
                    # data: [{"title": "标题", "url": "链接"}, ...]
                    yield f'event: sources\ndata: {json.dumps(sources)}\n\n'

            # 所有数据块发送完毕后，发送一个结束信号
            yield 'event: end\ndata: [DONE]\n\n'

        except Exception as e:
            print(f"处理流时发生错误: {e}")
            # 如果在流处理过程中发生错误，发送一个错误事件
            error_message = f"服务器在处理请求时发生错误: {str(e)}"
            yield f'event: error\ndata: {json.dumps({"error": error_message})}\n\n'

    # 返回一个 Response 对象，mimetype 设置为 'text/event-stream' 以支持 SSE
    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    # 启动 Flask 开发服务器，监听在 5001 端口
    app.run(host='0.0.0.0', port=5001, debug=True)

