const imageForm = document.getElementById("image-form");
const formCSRF = document.getElementsByName('csrfmiddlewaretoken');
const avatarInput = document.getElementById('id_avatar');
const DisplayNewAvatar = document.getElementById('display-new-avatar');

const newAvatarURL = document.getElementById('new-avatar-url');
const imageCloesForm = document.getElementById('image-form-close');



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


// Update Avatar

avatarInput.addEventListener('change', ()=>{
    const newAvatar = avatarInput.files[0];
    const newAvatarUrlCreate = URL.createObjectURL(newAvatar);
    DisplayNewAvatar.innerHTML = `<img src="${newAvatarUrlCreate}" width="100%" class="rounded-circle mt-5" width="170px">`;
});

url = '';

imageForm.addEventListener('submit', (e)=>{
    e.preventDefault();
    const form = new FormData();
    form.append('csrfmiddlewaretoken', formCSRF[0].value);
    form.append('avatar', avatarInput.files[0]);
    $.ajax({
        type: 'POST',
        url: 'update_image',
        enctype: 'multipart/form-data',
        data: form,
        success: function (response){
            const newAvatar = avatarInput.files[0];
            const newAvatarUrlCreate = URL.createObjectURL(newAvatar);
            newAvatarURL.src = newAvatarUrlCreate
            alert('success', 'Avatar Updated Successfully')
            imageCloesForm.click()
        },
        error: function(error){
            // console.log(error)
            imageCloesForm.click()
            alert('danger', 'Opp... data invalid')
        },        
        cache: false,
        contentType: false,
        processData: false,
    })
})


// Add ELert For Success
////////////////
// Update Bio
const bioForm = document.getElementById('bio-form');
const bio = document.getElementById('id_bio');
const bioUpdated = document.querySelector(".bio");
const closeBioForm = document.getElementById('bio-close-form');

bioForm.addEventListener('submit', (e)=>{
    e.preventDefault();
    const form = new FormData();
    form.append('csrfmiddlewaretoken', formCSRF[1].value);
    form.append('bio', bio.value);

    $.ajax({
        type: 'POST',
        url: 'update_bio',
        data: form,
        success: function(response){
            bioUpdated.innerHTML = `<p>${response.bio}</p>`
            closeBioForm.click()
            alert('success', 'Bio Updated Successfully')
        },
        error: function(error){
            closeBioForm.click()
            alert('danger', 'Opp... data invalid')},
        cache: false,
        contentType: false,
        processData: false,
    })
})

/////////////////////////////////////////////////////////

// Myprofile Information
const infoForm = document.getElementById('information-form');
const username = document.getElementById('id_username');
const firstname = document.getElementById('id_first_name');
const lastname = document.getElementById('id_last_name');
const country = document.getElementById('id_country');
const gender = document.getElementById('id_gender');
const year = document.getElementById('id_date_of_birth_year');
const month = document.getElementById('id_date_of_birth_month');
const day = document.getElementById('id_date_of_birth_day');

const firstname_ = document.getElementById('first-name');
const lastname_ = document.getElementById('last-name');
const country_ = document.getElementById('country');
const gender_ = document.getElementById('gender');
const dataOfBirth = document.getElementById('date-of-birth');

const btnCloseInfoForm = document.getElementById('info-close-form')

infoForm.addEventListener('submit', (e)=>{
    e.preventDefault();
    const form = new FormData();
    form.append('csrfmiddlewaretoken', formCSRF[2].value);
    form.append('username', username.value);
    form.append('first_name', firstname.value);
    form.append('last_name', lastname.value);
    form.append('country', country.value);
    form.append('gender', gender.value);
    form.append('date_of_birth_year', year.value);
    form.append('date_of_birth_month', month.value);
    form.append('date_of_birth_day', day.value);

    

    $.ajax({
        type: 'POST',
        url: '',
        data: form,
        success: function(response){
            if (response.infoError.username){    
                alert('danger', response.infoError.username);
                const closeAlert = document.getElementById("close-alert");
                setTimeout(()=>{
                    closeAlert.click();
                }, 3000)
            };
            firstname_.innerHTML = response.first_name
            lastname_.innerHTML = response.last_name
            country_.innerHTML = response.country
            gender_.innerHTML = response.gender
            dataOfBirth.innerHTML = response.date

            btnCloseInfoForm.click();
            alert('success', 'Information Updated Successfully')
        },
        error: function(error){
            btnCloseInfoForm.click();
            alert('danger', 'Opp... data invalid')
        },
        cache: false,
        contentType: false,
        processData: false,
    })
})

// Display Error in page if Exists