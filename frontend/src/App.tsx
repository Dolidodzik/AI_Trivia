import React, { useState, useEffect, ChangeEvent, useRef } from 'react';
import './App.css';

interface Message {
  content: string;
  sentBy: string;
}

interface UserInfo {
  nickname: string;
  userId: string;
}

function generateRandomId(): string {
  const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let randomId = '';
  for (let i = 0; i < 28; i++) {
    const randomIndex = Math.floor(Math.random() * characters.length);
    randomId += characters.charAt(randomIndex);
  }
  return randomId;
}

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState<string>('');
  const [roomName, setRoomName] = useState<string>('test');
  const [ws, setWs] = useState<WebSocket | null>(null);
  const userInfo = useRef<UserInfo | null>(null);

  console.log("Messages: ", messages);
  console.log("USER INFO: ", userInfo);

  useEffect(() => {
    if (ws) {
      ws.onopen = () => {
        console.log('WebSocket connected');
      };

      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log("NEW SOMETHING RECEIVED: ", data);
        if (data.type === 'chat.info') {
          userInfo.current = {
            nickname: data.nickname,
            userId: data.userId,
          }
        } else if (data.type === 'system.message'){
          const system_message = data.data;
          console.log("NEW system.message RECEIVED: ", system_message);
          console.log("curr state: ", userInfo)
          if(system_message.subtype === "new_user_joined"){
            // new user joined the channel
            if(system_message.nickname === userInfo.current?.nickname){ // notification about own join received
              const message: Message = {
                content: "You joined the room!",
                sentBy: "SYSTEM"
              };
              setMessages((prevMessages) => [...prevMessages, message]);
            }else{ // other user
              const message: Message = {
                content: "User "+ system_message.nickname +" joined the room",
                sentBy: "SYSTEM"
              };
              setMessages((prevMessages) => [...prevMessages, message]);
            }
          }
        } else if (data.type === 'chat.message') {
          // ignoring your own messages, receiving messages from websocket only from other users
          if (!(userInfo && data.user_id === userInfo.current?.userId)) {
            const message: Message = {
              content: data.message,
              sentBy: data.nickname, 
            };
            setMessages((prevMessages) => [...prevMessages, message]);
          }
        }
      };

      ws.onclose = () => {
        console.log('WebSocket disconnected');
      };
    }

    return () => {
      // cleanup
    };
  }, [roomName, messages, ws, userInfo]);

  const connect = () => {
    if (ws) {
      ws.close();
    }

    const newWs = new WebSocket(`ws://localhost:8000/ws/chat/${roomName}/`);
    setWs(newWs);
  };

  const sendMessage = () => {
    if (inputMessage.trim() !== '') {
      if (ws) {
        ws.send(JSON.stringify({ message: inputMessage }));
        const message: Message = {
          content: inputMessage,
          sentBy: userInfo.current?.nickname || 'UNKNOWN', // Use nickname or 'UNKNOWN' if not available
        };
        setMessages((prevMessages) => [...prevMessages, message]);
        setInputMessage('');
      }
    }
  };

  const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    setInputMessage(e.target.value);
  };

  const handleRoomChange = (e: ChangeEvent<HTMLInputElement>) => {
    setRoomName(e.target.value);
  };

  return (
    <div className="App">
      {(userInfo && userInfo.current) &&  (
        <div>
          <p>Your nickname: {userInfo.current.nickname}</p>
          <p>Your user ID: {userInfo.current.userId}</p>
        </div>
      )}

      <div>
        {messages.map((msg) => (
          <div
            key={generateRandomId()}
          >
            {msg.sentBy}: {msg.content}
          </div>
        ))}
      </div>
      <label>
        Room:
        <input type="text" value={roomName} onChange={handleRoomChange} />
      </label>
      <input type="text" value={inputMessage} onChange={handleInputChange} />
      <button onClick={sendMessage}>Send</button>
      <button
        style={{ margin: '200px 200px', fontSize: '7px' }}
        onClick={connect}
      >
        Connect
      </button>
    </div>
  );
}

export default App;
