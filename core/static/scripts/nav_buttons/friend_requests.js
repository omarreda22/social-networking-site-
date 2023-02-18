const requests = document.querySelectorAll('.friend_requests');
const formCSRF = document.getElementsByName('csrfmiddlewaretoken');


// Alert 
const alertBox = document.getElementById('alert-box')

const alert = function(statue, message){
    alertBox.innerHTML = `
    <div class="alert alert-${statue} alert-dismissible fade show mt-3 text-center" role="alert">
        ${message}.
        <button type="button" class="close" data-dismiss="alert" aria-label="Close" id="close-alert">
            <span aria-hidden="true">&times;</span>
        </button>
    </div>
    `
    const closeAlert = document.getElementById("close-alert");
    setTimeout(()=>{
        closeAlert.click();
    }, 3000)
}


for(let i=0; i<requests.length; i++){
    requests[i].addEventListener('submit', (e)=>{
        e.preventDefault();
        const relationshipId = requests[i].classList[1];
        const card = document.getElementById(`request-card-${relationshipId}`);
        const newStatus = "Accept";
        const form = new FormData();
        form.append('relationshipId', relationshipId);
        form.append('status', newStatus)
        form.append('csrfmiddlewaretoken', formCSRF[0].value);
        
        const requestsCount = document.getElementById('requests-count');
        const count = Number(requestsCount.textContent) - 1

        $.ajax({
            type: "POST",
            url: `/myprofile/${relationshipId}/friend_requests/new_status/`,
            data: form,
            success: function(response){
                requestsCount.innerHTML = count
                alert("success", "Friend Request Accepted");
                card.remove();
            },
            error: function(error){
                console.log(error);
            },
            cache: false,
            contentType: false,
            processData: false,
        })
    })
}



const removebuttons = document.querySelectorAll('.remove_friend_request');

for(let i=0; i<removebuttons.length; i++){
    removebuttons[i].addEventListener('click', (e)=>{
        e.preventDefault();
        const relationshipId = removebuttons[i].classList[4];
        const card = document.getElementById(`request-card-${relationshipId}`);
        const newStatus = "Remove";

        const form = new FormData();
        form.append('relationshipId', relationshipId);
        form.append('status', newStatus)
        form.append('csrfmiddlewaretoken', formCSRF[0].value);
        
        const requestsCount = document.getElementById('requests-count');
        const count = Number(requestsCount.textContent) - 1

        $.ajax({
            type: "POST",
            url: `/myprofile/${relationshipId}/friend_requests/new_status/`,
            data: form,
            success: function(response){
                requestsCount.innerHTML = count
                alert("success", "Friend Request Remove");
                card.remove();
            },
            error: function(error){
                console.log(error);
            },
            cache: false,
            contentType: false,
            processData: false,
        })
    })
}