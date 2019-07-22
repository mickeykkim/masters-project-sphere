"use strict";

// Video Elements
var currentFrame = $('#currentFrame');
var currentTime = $('#currentTime');
var videoTime = document.getElementById("videoTime");
var videoDuration = document.getElementById("videoDuration");

// Buttons
var playButton = document.getElementById("play-pause");
var muteButton = document.getElementById("mute");
var rewindButton = document.getElementById("rewind-video");
var seekBackwardButton = document.getElementById("seek-backward");
var seekForwardButton = document.getElementById("seek-forward");
var helpButton = document.getElementById("help");

// Range Sliders
var seekBar = document.getElementById("seek-bar");
var volumeBar = document.getElementById("volume-bar");

// Seek Value Elements
var rewindTextBox = document.getElementById("rewind-value");
var stepBackwardBox = document.getElementById("backward-increment");
var stepForwardBox = document.getElementById("forward-increment");
var copyFrameNumber = document.getElementById("copy-frame");
var copyTimeStamp = document.getElementById("copy-time");

// Framerate and Export Elements
/*
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
*/
var framerate = document.getElementById("framerate-list");
var currentFramerate = parseFloat(framerate.options[framerate.selectedIndex].text);

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

function toggleVideoPlayback() {
   if (video.video.paused == true) {
      playVideo();
      playButton.innerHTML = "Pause";
   } else {
      pauseVideo();
      playButton.innerHTML = "Play";
   }
}

function endVideo() {
   pauseVideo();
   playButton.innerHTML = "Play";
   updateSeekBar();
}

function rewindVideo() {
   var seekPosition = parseInt(rewindTextBox.value);
   video.video.currentTime = 0;
   if (seekPosition > 0) {
      video.seekForward(seekPosition, updateSeekBar());
   }
   playButton.innerHTML = "Play";
}

function stepBack() {
   var backwardStep = stepBackwardBox.options[stepBackwardBox.selectedIndex].text;
   video.seekBackward(backwardStep, updateSeekBar());
   playButton.innerHTML = "Play";
}

function stepForward() {
   var forwardStep = stepForwardBox.options[stepForwardBox.selectedIndex].text;
   video.seekForward(forwardStep, updateSeekBar());
   playButton.innerHTML = "Play";
}

function setSelectedIndex(s, i) {
   s.options[i - 1].selected = true;
}

function copyToClipboard(selection) {
   var textToCopy;
   if (selection === "frames") {
      textToCopy = document.getElementById("currentFrame");
   } else if (selection === "time") {
      textToCopy = document.getElementById("currentTime")
   }
   var textArea = document.createElement("textarea");
   textArea.value = textToCopy.textContent;
   document.body.appendChild(textArea);
   textArea.select();
   document.execCommand("Copy");
   alert("Copied to clipboard: " + textArea.value)
   textArea.remove();
}

function displayHelpAlert() {
   alert("Shortcuts:\nSpacebar: Play/Pause Video\nShift + Right Arrow to step frames forward by selected amount.\nShift + Left Arrow to step frames backward by selected amount.\nShift + Up Arrow to increase frame step rate.\nShift + Down Arrow to decrease frame step rate.\nShift + / to reset video to specified frame.");
}

// --- Event Listeners ---
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
   if (playButton.innerHTML === "Pause") {
      playVideo();
   }
});

seekBar.addEventListener("input", function() {
   updateVideoTime();
   if (playButton.innerHTML === "Pause") {
      pauseVideo();
   }
});

volumeBar.addEventListener("input", function() {
   video.video.volume = volumeBar.value;
});

volumeBar.addEventListener("change", function() {
   video.video.volume = volumeBar.value;
});

playButton.addEventListener("click", function() {
   toggleVideoPlayback();
});

helpButton.addEventListener("click", function() {
   displayHelpAlert();
});

video.video.addEventListener("click", function() {
   toggleVideoPlayback();
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
   rewindVideo();
});

seekBackwardButton.addEventListener("click", function() {
   stepBack();
});

seekForwardButton.addEventListener("click", function() {
   stepForward();
});

copyFrameNumber.addEventListener("click", function() {
   copyToClipboard("frames");
})

copyTimeStamp.addEventListener("click", function() {
   copyToClipboard("time");
})

// Keycodes for keypress event listeners
// 16 = shift, 32 = space, 37 = l arrow, 38 = up, 39 = right, 40 = down, 191 = forward slash
var map = {
   16: false,  
   32: false,
   37: false, 
   38: false, 
   39: false,
   40: false,
   191: false
};

// Check for keypress and fire appropriate shortcut functions
$(document).keypress(function(e) {
   if (e.which == 32) {
      toggleVideoPlayback();
   }
});

// Listener for multiple key presses
$(document).keydown(function(e) {
   if (e.keyCode in map) {
      map[e.keyCode] = true;
      var backOption = stepBackwardBox.selectedIndex;
      var forwardOption = stepForwardBox.selectedIndex;
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
}).keyup(function(e) {
   if (e.keyCode in map) {
      map[e.keyCode] = false;
   }
});
