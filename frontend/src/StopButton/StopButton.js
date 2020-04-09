import React from 'react'
import './StopButton.css'
function stopButton(props){
    return  (<div className = "stopButtonWrapper">
        <button className = "stopButton" onClick = {() => props.leaveGame()}>
            Leave Game
        </button>
    </div>)
}

export default stopButton