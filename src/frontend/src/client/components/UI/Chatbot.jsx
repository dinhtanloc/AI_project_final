import { useContext, useRef, useState, useEffect } from 'react';
import '@client/styles/chatbot.css';
import { useTheme } from "@mui/material";
import { assets } from '@assets/chatbot/assets';
import { ChatbotContext } from '@context/ChatbotContext';
import useAxios from '@utils/useAxios';

const Chatbot = () => {
    const theme = useTheme();
    const { onSent, recentPrompt, historyMessage, fullRes, showResult, loading, resultData, setInput, input } = useContext(ChatbotContext);
    const msgEnd = useRef(null);
    const fileInputRef = useRef(null);
    const [selectedFile, setSelectedFile] = useState(null);
    const [message, setMessage] = useState('');
    const [fileUrl, setFileUrl] = useState('');
    const [img,setImage]=useState('');
    const chatbot = useAxios();

    useEffect(() => {
        const fetchProfile = async () => {
            try {
              const res = await chatbot.get("accounts/user/profile/");
              const profile = res.data;
              var imgUrl = profile.image
              setImage(imgUrl)
              console.log(res)
              // setName(profile)
            } catch (error) {
              console.error('Có lỗi xảy ra khi truy cập dữ liệu:', error);
      
            }
          };
          fetchProfile();
      
        
    }, []);




    const onFileChange = (e) => {
        setSelectedFile(e.target.files[0]);
    };

    const onFileUpload = async () => {
        if (selectedFile) {
            const formData = new FormData();
            formData.append('pdf_file', selectedFile);
            console.log('Uploading file...');

            try {
                const res = await chatbot.post('/chatbot/upload/pdf/', formData);
                // setMessage('File uploaded successfully!');
                setFileUrl(res.data.file_url);
            } catch (error) {
                // setMessage('Failed to upload file');
                console.error(error);
            }
        } else {
            // setMessage('Please select a file first.');
        }
    };

    const handleEnter = async (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            await onSent(); 
            if (selectedFile) {
                await onFileUpload();
        }
    };
    
    }
    return (
        <div className='main'>
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
                    <div className='result' style={{color:'black'}}>
                        {historyMessage.length > 0 && (
                            <div>
                                {historyMessage.map((pair, index) => (
                                    <div key={index}>
                                        <div className="result-title">
                                            <img src={img} alt="User" />
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
                            <img src={img} alt="" />
                            <p>{recentPrompt}</p>
                        </div>
                        <div className="result-data">
                            <img src={assets.gemini_icon} alt="" />
                            {loading ? (
                                <div className='loader'>
                                    <hr />
                                    <hr />
                                    <hr />
                                </div>
                            ) : (
                                <p dangerouslySetInnerHTML={{ __html: resultData }}></p>
                            )}
                        </div>
                        <div ref={msgEnd}></div>
                    </div>
                )}
                <div className="main-bottom">
                    <div className="search-box" style={theme.palette.mode === 'dark' ? { backgroundColor: '#707a82', color: '' } : { backgroundColor: '', color: 'black' }}>
                        <input
                            onChange={(e) => setInput(e.target.value)}
                            onKeyDown={handleEnter}
                            value={input}
                            type="text"
                            placeholder='Enter a prompt here '
                        />
                        <input
                            type="file"
                            accept="application/pdf"
                            onChange={onFileChange}
                            style={{ display: 'none' }}
                            ref={fileInputRef} 
                        />
                        <div>
                            <img src={assets.gallery_icon} onClick={() => fileInputRef.current.click()} alt="" />
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
    );
};

export default Chatbot;
