import React, { useState, useContext } from 'react';
import "@client/styles/login.css";
import AuthContext from '@context/AuthContext'
import  AuthLoginContext  from '@context/AuthLoginContext';
import { useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faFacebookF, faGoogle, faGithub } from '@fortawesome/free-brands-svg-icons';

// axios.defaults.xsrfCookieName = 'csrftoken';
// axios.defaults.xsrfHeaderName = 'X-CSRFToken';
// axios.defaults.withCredentials = true;


const Login = () => {
  const {loginUser} = useContext(AuthContext);
  const { registerUser } = useContext(AuthContext);
  const { showLogin } = useContext(AuthLoginContext);
  const [isSignUpActive, setIsSignUpActive] = useState(!showLogin);


  const [currentUser, setCurrentUser] = useState();
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

    useEffect(() => {
        setTimeout(() => {
          setIsSignUpActive(showLogin);
        }, 100); 
    }, []);
  

  const handleSignUpClick = () => {
    setIsSignUpActive(true);
  };

  const handleSignInClick = () => {
    setIsSignUpActive(false);
  };

 
  function submitRegistration(e) {
    e.preventDefault()
    registerUser(email, username, password)
    setIsSignUpActive(false);

  }

  function submitLogin(e) {
    e.preventDefault();
    if (email.length > 0) {
        loginUser(email, password); 
        setCurrentUser(true);
    } 
}

  const containerClassName = isSignUpActive ? 'container_title right-panel-active' : 'container_title';
  return (
    <>
      <div className={containerClassName}>
        <div className="form-container sign-up-container">
          <form className='form_title' onSubmit={e => submitRegistration(e)}>
            <h1 className="h1_title">Create Account</h1>
            <div className="social-container">
            <a href="#" className="social">
                <FontAwesomeIcon icon={faFacebookF} />
            </a>
            <a href="#" className="social">
              <FontAwesomeIcon icon={faGoogle} />
            </a>
            <a href="#" className="social">
              <FontAwesomeIcon icon={faGithub} />
            </a>
            </div>
            <span className="span_title">or use your email for registration</span>
            <input className='input_title' type="text" placeholder="Name" value={username} onChange={e => setUsername(e.target.value)} />
            <input className='input_title' type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} />
            <input className='input_title' type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
            <button className='Angel' onClick={handleSignUpClick}>Sign Up</button>
          </form>
        </div>

        <div className="form-container sign-in-container">
          <form className='form_title' action="#" onSubmit={e => submitLogin(e)}>
            <h1 className="h1_title">Sign in</h1>
            <div className="social-container">
              <a href="#" className="social">
                <FontAwesomeIcon icon={faFacebookF} />
              </a>
              <a href="#" className="social">
                <FontAwesomeIcon icon={faGoogle} />
              </a>
              <a href="#" className="social">
                <FontAwesomeIcon icon={faGithub} />
              </a>
            </div>
            <span className="span_title">or use your account</span>
            <input className='input_title'  type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
            <input className='input_title' type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
            <a className="a_title" href="#">Forgot your password?</a>
            <button className='Angel' onClick={handleSignInClick}>Sign In</button>
          </form>
        </div>
        <div className="overlay-container">
          <div className="overlay">
            <div className="overlay-panel overlay-left">
              <h1 className="h1_title">Welcome Back!</h1>
              <p className='p_title'>To inform newest products please login to join with us</p>
              <button className="ghost" id="signIn" onClick={handleSignInClick}>Sign In</button>
            </div>
            <div className="overlay-panel overlay-right">
              <h1 className="h1_title">Welcom to Vietnamese Stock Advisor!</h1>
              <p className='p_title'>Enter your personal details and start journey with us</p>
              <button className="ghost" id="signUp" onClick={handleSignUpClick}>Sign Up</button>
            </div>
          </div>
        </div>
      </div>

      <footer className='footer_title'>
        <p className='p_title'>
          Created with <i className="fa fa-heart"></i> by
          <a className="a_title" target="_blank" href="https://www.facebook.com/profile.php?id=100010680972124"> Loc Dinh </a>
          - Read how I created this and give me ten points in Web programming subject
        </p>
      </footer>
    </>
  );
};

export default Login;
