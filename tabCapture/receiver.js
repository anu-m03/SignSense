// stream object
let currentStream = null;
let imageCapture;
let grabFrameButton = document.getElementById("grabFrame");
let grabFrameButtonStop = document.getElementById("stop");
let canvasA = document.getElementById("canvasA");
let canvasB = document.getElementById("canvasB");
let subtitles = document.getElementById("captions");
const newDiv = document.createElement("div");
let lastDiv = document.getElementById("test");
let isFirst = true;

grabFrameButton.onclick = () => {
  if ( isFirst ) {
    grabFrame1()
    //isFirst = false;
    //renderInterval = setInterval(grabFrame1, 1000);
    
  } else {
    
  }
}

grabFrameButtonStop.onclick = () => {
  console.log("stopped");
  clearInterval(renderInterval);
  renderInterval = null;
}

// error handler
function printErrorMessage(message) {
  const element = document.getElementById('echo-msg');
  element.innerText = message;
  console.error(message);
}


// Stop video play-out and stop the MediaStreamTracks.
function shutdownReceiver() {
  if (!currentStream) {
    return;
  }

  const player = document.getElementById('player');
  player.srcObject = null;
  const tracks = currentStream.getTracks();

  for (let i = 0; i < tracks.length; ++i) {
    tracks[i].stop();
  }
  currentStream = null;
}

// Start video play-out of the captured MediaStream.
function playCapturedStream(stream) {
  if (!stream) {
    printErrorMessage(
      'Error starting tab capture: ' +
        (chrome.runtime.lastError.message || 'UNKNOWN')
    );
    return;
  }
  if (currentStream != null) {
    shutdownReceiver();
  }
  currentStream = stream;
  const player = document.getElementById('player');
  const track = currentStream.getVideoTracks()[0];
  imageCapture = new ImageCapture(track);
  player.addEventListener(
    'canplay',
    function () {
      this.volume = 0.75;
      this.muted = false;
      this.play();
      console.log("100");
    },
    {
      once: true
    }
  );
  player.setAttribute('controls', '1');
  player.srcObject = stream;
}

function testGetMediaStreamId(targetTabId, consumerTabId) {
  chrome.tabCapture.getMediaStreamId(
    { targetTabId, consumerTabId },
    function (streamId) {
      if (typeof streamId !== 'string') {
        printErrorMessage(
          'Failed to get media stream id: ' +
            (chrome.runtime.lastError.message || 'UNKNOWN')
        );
        return;
      }

      navigator.webkitGetUserMedia(
        {
          audio: false,
          video: {
            mandatory: {
              chromeMediaSource: 'tab', // The media source must be 'tab' here.
              chromeMediaSourceId: streamId
            }
          }
        },
        function (stream) {
          playCapturedStream(stream);
        },
        function (error) {
          printErrorMessage(error);
        }
      );
    }
  );
}


// grabFrame with download
function grabFrame1() {
  imageCapture
    .grabFrame()
    .then((imageBitmap) => {
      //console.log("Grabbed frame:", imageBitmap);
      canvasA.width = imageBitmap.width;
      canvasA.height = imageBitmap.height;
      
      
      //console.log("getting context...");
      
      canvasA.getContext("2d").drawImage(imageBitmap, 0, 0);
      
      //console.log("finished");
      canvasA.classList.remove("hidden");
      const newDiv = document.createElement("div");
      const newContent = document.createTextNode("etc etc ");
      newDiv.appendChild(newContent);
      
      document.body.insertBefore(newDiv, lastDiv.nextSibling);
      lastDiv = newDiv;
      
      //console.log(canvasA + "in grabframe");

      let image = document.getElementById('passThis');
      image.setAttribute('download', 'Frame1.png');
      image.setAttribute('src', canvasA.toDataURL("image/png").replace("image/png", "image/octet-stream"));

      sendData()
  
    })
    .catch((error) => {
      console.error("grabFrame() error: ", error);
    });
}

function sendData() {
  const base64Image = canvasA.toDataURL('image/png')
  $.ajax({
      url: '/upload_image',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({ 'image': base64Image}),
      success: function(response) {
        console.log("success")  
        //document.getElementById('output').innerHTML = response.result;
      },
      error: function(error) {
          console.log(error);
      }
  });
}

/*
function analyzeFrame() {
    grabFrame1();
    console.log(canvasA)
    let ctx1 = canvasA.getContext('2d', { willReadFrequently: true });
    setTimeout(function() {
  
      grabFrame1();
      console.log(canvasA.width);

      let ctx2 = canvasA.getContext('2d', { willReadFrequently: true });
      let data1 = ctx1.getImageData(0, 0, canvasA.width, canvasA.height);
      let data2 = ctx2.getImageData(0, 0, canvasA.width, canvasA.height);

      var different = [];
      
      //console.log(pixelmatch(data1, data2, null, 0.0001))

      if ( different.length > 1 ) {
        console.log(different);
      }
    }, 2000);
    
    
} */




chrome.runtime.onMessage.addListener(function (request) {
  const { targetTabId, consumerTabId } = request;
  testGetMediaStreamId(targetTabId, consumerTabId);
});


window.addEventListener('beforeunload', shutdownReceiver);