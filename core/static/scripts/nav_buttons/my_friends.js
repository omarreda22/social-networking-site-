const unfriendForm = document.querySelectorAll('.unfriend');
const formCSRF = document.getElementsByName('csrfmiddlewaretoken');
const friendsCount = document.getElementById('friends-count');


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



for(let i=0; i<unfriendForm.length; i++){
    unfriendForm[i].addEventListener('submit', (e)=>{
        e.preventDefault();
        const friend = unfriendForm[i].classList[1];
        const id = unfriendForm[i].classList[2];
        const cardId = document.getElementById(`card--${id}`)

        const form = new FormData();
        form.append('friend', friend);
        form.append('csrfmiddlewaretoken', formCSRF[0].value);


        
        $.ajax({
            type: 'POST',
            url: `/myprofile/friend/delete/${friend}`,
            data: form,
            success: function(rep){
                num = friendsCount.textContent
                friendsNewCount = Number(num) - 1
                friendsCount.innerHTML = friendsNewCount
                cardId.remove();
                alert('success', 'Process Successful');
            },
            error: function(error){
                console.log(error)
            },
            cache: false,
            contentType: false,
            processData: false,
        })
    })
}
