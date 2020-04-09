import React from 'react'
import './ReadyScreen.css'

function ReadyScreen(props){
    return (
        <div className = "readyContainer">
        <h1> Your opponent is {props.opponent} </h1>
        <button onClick = {() =>props.getReady()}> I am Ready </button>
    </div>
    )
}

export default ReadyScreen