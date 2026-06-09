
async function signup(){

const name=

document.getElementById(
"name"
).value


const email=

document.getElementById(
"email"
).value


const password=

document.getElementById(
"password"
).value


const response=

await fetch(

"/signup",

{

method:"POST",

headers:{

"Content-Type":

"application/json"

},

body:JSON.stringify({

name,

email,

password

})

}

)


const data=

await response.json()


if(

response.ok

){

document.getElementById(
"message"
).className=

"success"


document.getElementById(
"message"
).innerText=

"Signup Successful. Redirecting..."


setTimeout(

()=>{

window.location.href=

"/login-page"

},

1500

)

}

else{

document.getElementById(
"message"
).innerText=

data.detail

}

}