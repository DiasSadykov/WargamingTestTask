import React from 'react'
import './Statistics.css'
import {useEffect} from 'react'

function Statistics(props){
    const useStateWithLocalStorage = localStorageKey => {
        const [value, setValue] = React.useState(
            parseInt(localStorage.getItem(localStorageKey)) || 0
        );
        useEffect(() => {
          localStorage.setItem(localStorageKey, value);
        }, [value, localStorageKey]);
        return [value, setValue];
      };

    let [total, setTotal] = useStateWithLocalStorage('total')
    let [win, setWin] = useStateWithLocalStorage('wins')

    useEffect(()=>{
        if (props.win) setWin(win + 1)
        if (props.game) setTotal(total + 1)
    },[])

    return (
        <div className = "centered">
            <h1>Wins/Total = {win}/{total}</h1>
        </div>
    )
    
}


export default Statistics