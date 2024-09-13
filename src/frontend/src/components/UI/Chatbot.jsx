import { useContext, useRef } from 'react';
import '@styles/chatbot.css';
import { assets } from '@assets/chatbot/assets';
import { Context } from '@context/ChatbotContext';

const Chatbot = () => {
    const { onSent, recentPrompt, showResult, loading, input, setInput, messages, resultData } = useContext(Context);
    const msgEnd = useRef(null);

    const handleEnter = async (e) => {
        if (e.key === 'Enter') {
            e.preventDefault(); // Prevent form submission or unexpected behavior
            await onSent();
        }
    };

    return (
        <div className='main'>
            <div className='nav'>
                <p>Gemini</p>
                <img src={assets.user_icon} alt="" />
            </div>
            <div className="main-container">
                {!showResult
                    ? <>
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
                    : <div className='result'>
                        {messages.map((message, i) => (
                            <div key={i} className="result-title">
                                {!message.isBot ? (
                                    <div className="user-message">
                                        <img src={assets.user_icon} alt="User Icon" />
                                        <p>{message.text}</p>
                                    </div>
                                ) : (
                                    <div className="result-data">
                                        <img src={assets.gemini_icon} alt="Bot Icon" />
                                        {message.isTyping ? (
                                            loading ? (
                                                <div className="loader">
                                                    <hr />
                                                    <hr />
                                                    <hr />
                                                </div>
                                            ) : (
                                                <p>{resultData}</p>
                                            )
                                        ) : (
                                            <p>{message.text}</p>
                                        )}
                                    </div>
                                )}
                            </div>
                        ))}
                        <div ref={msgEnd}></div>
                    </div>
                }
                <div className="main-bottom">
                    <div className="search-box">
                        <input
                            onChange={(e) => setInput(e.target.value)}
                            value={input}
                            onKeyDown={handleEnter}
                            type="text"
                            placeholder='Enter a prompt here'
                        />
                        <div>
                            <img src={assets.gallery_icon} alt="" />
                            <img src={assets.mic_icon} alt="" />
                            {input ? <img onClick={() => onSent()} src={assets.send_icon} alt="" /> : null}
                        </div>
                    </div>
                    <p className="bottom-info">
                        Gemiini may display inaccurate info, including about people, so double-click its responses. Your privacy and Gemini Apps
                    </p>
                </div>
            </div>
        </div>
    )
}

export default Chatbot;
