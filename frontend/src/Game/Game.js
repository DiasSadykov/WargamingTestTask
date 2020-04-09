import React, { useEffect } from 'react'
import './Game.css'
import StopButton from '../StopButton/StopButton.js'
import Statistics from '../Statistics/Statistics.js'

function Game (props) {
    let [weapon, setWeapon] = React.useState("")
    let [time, setTime] = React.useState(15)

    function weaponsHandler(event){
        let userWeapon = event.target.getAttribute('value')
        setWeapon(userWeapon)
        props.useWeapon(userWeapon)
    }

    useEffect(() => {
        if (!time) {
            if (!weapon) props.timeout()
            return
        }
        setTimeout(()=>{
            setTime(time - 1)
        }, 1000)
      }, [time, setTime, props, weapon])

    return (
        <div className = "gameContainer">
            <div className = "playerControls">
                <div className = "weapons centered">
                <button className = "weapon enemyWeapon" > 
                    <img value = "Rock" src="https://img.icons8.com/ios/100/000000/hand-rock.png" alt=""/> 
                </button>
                <button className = "weapon enemyWeapon" > 
                    <img value = "Scissors" src="https://img.icons8.com/ios/100/000000/hand-scissors.png" alt=""/> 
                </button>
                <button className = "weapon enemyWeapon"> 
                    <img value = "Paper" src="https://img.icons8.com/ios/100/000000/hand.png" alt=""/> 
                </button>
                </div>
                <h2 className = "centered" >{props.opponent} is already choosing the weapon!</h2>
                
            </div>
            
            {time!==0 && <h1 className = "centered timer"> {time} </h1>}
            {time===0 && <h1 className = "centered timer"> Time is up! </h1>}

            <div className = "playerControls">
                {!weapon && <h1 className = "centered">  {props.name}, choose Your Weapon </h1> }
                
                {weapon && <h1 className = "centered" >You choose {weapon}</h1>}
                <div className = "weapons centered">
                <button className = "weapon" onClick = {(event) => weaponsHandler(event)}> 
                    <img value = "Rock" src="https://img.icons8.com/ios/100/000000/hand-rock.png" alt=""/> 
                </button>
                <button className = "weapon" onClick = {(event) => weaponsHandler(event)}> 
                    <img value = "Scissors" src="https://img.icons8.com/ios/100/000000/hand-scissors.png" alt=""/> 
                </button>
                <button className = "weapon" onClick = {(event) => weaponsHandler(event)}> 
                    <img value = "Paper" src="https://img.icons8.com/ios/100/000000/hand.png" alt=""/> 
                </button>
                </div>
                <Statistics></Statistics>
                <StopButton leaveGame = {props.leaveGame}/>
                
            </div>

            
        </div>
    )
  
}

export default Game