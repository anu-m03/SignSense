// stream object
let currentStream = null;
let imageCapture;
let grabFrameButton = document.getElementById("grabFrame");
let grabFrameButtonStop = document.getElementById("stop");
let canvasA = document.getElementById("canvasA");
const newDiv = document.createElement("div");
let lastDiv = document.getElementById("test");
let isFirst = true;

grabFrameButton.onclick = () => {
  if ( isFirst ) {
    grabFrame1()
    //isFirst = false;
    renderInterval = setInterval(async function() {await grabFrame1(); sendData()}, 1000);
    
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
  if (player != null) {
    player.srcObject = null;
  }
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
  if (player != null) {
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
  } else {
    console.log("hello")
  }
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
async function grabFrame1() {
  imageCapture
    .grabFrame()
    .then((imageBitmap) => {
      //console.log("Grabbed frame:", imageBitmap);
      canvasA.width = imageBitmap.width;
      canvasA.height = imageBitmap.height;
      
      
      //console.log("getting context...");
      
      canvasA.getContext("2d").drawImage(imageBitmap, 0, 0);
      
      //console.log("finished");
      const newDiv = document.createElement("p");
      const newContent = document.createTextNode("etc etc ");
      newDiv.appendChild(newContent);
      
      document.body.insertBefore(newDiv, lastDiv.nextSibling);
      lastDiv = newDiv;
      
      //console.log(canvasA + "in grabframe");

      let image = document.getElementById('passThis');
      image.setAttribute('download', 'Frame1.png');
      image.setAttribute('src', canvasA.toDataURL("image/png").replace("image/png", "image/octet-stream"));

  
    })
    .catch((error) => {
      console.error("grabFrame() error: ", error);
    });
}

async function sendData() {
  const image = canvasA.toDataURL('image/png')

    // Convert base64 image data to a Blob
    const response = await fetch(image);
    const blob = await response.blob();

  const formattedData = new FormData();
  formattedData.append('image', blob, 'captured_frame.png');

  // Make the AJAX request
  $.ajax({
      url: "http://localhost:5000/upload_image",
      type: 'POST',
      data: formattedData,
      processData: false, // Prevent jQuery from automatically transforming the data into a query string
      contentType: false, // Prevent jQuery from setting Content-Type, since FormData will do it
      success: function(response) {

        console.log("Success:", response);
      },
      error: function(error){
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