import AtomicSpinner from 'atomic-spinner'
import "@admin/styles/loading-page.css"
import { tokens } from "@theme";
import { Box, Button, useTheme } from "@mui/material";
const LoadingPage = () =>{
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const darkColors = [colors.grey[800], colors.grey[700], colors.grey[600]]; 
    const lightColors = [colors.grey[200], colors.grey[300], colors.grey[400]];


    const backgroundColors = theme.palette.mode === 'dark' ? darkColors : lightColors;
    const animationStyle = {
        animation: `changeColor 5s infinite alternate`,
        backgroundColor: backgroundColors[0], 
    };
    return(
        <div className='loading_container_admin' style={animationStyle}>
            <AtomicSpinner/>

        </div>

    );
}

export default LoadingPage