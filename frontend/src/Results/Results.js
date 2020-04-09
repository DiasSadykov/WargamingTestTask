import React from 'react'
import './Results.css'
import StopButton from '../StopButton/StopButton.js'
import Statistics from '../Statistics/Statistics.js'
function Results (props) {


    return (
        <div className = "resultsContainer">
            <div className = "playerControls">
                
                <h2 className = "centered" >{props.opponentWeapon}</h2>
                
            </div>
            
            <div className = "resultsWrapper centered">
                {props.winner===null && <h1 className = "centered result"> It is Draw! </h1>}
                {props.winner===props.name && <h1 className = "centered result"> You Won! </h1>}
                {props.winner!==props.name && props.winner!==null && <h1 className = "centered result"> You Lose:( </h1>}
                <button onClick = {() => props.getReady()}> I want to play again with same opponent! </button>
            </div>
            



            <div className = "playerControls">
                <h2 className = "centered" >{props.myWeapon}</h2>
                <Statistics win = {props.winner===props.name} game = {true}></Statistics>
                <StopButton leaveGame = {props.leaveGame}/>
            </div>

            
        </div>
    )
  
}

export default Results