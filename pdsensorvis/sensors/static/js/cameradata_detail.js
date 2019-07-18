"use strict";

var FrameRates = {
   film: 24,
   NTSC: 29.97,
   NTSC_Film: 23.98,
   NTSC_HD: 59.94,
   PAL: 25,
   PAL_HD: 50,
   web: 30,
   high: 60
};

// Video Elements
var currentFrame = $('#currentFrame');
var currentTime = $('#currentTime');
var videoTime = document.getElementById("videoTime");
var videoDuration = document.getElementById("videoDuration");
var currentFramerate = FrameRates.NTSC;

// Buttons
var playButton = document.getElementById("play-pause");
var muteButton = document.getElementById("mute");
var rewindButton = document.getElementById("rewind-video");
var seekBackward = document.getElementById("seek-backward");
var seekForward = document.getElementById("seek-forward");

// Range Sliders
var seekBar = document.getElementById("seek-bar");
var volumeBar = document.getElementById("volume-bar");

// Seek Value Elements
var rewindTextBox = document.getElementById("rewind-value");
var stepBackwardBox = document.getElementById("backward-increment");
var stepForwardBox = document.getElementById("forward-increment");
var backwardStepValue = stepBackwardBox.options[stepBackwardBox.selectedIndex].value;
var forwardStepValue = stepForwardBox.options[stepForwardBox.selectedIndex].value;

var video = VideoFrame({
   id : 'video',
   frameRate: currentFramerate,
   callback : function(frame) {
      currentFrame.html(video.get());
      currentTime.html(frame);
   }
});

function playVideo() {
   video.video.play();
   video.listen('SMPTE');
}

function pauseVideo() {
   video.video.pause();
   video.stopListen();
}

function updateVideoTime() {
   currentFrame.html(video.get());
   currentTime.html(video.toSMPTE());
   video.video.currentTime = seekBar.value / currentFramerate;
}

function updateSeekBar() {
   seekBar.value = video.video.currentTime * currentFramerate;
   refreshVideoTimes();
}

function refreshVideoTimes() {
   var curMins = Math.floor(video.video.currentTime / 60);
   var curSecs = Math.floor(video.video.currentTime - curMins * 60);
   var durMins = Math.floor(video.video.duration / 60);
   var durSecs = Math.floor(video.video.duration - durMins * 60);
   if(curSecs < 10){ curSecs = "0" + curSecs; }
   if(durSecs < 10){ durSecs = "0" + durSecs; }
   if(curMins < 10){ curMins = "0" + curMins; }
   if(durMins < 10){ durMins = "0" + durMins; }
   videoTime.innerHTML = curMins + ":" + curSecs;
   videoDuration.innerHTML = durMins + ":" + durSecs;
}

function endVideo() {
   pauseVideo();
   playButton.innerHTML = "Play";
   updateSeekBar();
}

video.video.addEventListener("loadedmetadata", function() {
   refreshVideoTimes();
   seekBar.max = video.video.duration * currentFramerate;
});

video.video.addEventListener("timeupdate", function() {
   updateSeekBar();
});

video.video.addEventListener("ended", function() {
   endVideo();
});

seekBar.addEventListener("change", function() {
   updateVideoTime();
});

seekBar.addEventListener("input", function() {
   if (playButton.innerHTML === "Pause") {
      pauseVideo();
   }
   updateVideoTime();
});

seekBar.addEventListener("change", function() {
   if (playButton.innerHTML === "Pause") {
      playVideo();
   }
});

volumeBar.addEventListener("input", function() {
   video.video.volume = volumeBar.value;
});

volumeBar.addEventListener("change", function() {
   video.video.volume = volumeBar.value;
});

playButton.addEventListener("click", function() {
   if (video.video.paused == true) {
      playVideo();
      playButton.innerHTML = "Pause";
   } else {
      pauseVideo();
      playButton.innerHTML = "Play";
   }
});

muteButton.addEventListener("click", function() {
   if (video.video.muted == false) {
      video.video.muted = true;
      muteButton.innerHTML = "Unmute";
   } else {
      video.video.muted = false;
      muteButton.innerHTML = "Mute";
   }
});

rewindButton.addEventListener("click", function() {
   var seekPosition = parseInt(rewindTextBox.value);
   video.video.currentTime = 0;
   video.seekForward(seekPosition);
   updateVideoTime();
   updateSeekBar();
   playButton.innerHTML = "Play";
});
