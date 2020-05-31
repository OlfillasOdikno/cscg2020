cps = ()=>{
    fetch(`/cmd/move ${window.destination[0]} ${window.destination[1]} 0.015`)
}

send_cmd=()=>{
    let cmd = document.getElementById("cmd").value
    fetch(`/cmd/${cmd}`).then(r=>{
        return r.json()
    }).then(j=>{
        let o = document.getElementById("output")
        o.value += `> ${cmd}\n`
        o.value += `${j['resp']}\n`
        o.scrollTop = o.scrollHeight
    })
    document.getElementById("cmd").value = ""
}

trace=()=>{
    if(window.tracing){
        document.getElementById("trace-btn").textContent = "start trace"
        window.tracing = false;
        return;
    }
    window.tracing = true;
    window.trace_path = []
    document.getElementById("trace-btn").textContent = "stop trace"

    let sel = document.getElementById('trace-select')
    window.trace_target = sel.options[sel.selectedIndex].value
}
window.tracing = false;
window.onload = function () {
    var img = new Image()
    img.src = "/static/map.bmp"
    img.onload = () => {

        let destination = [0, 0]
        var c = document.getElementById("map");
        var c2 = document.getElementById("map2");
        var ctx = c.getContext("2d");
        var ctx2 = c2.getContext("2d");
        ctx.imageSmoothingEnabled = false;
        ctx.drawImage(img, 0, 0, 64, 64, 0, 0, c.width, c.height);
        c.addEventListener("mousedown", (ev) => {
            const rect = c.getBoundingClientRect()
            let x = ev.clientX - rect.left
            let y = ev.clientY - rect.top
            destination[0] = Math.round((x / rect.width) * 64 - 0.5)
            destination[1] = Math.round((y / rect.height) * 64 - 0.5)
            window.destination = destination
            fetch(`/cmd/path ${destination[0]} ${destination[1]}`)
                .then((response) => {
                    return response.json();
                })
                .then((data) => {
                    window.last_path = data['resp']
                })

        })

        let draw_pos = () => {
            fetch('/cmd/state')
                .then((response) => {
                    return response.json();
                })
                .then((data) => {
                    data = data['resp']
                    let draw_in_grid = (x, y, r) => {
                        ctx.arc(((x + 0.5) / 64) * c.width, ((y + 0.5) / 64) * c.height, r, 0, 2 * Math.PI, false);
                    }


                    let x = ((data.pos.x - 5)/480)*c.width
                    let z = ((data.pos.z - 2)/480)*c.height

                    let gx = data.grid_pos.x
                    let gy = data.grid_pos.y

                    let radius = 10
                    ctx.clearRect(0,0,c.width,c.height)
                    ctx.drawImage(img, 0, 0, 64, 64, 0, 0, c.width, c.height);


                    if (window.last_path && window.last_path.length > 2) {

                        ctx.beginPath();
                        ctx.moveTo(((window.last_path[0][0] + 0.5) / 64) * c.width, ((window.last_path[0][1] + 0.5) / 64) * c.height);
                        let should_draw = false
                        for (let i = 0; i < window.last_path.length; i++) {
                            e = window.last_path[i]
                            if(should_draw){
                                ctx.lineTo(((e[0] + 0.5) / 64) * c.width, ((e[1] + 0.5) / 64) * c.height);
                            }
                            ctx.moveTo(((e[0] + 0.5) / 64) * c.width, ((e[1] + 0.5) / 64) * c.height);
                            if (e[0] == gx && e[1] == gy) {
                                should_draw = true
                            }
                        }
                        if (!should_draw) {
                            fetch(`/cmd/path ${destination[0]} ${destination[1]}`)
                                .then((response) => {
                                    return response.json();
                                })
                                .then((data) => {
                                    window.last_path = data['resp']
                                })
                        }
                        ctx.stroke();
                    }
                    /*
                    //draw grid-pos
                    ctx.beginPath();
                    draw_in_grid(gx, gy, radius);
                    ctx.fillStyle = 'blue';
                    ctx.fill();
                    */

                    //draw other players
                    let sel = document.getElementById('trace-select');
                    for (let uid of Object.keys(data.npcs)) {
                        v = data.npcs[uid]
                        ctx.beginPath();
                        ctx.arc( ((v.pos.x - 5)/480)*c.width, c.height - ((v.pos.z - 2)/480)*c.height, radius, 0, 2 * Math.PI, false);
                        ctx.fillStyle = 'orange';
                        ctx.fill();
                        ctx.font = "28px Arial";
                        ctx.fillStyle = 'black';
                        ctx.fillText(parseInt(uid).toString(16), ((v.pos.x - 5)/480)*c.width, c.height - ((v.pos.z - 2)/480)*c.height);

                        var children = sel.children;
                        let found = false;
                        for (var i = 0; i < children.length; i++) {
                            if(children[i].value == uid){
                                found = true;
                                break;
                            }
                        }
                        if(!found){
                            var opt = document.createElement('option');

                            opt.appendChild( document.createTextNode(uid) );
    
                            opt.value = uid; 
    
                            sel.appendChild(opt); 
                        }

                    }

                    //draw trace
                    ctx.strokeStyle = 'red'

                    if(window.tracing){
                        let uid = window.trace_target
                        if(Object.keys(data.npcs).indexOf(uid) != -1){
                            window.trace_path.push(data.npcs[uid].pos)
                        }
                        let should_draw = false
                        ctx.beginPath()
                        for (let i = 0; i < window.trace_path.length; i++) {
                            e = window.trace_path[i]
                            let x = ((e.x - 5)/480)*c.width
                            let y = c.height - ((e.z - 2)/480)*c.height
                            if(should_draw){
                                ctx.lineTo(x,y)
                            }
                            ctx.moveTo(x,y)
                            should_draw=true;
                        }
                        ctx.stroke()
                        console.log(window.trace_path)

                    }

                    //draw look angle
                    let v_len = radius*2.5;
                    ctx.beginPath();
                    ctx.moveTo(x, c.height - z);
                    ctx.lineTo(x + this.Math.sin((data.rot.y) * Math.PI / 180) * v_len, c.height - z - this.Math.cos((data.rot.y) * Math.PI / 180) * v_len);
                    ctx.strokeStyle = 'red';
                    ctx.stroke();

                    //draw destination
                    ctx.beginPath();
                    draw_in_grid(destination[0], destination[1], radius)
                    ctx.fillStyle = 'red';
                    ctx.fill();



                    //draw player
                    ctx.beginPath();
                    ctx.arc(x, c.height - z, radius, 0, 2 * Math.PI, false);
                    ctx.fillStyle = 'green';
                    ctx.fill();




                    ctx2.save()
                    ctx2.clearRect(0,0,c2.width, c2.height)
                    ctx2.beginPath()
                    ctx2.arc(c2.width/2, c2.height/2, c2.width/2, 0, 2 * Math.PI)
                    ctx2.closePath()
                    ctx2.clip()
                    ctx2.translate(c2.width / 2, c2.height / 2)
                    ctx2.rotate((-data.rot.y) * Math.PI / 180)
                    ctx2.scale(2, 2)
                    ctx2.translate(-c2.width / 2, -c2.height / 2)
                    ctx2.drawImage(c, x - c2.width / 2, c.height - z - c2.height / 2, c.width, c.height, 0, 0, c.width, c.height)


                    ctx2.restore()

                    let d = Math.atan2(destination[0]-gx,gy-destination[1])-this.Math.PI/2 + (-data.rot.y) * Math.PI / 180
                    let d2 = Math.min(1/this.Math.pow((Math.sqrt((destination[0]-gx)*(destination[0]-gx)+(gy-destination[1])*(gy-destination[1]))/64),0.7),6)
                    ctx2.beginPath()
                    ctx2.arc(c2.width/2, c2.height/2, c2.width/2 -5, d-0.1*d2, d+0.1*d2, false);
                    ctx2.strokeStyle = 'red'
                    ctx2.lineWidth  = 10
                    ctx2.stroke();

                    this.document.getElementById("player-pos").textContent = `${data.pos.x} ${data.pos.y} ${data.pos.z} `
                });
        }
        setInterval(draw_pos, 100)
    }

    document.getElementById("cmd").addEventListener("keyup", ev=>{
        if (ev.keyCode === 13) {
            ev.preventDefault()
            send_cmd()
        }
    })

}; 