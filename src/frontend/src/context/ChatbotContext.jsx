import { createContext, useState } from "react";
import useAxios from "@utils/useAxios"; 

export const ChatbotContext = createContext();

const ChatbotContextProvider = (props) => {
    const axiosInstance = useAxios(); 
    const [input, setInput] = useState("");
    const [recentPrompt, setRecentPrompt] = useState("");
    const [prevPrompts, setPrevPrompts] = useState([]);
    const [showResult, setShowResult] = useState(false);
    const [loading, setLoading] = useState(false);
    const [resultData, setResultData] = useState("");
    const [fullRes, setfullRes] = useState("");
    const [output, setOutput] = useState("");
    const [historyMessage, setHistoryMessage] = useState([]); 

    const storeMessage = (userMessage, botMessage) => {
        const messagePair = {
            user: { sender: 'user', message: userMessage },
            bot: { sender: 'bot', message: botMessage }
        };
        setHistoryMessage(prev => [...prev, messagePair]);
    };

    const delayPara = (index, nextWord) => {
        setTimeout(function () {
            setResultData(prev => prev + nextWord);
        }, 75 * index);
    };

    const newChat = () => {
        setLoading(false);
        setShowResult(false);
    };

    const getChatbotAnswer = async (prompt) => {
        try {
            const response = await axiosInstance.post("/chatbot/chatbot/interact/", {'message': prompt });

            return response.data.response; 
        } catch (error) {
            console.error("Lỗi khi lấy câu trả lời từ backend:", error);
            return "Xin lỗi, đã xảy ra lỗi. Vui lòng thử lại.";
        }
    };

    const onSent = async (prompt) => {
        if (prevPrompts.length > 0) {
            storeMessage(prevPrompts[prevPrompts.length - 1], output);
        }

        setResultData("");
        setLoading(true);
        setShowResult(true);
        let response;
        if (prompt !== undefined) {
            response = await getChatbotAnswer(prompt); 
            setRecentPrompt(prompt);
        } else {
            setPrevPrompts(prev => [...prev, input]);
            setRecentPrompt(input);
            response = await getChatbotAnswer(input);
        }

        setInput("");
        let responseArray = response.split("**");
        let newResponse = "";
        for (let i = 0; i < responseArray.length; i++) {
            if (i === 0 || i % 2 !== 1) {
                newResponse += responseArray[i];
            } else {
                newResponse += "<b>" + responseArray[i] + "</b>";
            }
        }
        let newResponse2 = newResponse.split("*").join("</br>");
        let newResponseArray = newResponse2.split(" ");
        for (let i = 0; i < newResponseArray.length; i++) {
            const nextWord = newResponseArray[i];
            delayPara(i, nextWord + " ");
        }
        setLoading(false);
        setOutput(newResponse2);
    };

    const contextValue = {
        prevPrompts,
        fullRes,
        setPrevPrompts,
        onSent,
        setRecentPrompt,
        recentPrompt,
        showResult,
        loading,
        resultData,
        input,
        setInput,
        newChat,
        historyMessage
    };

    return (
        <ChatbotContext.Provider value={contextValue}>
            {props.children}
        </ChatbotContext.Provider>
    );
};

export default ChatbotContextProvider;
