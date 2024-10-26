// stream object
let currentStream = null;

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
const imagePreview = async ({ videoRef }) => {
  try {
    const videoElem = videoRef.current
    if (!videoElem) throw Error("Video HTML element not defined")

    videoElem.srcObject = await navigator.mediaDevices.getDisplayMedia()

    return videoElem.srcObject
  } catch (error) {
    console.error("imagePreview error: " + error)
  }
}


const imageCapture = async ({ videoRef }) => {
  try {
    const videoElem = videoRef.current
    if (!videoElem) throw Error("Video HTML element not defined")

    let mediaStream = videoElem.srcObject
    if (!mediaStream) throw Error("Video MediaStream not defined")

    const track = mediaStream.getVideoTracks()[0]
    const image = generateImageWithCanvas(track, videoElem)
    // const image = await generateImageWithImageCapture(mediaStreamTrack);

    mediaStream.getTracks().forEach(track => track.stop())

    return image
  } catch (error) {
    console.error("imageCapture error: " + error)
  }
}

const generateImageWithCanvas = (track, videoElem) => { // convert mediatrack to canvas
  const canvas = document.createElement("canvas")

  const { width, height } = track.getSettings()
  canvas.width = width || 100
  canvas.height = height || 100

  canvas.getContext("2d")?.drawImage(videoElem, 0, 0)
  const image = canvas.toDataURL("image/png")

  return image
}

function downloadImage() { // convert canvas to downloaded image file
  var link = document.getElementById('link');
  link.setAttribute('download', 'imageurl.png');
  link.setAttribute('href', canvas.toDataURL("image/png").replace("image/png", "image/octet-stream"));
  link.click();
}



chrome.runtime.onMessage.addListener(function (request) {
  const { targetTabId, consumerTabId } = request;
  testGetMediaStreamId(targetTabId, consumerTabId);
});

window.addEventListener('beforeunload', shutdownReceiver);
