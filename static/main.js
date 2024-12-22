const { animate, scroll,linear } = Motion

class SocEv { 
    constructor(WebSocket){
        this.WebSocket = WebSocket
    }

    send_text = (message) =>{
        this.WebSocket.send(JSON.stringify(message))
    }

    on = (event,callback) =>{

        this.WebSocket.addEventListener("message",(msg)=>{
            msg = JSON.parse(msg.data)
           
            if (msg.event == event){
               
                callback(msg)
            }
        })
    }

}



class Bar {
    static Bars = []
    static socket = null

    constructor(element,id){
        this.element = element
        this.id = id
        this.socket = Bar.socket
        this.barElement = element.querySelector(".bar").querySelector(".progress")
        this.timeperiod = element.querySelector(".time_period")
        this.text = element.querySelector(".flavour")

        this.speed = null
        this.interval = null
        
        Bar.Bars.push(this)
        this.connect_bar()
        this.setup_sliders()
    }

    static get = (id) =>{
        let bar = null
        this.Bars.forEach((e)=>{
            if(e.id === id){
                bar = e
            }
        })
        return bar
    }

    connect_bar = ()=>{
        const message = {
            "event":"connect_bar",
            "id":this.id
        }
        console.log(message)
        if (this.socket.readyState === WebSocket.OPEN){
            this.socket.send(JSON.stringify(message))
        } else{
            this.socket.addEventListener('open',()=>{
                this.socket.send(JSON.stringify(message))
            })
        }
    }

    setup_sliders = ()=>{
        let sliders = this.element.querySelectorAll(".slider")
        sliders.forEach((slider)=>{
            let inp = slider.querySelector("input")
            let type = inp.classList[0]
            let out = slider.querySelector("span")
            out.innerText = inp.value
            this[type] = inp.value

            inp.addEventListener("input",(e)=>{
                let val = inp.value
                out.innerText = val
                this[type] = inp.value
                console.log(this[type])
            })
            

        })
        
    }

    start_bar = ()=>{
        const message = {
            "event":"start",
            "id":this.id,
            "speed":this.speed,
            "interval":this.interval
        }
        this.socket.send(JSON.stringify(message))
    }
    pause_bar = ()=>{
        const message = {
            "event":"pause",
            "id":this.id
        }   
        this.socket.send(JSON.stringify(message))
    }

    advance = (progress,duration,text,time)=>{
        let barEl = this.barElement
        let barText = this.text
        let barTime = this.timeperiod
        animate(barEl,{width:[barEl.style.width,progress+"%"]},{duration:duration})
        barText.innerText = text
        barTime.innerText = time
        
        
    }
}

document.addEventListener("DOMContentLoaded",()=>{

    const barElements = document.querySelectorAll(".bar-container")

    const socket = new WebSocket("/bar")
    const socev = new SocEv(socket)
    Bar.socket = socket

    barElements.forEach(element=>{
        let bar = new Bar(element,element.id)
        const controls = element.querySelector(".controls").querySelectorAll("button")
        controls.forEach(control=>{
            control.addEventListener("click",(e)=>{
                btn = e.target
                handleButton(btn,bar,socket)
            })
        })

    })

    socev.on("progress",(msg)=>{
        const elbar = Bar.get(msg.id)
        elbar.advance(msg.progress,msg.interval,msg.text,msg.time)
    })
    
})


const handleButton = (control,bar,socket)=>{
  
    console.log(bar.sliders)
    action = control.classList[0]
    switch (action){
        case "start":
            bar.start_bar()
            break
        case "pause":
            bar.pause_bar()
            break
        default:
            console.log("invalid event")
            break
    }

}