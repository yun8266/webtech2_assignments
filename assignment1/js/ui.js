// Start the loading bar
function startLoading(){
    document.querySelector(".loading").style.display="block";
}

// Stop the loading bar
function stopLoading(){
    document.querySelector(".loading").style.display="none";
}

function hideBranches(){
    document.querySelector(".branches").style.display = "none"
}

function showBranches(){
    document.querySelector(".branches").style.display = "block"
}

// Show error banner on top for time milliseconds
// If time is undefined then show inifinitely
function showError(text,time){
    const errorElement = document.querySelector(".error")
    errorElement.innerHTML = text
    errorElement.style.display="block"
    if (time){
        setTimeout(()=>{
            errorElement.style.display="none"
        },time)
    }
}

// Hide error banner on top
function hideError(){
    document.querySelector(".error").style.display ="none"
}

function clickHandler(elem){
    if (elem.classList.contains("active") ) {
        unselect(elem)
    }
    else if (!elem.classList.contains("unavailable")) {
        select(elem)
    }
}
console.log()

// Initalizes UI with given data array
// This creates elements
function initUI(data){
    const b = document.querySelector(".branches")
    const next = data.Topics.forEach((branch,i)=>{
        const article = document.createElement("article")
        article.innerHTML = (
            `<h1 class="name">${branch.Abbr}</h1>
            <h3 class="desc">${branch.Name}</h2>
            <p class="remaining"> Remaining: ${branch.seats}</p>`
            )
        article.classList.add("branch")
        if (data.selection===i){
            article.classList.add("active")
        }
        else if (branch.seats==0){
            article.classList.add("unavailable")
        }

        article.setAttribute("data-i",i)
        article.onclick = ()=>clickHandler(article)
        branches.push(article)
        b.appendChild(article)
    })
}

// Updates existing elements. This does not create new elements.
// This is to keep the CSS Transitions at place.
function updateUI(data){
    const topics = data.Topics
    branches.forEach((branch,i)=>{
        branch.querySelector(".name").innerHTML = topics[i].Abbr
        branch.querySelector(".desc").innerHTML = topics[i].Name
        branch.querySelector(".remaining").innerHTML = "Remaining: "+topics[i].seats
        branch.classList.remove("active","unavailable")
        if (data.selection===i){
            console.log(branch)
            branch.classList.add("active")
        }
        else if (topics[i].seats==0){   
            branch.classList.add("unavailable")
        }
    })
}