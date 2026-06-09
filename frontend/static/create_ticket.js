
const form=

document.getElementById(
"ticketForm"
)


function handleUnauthorized(

response

){

if(

response.status===401

){

localStorage.clear()

window.location.href=

"/login-page"

return true

}

return false

}


form.addEventListener(

"submit",

async function(event){

event.preventDefault()

try{

const data={

customer_name:

document.getElementById(

"customer_name"

).value,


customer_email:

document.getElementById(

"customer_email"

).value,


subject:

document.getElementById(

"subject"

).value,


description:

document.getElementById(

"description"

).value

}


const response=

await fetch(

"/tickets",

{

method:"POST",

headers:{

"Content-Type":

"application/json",

Authorization:

`Bearer ${localStorage.getItem("token")}`

},

body:

JSON.stringify(

data

)

}

)


if(

handleUnauthorized(

response

)

){

return

}


const result=

await response.json()


document.getElementById(

"result"

).className=

"success"


document.getElementById(

"result"

).innerText=

"Created Successfully: "

+

result.ticket_id


setTimeout(

()=>{

location.replace(

"/dashboard"

)

},

1000

)

}

catch(error){

console.log(

error

)

}

}

)