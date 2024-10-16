import { createContext, useState } from "react";
import runChat from "@utils/gemini";

export const ChatbotContext = createContext();

const ChatbotContextProvider = (props) => {
    const [input, setInput] = useState("");
    const [recentPrompt, setRecentPrompt] = useState("");
    const [prevPrompts, setPrevPrompts] = useState([]);
    const [showResult, setShowResult] = useState(false);
    const [loading, setLoading] = useState(false);
    const [resultData, setResultData] = useState("");
    const [fullRes, setfullRes] = useState("");
    const [output, setOutput] = useState("")
    const [historyMessage, setHistoryMessage] = useState([]); // Lưu lịch sử hội thoại

    const storeMessage = (userMessage, botMessage) => {
        const messagePair = {
            user: { sender: 'user', message: userMessage },
            bot: { sender: 'bot', message: botMessage }
        };
        setHistoryMessage(prev => [...prev, messagePair]);
    };

    const delayPara = (index, nextWord) => {
        setTimeout(function (){
            setResultData(prev=>prev+nextWord);
        },75*index)
    }

    const newChat = () => {
        setLoading(false)
        setShowResult(false)
    }

    
    const onSent = async (prompt) => {
        console.log(prevPrompts)
        if(prevPrompts.length>0){
            console.log(prevPrompts[prevPrompts.length -1])
            console.log(output)
            storeMessage(prevPrompts[prevPrompts.length - 1], output);

        }
        setResultData("")
        setLoading(true)
        setShowResult(true)
        let response;
        if (prompt != undefined) {
            response = await runChat(prompt);
            setRecentPrompt(prompt)
        }
        else
        {
            setPrevPrompts(prev=>[...prev, input])
            setRecentPrompt(input)
            response = await runChat(input)
        }

        setInput("")
        let responseArray = response.split("**");
        let newResponse = "" ;
        for(let i = 0; i < responseArray.length; i++)
        {
            if(i === 0 || i%2 !== 1) {
                newResponse += responseArray[i];
            }
            else {
                newResponse += "<b>"+responseArray[i]+"</b>";
            }
        }
        let newResponse2 = newResponse.split("*").join("</br>")
        let newResponseArray = newResponse2.split(" ");
        for(let i = 0; i < newResponseArray.length; i++)
        {
            const nextWord = newResponseArray[i];
            delayPara(i,nextWord+" ") 
        }
        setLoading(false)
        // console.log(prompt)
        // console.log(input)
        setOutput(newResponse2)
    }
    
    
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
    }

    return (
        <ChatbotContext.Provider value={contextValue}>
            {props.children}
        </ChatbotContext.Provider>
    )
}

export default ChatbotContextProvider;
