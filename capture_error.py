from chatbot_agent import MentalHealthChatbot
bot = MentalHealthChatbot()
response = bot.get_response('I am feeling anxious')
with open('response.log', 'w') as f:
    f.write(response)
