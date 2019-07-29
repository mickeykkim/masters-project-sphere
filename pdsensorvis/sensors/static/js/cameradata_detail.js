"use strict";

// Video Elements
let currentFrame = $('#current-frame');
let currentTime = $('#current-time');
let videoTime = document.getElementById("video-time");
let videoDuration = document.getElementById("video-duration");

// Buttons
let playButton = document.getElementById("play-pause");
let muteButton = document.getElementById("mute");
let rewindButton = document.getElementById("rewind-video");
let seekBackwardButton = document.getElementById("seek-backward");
let seekForwardButton = document.getElementById("seek-forward");
let helpButton = document.getElementById("help");

// Range Sliders
let seekBar = document.getElementById("seek-bar");
let volumeBar = document.getElementById("volume-bar");

// Seek Value Elements
let rewindTextBox = document.getElementById("rewind-value");
let stepBackwardBox = document.getElementById("backward-increment");
let stepForwardBox = document.getElementById("forward-increment");
let copyFrameNumber = document.getElementById("copy-frame");
let copyTimeStamp = document.getElementById("copy-time");

// Framerate and Export Elements
/*
let stdFrameRates = {
   film: 24,
   NTSC: 29.97,
   NTSC_Film: 23.98,
   NTSC_HD: 59.94,
   PAL: 25,
   PAL_HD: 50,
   web: 30,
   high: 60
};
*/
let framerate = document.getElementById("framerate-list");
let currentFramerate; // assigned on page load of metadata
let currentVolume;

let video = VideoFrame({
   id: 'video',
   frameRate: currentFramerate,
   callback: function (frame) {
      currentFrame.html(video.get());
      currentTime.html(frame);
   }
});

function updatePlayButton(text) {
   if (text === "play") {
      playButton.innerHTML = "<i class=\"material-icons\">play_arrow</i>";
   } else if (text === "pause") {
      playButton.innerHTML = "<i class=\"material-icons\">pause</i>";
   }
}

function updateVolumeButton(text) {
   if (text === "mute") {
      muteButton.innerHTML = "<i class=\"material-icons\">volume_off</i>";
   } else if (text === "unmute") {
      muteButton.innerHTML = "<i class=\"material-icons\">volume_up</i>";
   }
}

function playVideo() {
   video.video.play();
   video.listen('SMPTE');
}

function pauseVideo() {
   video.video.pause();
   video.stopListen();
}

function updateVideoTime() {
   video.video.currentTime = seekBar.value / currentFramerate;
   currentFrame.html(video.get());
   currentTime.html(video.toSMPTE());
}

function updateSeekBar() {
   seekBar.value = video.video.currentTime * currentFramerate;
   refreshVideoTimes();
   currentFrame.html(video.get());
   currentTime.html(video.toSMPTE());
}

function refreshVideoTimes() {
   let curMins = Math.floor(video.video.currentTime / 60);
   let curSecs = Math.floor(video.video.currentTime - curMins * 60);
   let durMins = Math.floor(video.video.duration / 60);
   let durSecs = Math.floor(video.video.duration - durMins * 60);
   if (curSecs < 10) {
      curSecs = "0" + curSecs;
   }
   if (durSecs < 10) {
      durSecs = "0" + durSecs;
   }
   if (curMins < 10) {
      curMins = "0" + curMins;
   }
   if (durMins < 10) {
      durMins = "0" + durMins;
   }
   videoTime.innerHTML = curMins + ":" + curSecs;
   videoDuration.innerHTML = durMins + ":" + durSecs;
}

function toggleVideoPlayback() {
   if (video.video.paused === true) {
      playVideo();
      updatePlayButton("pause");
   } else {
      pauseVideo();
      updatePlayButton("play");
   }
}

function endVideo() {
   pauseVideo();
   updatePlayButton("play");
   updateSeekBar();
}

function rewindVideo() {
   let seekPosition = parseInt(rewindTextBox.value);
   video.video.currentTime = 0;
   if (seekPosition > 0) {
      video.seekForward(seekPosition, updateSeekBar());
   }
   pauseVideo();
   updatePlayButton("play");
}

function stepBack() {
   let backwardStep = stepBackwardBox.options[stepBackwardBox.selectedIndex].text;
   video.seekBackward(backwardStep, updateSeekBar());
   updatePlayButton("play");
}

function stepForward() {
   let forwardStep = stepForwardBox.options[stepForwardBox.selectedIndex].text;
   video.seekForward(forwardStep, updateSeekBar());
   updatePlayButton("play");
}

