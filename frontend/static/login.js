
async function login(){

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

"/login",

{

method:"POST",

headers:{

"Content-Type":

"application/json"

},

body:JSON.stringify({

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

localStorage.setItem(

"token",

data.access_token

)


localStorage.setItem(

"name",

data.name

)


window.location.href="/dashboard"

}

else{

document.getElementById(
"message"
).innerText=

data.detail

}

}
