import React, { useState } from 'react'
import image from '../assets/image.png'

const GeneSearch = () => {
 const [change, setfirst] = useState('')
 const [data, setdata] = useState(null)
 console.log(data)

 const input = (e) => {
    setfirst(e.target.value)
 }

 const btn = (e) => {
    e.preventDefault()
    
    fetch(`http://localhost:8000/gene/${change}`)
         .then(response => response.json())
         .then(result => setdata(result))
 }

  return (
    <div className='flex h-screen bg-blue-200 w-full'>
      <div className='flex bg-cover w-1/2' style={{ backgroundImage: `url(${image})` }} ><div><h1 className='bg-red-100'>FOUR LETTERS</h1><h2>ONE YOU</h2></div></div>
      <div className='flex w-1/2'>
      <input onChange={input} placeholder='Enter gene name'/>
      <button onClick={btn}>Search</button>
      {data &&(<div><p>{data.searched_name}</p>
      <p>{data.serial_number}</p>
      <p>A:{data.A}</p>
      <p>G:{data.G}</p>
      <p>T{data.T}</p>
      <p>C{data.C}</p>
      <p>{data.description}</p>
      </div>)}
      </div>
    </div>
  )
}

export default GeneSearch
