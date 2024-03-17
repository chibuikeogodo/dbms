const sidebar = document.getElementById('app-primary-sidebar')
const secondary_sidebar = document.getElementById('secondary-sidebar')
const student_form = document.getElementById('student-form')
const staff_form = document.getElementById('staff-form')

const select_year = document.getElementById('year-val')
const programs = document.getElementById('programs')

const secondary_sidebar_title = document.getElementById('secondary-sidebar-title')

const goBack=()=>{
    history.back()
}

const studentDetails=(id)=>{
    location = `/students/${id}/`
}

const staffDetails=(id)=>{
    location = `/staff/${id}/`
}

const volunteersDetails=(id)=>{
    location = `/volunteer/${id}/`
}


const toggle_navbar=(open=false)=>{
    if(open){
        sidebar.style.transform = "translateX(-250px)"
    }else{
        sidebar.style.transform = "translateX(0px)"
    }
}

function setActiveDiv(id) {
    // Remove "div-active" class from all elements with class "my-div"
    var elements = document.getElementsByClassName("my-form-container");
    for (var i = 0; i < elements.length; i++) {
        elements[i].classList.remove("my-form-container-active");
    }

    // Add "my-form-container-active" class to the element with the provided id
    var element = document.getElementById(id);
    if (element) {
        element.classList.add("my-form-container-active");
    } else {
        console.log("Element with id '" + id + "' not found.");
    }
}


const open_secodary_sidebar=(form=null)=>{
    // students, staff, volunteers

    if(form){
        if(form === "student-form"){
            secondary_sidebar_title.innerText = "Add Student"
        }else if(form === "grade-form"){
            secondary_sidebar_title.innerText = "Edit Student Grade"
        }else if(form === "staff-form"){
            secondary_sidebar_title.innerText = "Manage Staff"
        }else if(form === "program-form"){
            secondary_sidebar_title.innerText = "Add Program"
        }else if(form === "contact-form"){
            secondary_sidebar_title.innerText = "Emergency Contact"
        }else if(form === "sponsor-form"){
            secondary_sidebar_title.innerText = "Sponsors"
        }else if(form === "volunteer-form"){
            secondary_sidebar_title.innerText = "Volunteers"
        }else{
            // secondary_sidebar_title.innerText = "Manage Staff"
        }
        setActiveDiv(form)
        secondary_sidebar.style.display = "block"
    }else{
        secondary_sidebar.style.display = "none"
    }
}


const navbar = document.getElementById('mini-nav');
const main_section = document.getElementById('app-main-section');

    main_section.addEventListener('scroll', function() {
      if (main_section.scrollTop >= 150) {
        navbar.classList.add('min-nav-fixed');
      } else {
        navbar.classList.remove('min-nav-fixed');
      }
    });



const change_year=()=>{
    let val = select_year.value

   if(val.includes(':')){
        val = val.split(":")
        const quarter = val[1].slice(1)
        if(quarter.length > 0){
            location = `?year=${val[0]}&quarter=${val[1].slice(1)}`
        }else{
            location = `?year=${val[0]}`
        }
        
    }else{
        location = `?year=${val}`   
    }
}

const since_2014 = ()=>{
    location = "/"
}


const filter_student=()=>{
    let val = programs.value

   if(val !== 'all'){

      location = `?program=${val}` 

    }else{
        location = location.pathname  
    }
}


function setProgress(percent) {
    const progressRing = document.querySelector('.progress-ring');
    const progressRingRemaining = document.querySelector('.progress-ring-remaining');
    const text = document.querySelector('.progress-text');
  
    const circumference = 251.2;
    //const offset = circumference - (percent / 100) * circumference;
    const offset = (percent*circumference/100) * -1
  
    progressRingRemaining.style.strokeDashoffset = offset;
    text.textContent = percent + '%';
}
  

// open_secodary_sidebar("student")
window.onload = function() {
    // Get the URL parameters

    const urlParams = new URLSearchParams(window.location.search);
    
    // Check if the 'param' parameter exists in the URL
    if (urlParams.has('edit') && urlParams.has('form')) {
        // Call your function if the 'param' parameter exists
        // yourFunction();
        const form = urlParams.get('form')
        open_secodary_sidebar(form);
    }
};



