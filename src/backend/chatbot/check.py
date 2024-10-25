from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def chatbot_respond(request):
    data = json.loads(request.body)
    message = data['message']
    user_id = request.user.id

    # Kiểm tra nếu `thread_id` được gửi từ client, nếu không thì tạo mới
    thread_id = data.get('thread_id') or str(uuid.uuid4())
    
    # Khởi tạo chatbot với user_id và thread_id hiện có
    bot = ChatBot(user_id=user_id, thread_id=thread_id)
    _, updated_chatbot = bot.respond([], message)

    return JsonResponse({
        'response': updated_chatbot[-1][1],
        'thread_id': thread_id  # Gửi lại thread_id để client có thể lưu lại
    })




# // Function to send a message to the chatbot API
# async function sendMessage(message) {
#     let thread_id = sessionStorage.getItem('thread_id');

#     const response = await fetch('/api/chatbot/respond', {
#         method: 'POST',
#         headers: {
#             'Content-Type': 'application/json'
#         },
#         body: JSON.stringify({ message, thread_id })
#     });

#     const data = await response.json();
    
#     // Save thread_id in session if it's new
#     if (data.thread_id) {
#         sessionStorage.setItem('thread_id', data.thread_id);
#     }

#     // Process the chatbot response...
# }
