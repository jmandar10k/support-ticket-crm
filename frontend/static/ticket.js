const params = new URLSearchParams(
    window.location.search
)

const ticketId = params.get("id")


async function loadTicket(){

    const response = await fetch(

        `/tickets/${ticketId}`

    )

    const data = await response.json()
    document.getElementById(
        "status"
        ).value=

        data.status


   document.getElementById(
"details"
).innerHTML=

`

<div class="card">

<h2>

${data.ticket_id}

</h2>

<p>

<b>Status:</b>

${data.status}

</p>

</div>


<div class="card">

<h3>

Customer Information

</h3>

<p>

<b>Name:</b>

${data.customer_name}

</p>

<p>

<b>Email:</b>

${data.customer_email}

</p>

</div>


<div class="card">

<h3>

Issue Information

</h3>

<p>

<b>Subject:</b>

${data.subject}

</p>

<p>

<b>Description:</b>

${data.description}

</p>

</div>


<div class="card">

<h3>

Notes History

</h3>

<ul>

${data.notes.map(

n => `

<li>

${n.note_text}

</li>

`

).join("")}

</ul>

</div>

`

}


async function updateTicket(){

    const status =
    document.getElementById(
        "status"
    ).value


    const notes =
    document.getElementById(
        "notes"
    ).value


    const response =
    await fetch(

        `/tickets/${ticketId}`,

        {

            method:"PUT",

            headers:{

                "Content-Type":
                "application/json"

            },

            body:JSON.stringify({

                status,

                notes

            })

        }

    )


    if(response.ok){

                document.getElementById(
        "message"
        ).className=

        "success"

        document.getElementById(
        "message"
        ).innerText=

        "Updated Successfully"


        document.getElementById(
            "notes"
        ).value = ""


        loadTicket()

    }

    else{

        document.getElementById(
            "message"
        ).innerText =

        "Update Failed"

    }

}


loadTicket()