function copyToClipboard(selection) {
   let textToCopy;
   if (selection === "frames") {
      textToCopy = document.getElementById("current-frame");
   } else if (selection === "time") {
      textToCopy = document.getElementById("current-time")
   }
   let textArea = document.createElement("textarea");
   textArea.value = textToCopy.textContent;
   document.body.appendChild(textArea);
   textArea.select();
   document.execCommand("Copy");
   alert("Copied to clipboard: " + textArea.value)
   textArea.remove();
}

function displayHelpAlert() {
   const newLine = "\r\n";
   let helpMessage = "Shortcuts:";
   helpMessage += newLine;
   helpMessage += newLine;
   helpMessage += "Spacebar : Play/pause video.";
   helpMessage += newLine;
   helpMessage += "Shift + Right Arrow : Step frames forward by selected amount.";
   helpMessage += newLine;
   helpMessage += "Shift + Left Arrow : Step frames backward by selected amount.";
   helpMessage += newLine;
   helpMessage += "Shift + Up Arrow : Increase frame step amount.";
   helpMessage += newLine;
   helpMessage += "Shift + Down Arrow : Decrease frame step amount.";
   helpMessage += newLine;
   helpMessage += "Shift + / : Reset video to specified frame."
   alert(helpMessage);
}

function updateVolume(level) {
   currentVolume = level;
   video.video.volume = level;
}

// --- Event Listeners ---
video.video.addEventListener("loadedmetadata", function () {
   currentFramerate = parseFloat(framerate.options[framerate.selectedIndex].text);
   seekBar.max = video.video.duration * currentFramerate;
   refreshVideoTimes();
});

video.video.addEventListener("timeupdate", function () {
   updateSeekBar();
});

video.video.addEventListener("ended", function () {
   endVideo();
});

seekBar.addEventListener("change", function () {
   updateVideoTime();
   if (playButton.innerHTML === "Pause") {
      playVideo();
   }
});

seekBar.addEventListener("input", function () {
   updateVideoTime();
   if (playButton.innerHTML === "Pause") {
      playVideo();
   }
});

volumeBar.addEventListener("input", function () {
   updateVolume(volumeBar.level);
});

volumeBar.addEventListener("change", function () {
   updateVolume(volumeBar.level);
});

playButton.addEventListener("click", function () {
   toggleVideoPlayback();
});

helpButton.addEventListener("click", function () {
   displayHelpAlert();
});

video.video.addEventListener("click", function () {
   toggleVideoPlayback();
});

muteButton.addEventListener("click", function () {
   if (video.video.muted === false) {
      video.video.muted = true;
      updateVolumeButton("mute");
   } else {
      video.video.muted = false;
      updateVolumeButton("unmute");
   }
});

rewindButton.addEventListener("click", function () {
   rewindVideo();
});

seekBackwardButton.addEventListener("click", function () {
   stepBack();
});

seekForwardButton.addEventListener("click", function () {
   stepForward();
});

copyFrameNumber.addEventListener("click", function () {
   copyToClipboard("frames");
});

copyTimeStamp.addEventListener("click", function () {
   copyToClipboard("time");
});

// Keycodes for keypress event listeners
// 16 = shift, 32 = space, 37 = l arrow, 38 = up, 39 = right, 40 = down, 191 = forward slash
let map = {
   16: false,
   32: false,
   37: false,
   38: false,
   39: false,
   40: false,
   191: false
};

// Check for keypress and fire appropriate shortcut functions
$(document).keypress(function (e) {
   if (e.which === 32) {
      toggleVideoPlayback();
   }
});

// Listener for multiple key presses
$(document).keydown(function (e) {
   if (e.keyCode in map) {
      map[e.keyCode] = true;
      let backOption = stepBackwardBox.selectedIndex;
      let forwardOption = stepForwardBox.selectedIndex;
      if (map[16] && map[191]) {
         rewindVideo();
      } else if (map[16] && map[37]) {
         stepBack();
      } else if (map[16] && map[39]) {
         stepForward();
      } else if (map[16] && map[38]) {
         stepBackwardBox.options[parseInt(backOption) + 1].selected = true;
         stepForwardBox.options[parseInt(forwardOption) + 1].selected = true;
      } else if (map[16] && map[40]) {
         stepBackwardBox.options[parseInt(backOption) - 1].selected = true;
         stepForwardBox.options[parseInt(forwardOption) - 1].selected = true;
      }
   }
}).keyup(function (e) {
   if (e.keyCode in map) {
      map[e.keyCode] = false;
   }
});