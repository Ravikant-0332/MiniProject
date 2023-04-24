let mediaRecorder = NaN
let startBtn = document.getElementById("startBtn");
let stopBtn = document.getElementById("stopBtn");
let audioChunks = [];
//const socket = new WebSocket('ws://localhost:8000/ws/liveDictation/');

startBtn.onclick = async ()=>{
  const socket = new WebSocket('ws://localhost:8000/ws/liveDictation/');
  socket.onmessage = (e) => {
        result = JSON.parse(e.data).result;
        text = tinymce.activeEditor.getContent();
        pos = text.indexOf(">");
        tag = text.substr(1,pos-1);
        text = text.substr(pos+1);
        text = text.substr(0,text.length-pos-2);
        tinymce.activeEditor.setContent("<" + tag + ">" + text + " " + result + "</" + tag + ">");
  }

  socket.onclose = (e) => {
        console.log("Socket closed!");
  }

  await navigator.mediaDevices.getUserMedia({audio:true})
  .then((stream)=>{
    mediaRecorder = new MediaRecorder(stream,{mimeType : 'audio/webm', codecs : "opus"});
    mediaRecorder.start(1000);
    audioChunks = [];

    mediaRecorder.addEventListener("dataavailable", (ev)=>{
//        console.log(ev.data);
        audioChunks.push(ev.data);
//        var blob = new Blob(audioChunks, {'type':'audio/webm; codecs=opus'});
//        console.log(blob);
//        var data = new FormData();
//        data.append('data', blob, 'audio_blob');

        socket.send(JSON.stringify(
        {
            audioStream: "HI"
        }
        ));
        audioChunks = [];
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