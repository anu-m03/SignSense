// stream object
let currentStream = null;
let imageCapture;
let grabFrameButton = document.getElementById("grabFrame");
let canvasA = document.getElementById("canvasA");
let canvasB = document.getElementById("canvasB");

grabFrameButton.onclick = grabFrame1;

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

function analyzeFrame(canvas1, canvas2) {
  var data1 = canvas1.getImageData

  var different = [];

  for (var y=0; y<img1.height; y++){
      for (var x=0; x<img1.width; i++){
          var pos = (x * 4) + (y * (img.width * 4));
          for (var i=0; i<4; i++){
              if (data1[pos + i] != data2[pos + i]){
                different.push({x: x, y: y});
              }
          }
      }
  }
}

// grabFrame with download
function grabFrame1() {
  imageCapture
    .grabFrame()
    .then((imageBitmap) => {
      console.log("Grabbed frame:", imageBitmap);
      canvasA.width = imageBitmap.width;
      canvasA.height = imageBitmap.height;
      canvasA.getContext("2d").drawImage(imageBitmap, 0, 0);
      canvasA.classList.remove("hidden");

      var link = document.getElementById('link');
      link.setAttribute('download', 'Frame1.png');
      link.setAttribute('href', canvasA.toDataURL("image/png").replace("image/png", "image/octet-stream"));
      link.click();
    })
    .catch((error) => {
      console.error("grabFrame() error: ", error);
    });
}

function grabFrame2() {
  imageCapture
    .grabFrame()
    .then((imageBitmap) => {
      console.log("Grabbed frame:", imageBitmap);
      canvasA.width = imageBitmap.width;
      canvasA.height = imageBitmap.height;
      canvasA.getContext("2d").drawImage(imageBitmap, 0, 0);
      canvasA.classList.remove("hidden");

      

      analyzeFrame()

    })
    .catch((error) => {
      console.error("grabFrame() error: ", error);
    });
}


chrome.runtime.onMessage.addListener(function (request) {
  const { targetTabId, consumerTabId } = request;
  testGetMediaStreamId(targetTabId, consumerTabId);
});


window.addEventListener('beforeunload', shutdownReceiver);
