import { useState, useContext, useRef, useEffect } from 'react';
import '@admin/styles/chatbotadmin.css';
import { useTheme } from "@mui/material";
import { assets } from '@assets/chatbot/assets';
import { ChatbotContext } from '@context/ChatbotContext';
import useAxios from "@utils/useAxios";
import LoadingPage from './LoadingPage';

const ChatbotAdmin = () => {
    const theme = useTheme();
    const { onSent, recentPrompt, historyMessage, fullRes, showResult, loading, resultData, setInput, input } = useContext(ChatbotContext);
    const msgEnd = useRef(null);
    const api = useAxios();
    const [isUploading, setIsUploading] = useState(false);
    const [img,setImage]=useState('');


    const [files, setFiles] = useState([]);
    const [responseMessage, setResponseMessage] = useState("");
    const fileInputRef = useRef(null);

    useEffect(() => {
        const fetchProfile = async () => {
            try {
              const res = await api.get("accounts/user/profile/");
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

    const handleEnter = async (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            await onSent();
        }
    };

    const handleDirectoryChange = (e) => {
        const selectedFiles = Array.from(e.target.files);
        if (selectedFiles.length === 0) {
            alert("Vui lòng chọn ít nhất một file để tải lên.");
            return;
        }
        setFiles(selectedFiles); 
        handleUpload(selectedFiles); 
    };

    const handleUpload = async (selectedFiles) => {
        if (!selectedFiles || selectedFiles.length === 0) {
            alert("Vui lòng chọn ít nhất một file để tải lên.");
            return;
        }

        const formData = new FormData();
        selectedFiles.forEach(file => {
            formData.append("file", file);
        });
        setIsUploading(true);

        try {
            const response = await api.post("/chatbot/upload/file/", formData, {
                headers: {
                    "Content-Type": "multipart/form-data",
                },
            });

            setResponseMessage(response.data.message);
        } catch (error) {
            setResponseMessage("Đã xảy ra lỗi trong quá trình tải lên");
            console.error("Error uploading files:", error);
        } finally {
            setIsUploading(false);  
        }
    };

    const handleCardClick = async() => {
        fileInputRef.current.click();
    };

    if(isUploading){
        return <LoadingPage/>
    }

    return (
        <div className='admin'>
            <div className="admin-container">
                <input 
                    id='file'
                    type="file" 
                    // webkitdirectory="false"
                    ref={fileInputRef} 
                    onChange={handleDirectoryChange} 
                    style={{ display: 'none' }} 
                />
                {!showResult ? (
                    <>
                        <div className="greet">
                            <p><span>Hello, Admin.</span></p>
                            <p>What will we be training, today?</p>
                        </div>
                        <div className="cards">
                            <div className="card" onClick={handleCardClick}>
                                <p>Financial knowledge by using documents from pdf, text and improve my accuracy</p>
                                <img src={assets.compass_icon} alt="" />
                            </div>
                            <div className="card">
                                <p>Algorithm for using function calls to solve financial problems accurately.</p>
                                <img src={assets.bulb_icon} alt="" />
                            </div>
                            <div className="card" onClick={handleCardClick}>
                                <p>Extract information based on tabular data from CSV and XLSX files.</p>
                                <img src={assets.message_icon} alt="" />
                            </div>
                            <div className="card" onClick={handleCardClick}>
                                <p>Train how to use image</p>
                                <img src={assets.code_icon} alt="" />
                            </div>
                        </div>
                    </>
                ) : (
                    <div className='result'>
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
                            {loading
                            ? <div className='loader'>
                                <hr />
                                <hr />
                                <hr />
                              </div>
                            : <p dangerouslySetInnerHTML={{ __html: resultData }}></p>}
                        </div>
                        <div ref={msgEnd}></div>
                    </div>
                )}

                <div className="admin-bottom">
                    <div className="search-box" style={theme.palette.mode === 'dark' ? { backgroundColor: '#707a82', color: '' } : { backgroundColor: '', color: 'black' }}>
                        <input onChange={(e) => setInput(e.target.value)} onKeyDown={handleEnter} value={input} type="text" placeholder='Enter a prompt here ' />
                        <div>
                            <img src={assets.gallery_icon} alt="" />
                            <img src={assets.mic_icon} alt="" />
                            {input ? <img onClick={() => onSent()} src={assets.send_icon} alt="" /> : null}
                        </div>
                    </div>
                    <p className="bottom-info">
                        Moketobot may display inaccurate info, including about people, so double-click its responses. Your privacy and Gemini Apps
                    </p>
                </div>
            </div>
        </div>
    );
};

export default ChatbotAdmin;
