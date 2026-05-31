const params = new URLSearchParams(
    window.location.search
)

const ticketId = params.get("id")


async function loadTicket(){

    const response = await fetch(

        `http://127.0.0.1:8000/tickets/${ticketId}`

    )

    const data = await response.json()
    document.getElementById(
        "status"
        ).value=

        data.status


    document.getElementById(
        "details"
    ).innerHTML =

`
<div>

<h2>

${data.ticket_id}

</h2>

<p>

<b>Customer:</b>

${data.customer_name}

</p>

<p>

<b>Email:</b>

${data.customer_email}

</p>

<p>

<b>Subject:</b>

${data.subject}

</p>

<p>

<b>Description:</b>

${data.description}

</p>

<p>

<b>Status:</b>

<span class="status">

${data.status}

</span>

</p>


<h3>

Notes

</h3>

<ul>

${
data.notes.map(

note =>

`

<li>

<b>

${new Date(
note.created_at
).toLocaleString()}

</b>

<br>

${note.note_text}

</li>

`

).join("")

}

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