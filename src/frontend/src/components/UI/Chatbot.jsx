import { useContext, useRef } from 'react';
import '@styles/chatbot.css';
import { useTheme } from "@mui/material";
import { assets } from '@assets/chatbot/assets';
import { ChatbotContext } from '@context/ChatbotContext';
import { tokens } from "@theme";

const Chatbot = () => {
    const theme = useTheme();
    const { onSent, recentPrompt,historyMessage, fullRes, showResult, loading, resultData, setInput, input } = useContext(ChatbotContext);
    const msgEnd = useRef(null);

    const handleEnter = async (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            await onSent();
        }
    };

    return (
        <div className='main'>
            {/* <div className='nav'>
                <p>Gemini</p>
                <img src={assets.user_icon} alt="User" />
            </div> */}
            <div className="main-container">
                {!showResult ? (
                    <>
                        <div className="greet">
                            <p><span>Hello, Dev.</span></p>
                            <p>How can I help you today..?</p>
                        </div>
                        <div className="cards">
                            <div className="card">
                                <p>Suggest beautiful places to see on an upcoming road trip</p>
                                <img src={assets.compass_icon} alt="" />
                            </div>
                            <div className="card">
                                <p>Briefly summarize this concept: urban planning</p>
                                <img src={assets.bulb_icon} alt="" />
                            </div>
                            <div className="card">
                                <p>Brainstorm team bonding activities for our work retreat</p>
                                <img src={assets.message_icon} alt="" />
                            </div>
                            <div className="card">
                                <p>Improve the readability of the following code</p>
                                <img src={assets.code_icon} alt="" />
                            </div>
                        </div>
                    </>
                ) : (
                      <div className='result'>
                        {/* Kiểm tra nếu historyMessage không rỗng mới hiển thị lịch sử */}
                        {historyMessage.length > 0 && (
                          <div>
                              {historyMessage.map((pair, index) => (
                                  <div key={index}>
                                      <div className="result-title">
                                          <img src={assets.user_icon} alt="User" />
                                          <p dangerouslySetInnerHTML={{ __html: pair.user.message }}></p>
                                      </div>
                                      <div className="result-data">
                                        <img src={assets.gemini_icon} alt="Bot" />
                                        <p dangerouslySetInnerHTML={{ __html: pair.bot.message }}></p>
                                    </div>
                                    </div>
                                  ))}
                            </div>
                        )}
                        <div className="result-title">
                          <img src={assets.user_icon} alt="" />
                          <p>{recentPrompt}</p>
                        </div>
                        <div className="result-data">
                          <img src={assets.gemini_icon} alt="" />
                          {loading
                          ?<div className='loader'>
                            <hr />
                            <hr />
                            <hr />
                          </div>
                          :<p dangerouslySetInnerHTML={{__html:resultData}}></p>
                          }
                  
                        </div>
                        <div ref={msgEnd}></div>
                      </div>
                )}

              <div className="main-bottom">
                <div className="search-box" style={theme.palette.mode==='dark'?{ backgroundColor: '#707a82', color: ''} : { backgroundColor: '', color: 'black'}}>
                    <input onChange={(e) =>setInput(e.target.value)}  onKeyDown={handleEnter} value={input} type="text"  placeholder='Enter a prompt here ' />
                    <div>
                        <img src={assets.gallery_icon} alt="" />
                        <img src={assets.mic_icon} alt="" />
                        {input?<img onClick={() =>onSent()} src={assets.send_icon} alt="" /> : null}
                    </div>
                </div>
                <p className="bottom-info">
                    Gemiini may display inaccurate info, including about people, so double-click its responses. Your privacy and Gemini Apps
                </p>
              </div>
            </div>

      </div>
    // </div>
    );
};

export default Chatbot;
