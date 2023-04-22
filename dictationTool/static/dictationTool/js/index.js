let mediaRecorder = NaN
let startBtn = document.getElementById("startBtn");
let stopBtn = document.getElementById("stopBtn");
let audioChunks = [];
let looper = true;

startBtn.onclick = async ()=>{
  const socket = new WebSocket('ws://localhost:8000/ws/liveDictation/');
  socket.onmessage = (e) => {
        result = JSON.parse(e.data).result;
        document.getElementById("results").value += result + " ";
  }

  socket.onclose = (e) => {
        console.log("Socket closed!");
  }

  await navigator.mediaDevices.getUserMedia({audio:true})
  .then((stream)=>{
    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.start(3000);
    audioChunks = [];

    mediaRecorder.addEventListener("dataavailable", (ev)=>{
        socket.send(JSON.stringify(
        {
            audioStream : ev.data
        }
        ));
    });

    mediaRecorder.onstop = function(){
      socket.close();
    }
  }).catch((err)=>{
    window.alert(err.message);
  })
}

stopBtn.onclick = ()=>{
  mediaRecorder.stop();
}