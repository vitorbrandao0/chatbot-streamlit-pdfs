css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}
'''

bot_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://cmlo.co/wp-content/uploads/2024/11/cute-business-woman-with-headset-3d-rendering-computer-digital-drawing.jpg.webp">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://img.freepik.com/fotos-premium/representante-de-servico-ao-cliente-avatar-digital-ia-geradora_934475-9075.jpg">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''