import React from 'react'
import './Login.css'
import Error from '../Error/Error.js'
function Login(props) {
    let [name,setName] = React.useState('')



    return (
        <div className = "LoginContainer">
            <h1>Welcome to Rock Scissors Paper</h1> 
            <p className = "centered" > Enter your name and play!</p>
            <input placeholder = "Username" onChange = {event => setName(event.target.value)}></input>
            <button className = "loginButton" onClick = {() => props.login(name)}> Play </button>
            <Error error = {props.error}></Error>
        </div>
    )
  
}

export default Login