import ds_protocol as dsp

# Sending of direct message was successful
dir = '{"response": {"type": "ok", "message": "Direct message sent"}}'

# Response to request for **`all`** and **`new`** messages. Timestamp is time in seconds 
# of when the message was originally sent.
mess = '{"response": {"type": "ok", "messages": [{"message":"Hello User 1!", "from":"markb", "timestamp":"1603167689.3928561"},{"message":"Bzzzzz", "from":"thebeemoviescript", "timestamp":"1603167689.3928561"}]}}'

# Send a directmessage to another DS user
direct_message = '{"token": "user_token", "directmessage": {"entry": "Hello World!", "recipient": "ohhimark", "timestamp": "1603167689.3928561"}}'

# Request unread message from the DS server
unread = '{"token": "user_token", "directmessage": "new"}'

# Request all messages from the DS server
all = '{"token": "user_token", "directmessage": "all"}'

def test_extract_json():
    json = dsp.extract_json(dir)
    if json == {"response": {"type": "ok", "message": "Direct message sent"}}:
        print('TEST 1 PASSED')
    else:
        print('TEST 1 FAILED')

def test_extract_messages():
    messages = dsp.extract_messages(dsp.extract_json(mess))
    if messages == [{"message":"Hello User 1!", "from":"markb", "timestamp":"1603167689.3928561"},{"message":"Bzzzzz", "from":"thebeemoviescript", "timestamp":"1603167689.3928561"}]:
        print('TEST 2 PASSED')
    else:
        print('TEST 2 FAILED')

def test_gen_direct():
    message = dsp.gen_direct_message('user_token', 'Hello World!', 'ohhimark')
    if message[:message.find('"timestamp')] == direct_message[:direct_message.find('"timestamp')]:
        print('TEST 3 PASSED')
    else:
        print(message)
        print(direct_message)
        print('TEST 3 FAILED')
    
def test_gen_unread():
    message = dsp.gen_get_unread_message('user_token')
    if message == unread:
        print('TEST 4 PASSED')
    else:
        print(message)
        print(unread)
        print('TEST 4 FAILED')

def test_gen_all():
    message = dsp.gen_all_messages('user_token')
    if message == all:
        print('TEST 5 PASSED')
    else:
        print(message)
        print(all)
        print('TEST 5 FAILED')


test_extract_json()
test_extract_messages()
test_gen_direct()
test_gen_unread()
test_gen_all()