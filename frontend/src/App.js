import React, { useEffect } from 'react';
import Login from './Login/Login.js'
import Matching from './Matching/Matching.js'
import Game from './Game/Game.js'
import ReadyScreen from './ReadyScreen/ReadyScreen.js'
import Results from './Results/Results.js'

import './App.css';

var websocket = new WebSocket("ws://localhost:8080/ws");



function App() {

  let [state, setState] = React.useState("NOT_LOGGED_IN")
  let [name, setName] = React.useState("")
  let [opponent, setOpponent] = React.useState("")
  let [results, setResults] = React.useState({})
  let [error, setError] = React.useState("")


  const setupBeforeUnloadListener = () => {
    window.addEventListener("beforeunload", (ev) => {
        disconnect();
      });
  };

  useEffect(() => {
    setupBeforeUnloadListener();
    websocket.onmessage = function(str) {
      console.log(str.data)
      let message = JSON.parse(str.data)

      if (message['status'] === 'you were connected') {
        setState("WAITING_FOR_GAME")
      }

      else if (message['status'] === 'game is found') {
        setOpponent(message['opponent'])
        setState("GAME_FOUND")
      }
      else if (message['status'] === 'game is started') {
        setState("GAME_STARTED")
      }
      else if (message['status'] === 'results') {
        setResults(message)
        setState("RESULTS")
      }

      if (message['status'] === 'game is ended') {
        setState("WAITING_FOR_GAME")
      }
      if (message['status'] === 'error') {
        setError(message['body'])
      }

      
    };

  }, [])

  function login(username) {
    setName(username)
    websocket.send(JSON.stringify({
      message: 'connect',
      name: username
    }));
  }

  function getReady() {
    websocket.send(JSON.stringify({
      message: 'action',
      body: 'Ready'
    }));
  }

  function useWeapon(weapon) {
    console.log(weapon)
    websocket.send(JSON.stringify({
      message: 'action',
      body: weapon
    }));
  }

  function timeout(weapon) {
    console.log(weapon)
    websocket.send(JSON.stringify({
      message: 'action',
      body: 'Timeout'
    }));
  }

  function leaveGame(weapon) {
    console.log(weapon)
    websocket.send(JSON.stringify({
      message: 'action',
      body: 'Stop'
    }));
  }

  function disconnect() {
    websocket.send(JSON.stringify({
      message: 'disconnect'
    }));
  }

  return (
    <div className = "wrapper">
      {state === "NOT_LOGGED_IN" && <Login error = {error}login={login}></Login>}
      {state === "WAITING_FOR_GAME" && <Matching></Matching>}
      {state === "GAME_FOUND"  && <ReadyScreen opponent = {opponent} leaveGame = {leaveGame} getReady = {getReady}></ReadyScreen>}
      {state === "GAME_STARTED"  && <Game name = {name }opponent = {opponent} leaveGame = {leaveGame} timeout = {timeout} useWeapon = {useWeapon}></Game>}
      {state === "RESULTS"  && <Results name = {name } 
                                        opponent = {opponent} 
                                        winner = {results['winner']} 
                                        myWeapon = {results[name]} 
                                        opponentWeapon = {results[opponent]} 
                                        leaveGame = {leaveGame}
                                        getReady = {getReady}>
                               </Results>}
    </div>
  );
  }


export default App;
