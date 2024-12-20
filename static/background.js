var animation_time = 3 //s

function make_down() {
    var blocks = document.querySelectorAll("#background > .piece")
    var index = Math.floor(Math.random()*(blocks.length))

    if (!blocks[index].style.animation) {
        console.log(blocks)
        blocks[index].style.left = Math.floor(Math.random()*(window.innerWidth-blocks[index].offsetWidth)) + 'px'
        blocks[index].style.animation = `go_down  ${animation_time}s linear`
        blocks[index].style.visibility = "visible"
        setTimeout(()=>{
            // pour enlever l'animation, cette forme de texte est normale
            blocks[index].style.animation = ""
            blocks[index].style.visibility = "hidden"
        }, animation_time*1000)
    }
}

setInterval(make_down, 50)