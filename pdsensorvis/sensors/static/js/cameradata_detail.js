"use strict";

// Video Elements
let currentFrame = document.getElementById('id-frame');
let currentTime = document.getElementById('form-timestamp');
let videoTime = document.getElementById("video-time");
let videoDuration = document.getElementById("video-duration");
let framerateSelect = document.getElementById("framerate-list");

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
let currentFramerate = 24; // reassigned on page load of metadata
let currentVolume;

let video = VideoFrame({
   id: 'video',
   frameRate: currentFramerate,
   callback: function (frame) {
      updateSeekBar();
   }
});

function togglePlayButton(text) {
   if (text === "play") {
      playButton.innerHTML = "<i class=\"material-icons\">play_arrow</i>";
   } else if (text === "pause") {
      playButton.innerHTML = "<i class=\"material-icons\">pause</i>";
   }
}

function toggleVolumeButton(text) {
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
}

function updateSeekBar() {
   seekBar.value = video.video.currentTime * currentFramerate;
   currentFrame.value = video.get();
   currentTime.value = video.toSMPTE();
   refreshVideoTimes();
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
      togglePlayButton("pause");
   } else {
      pauseVideo();
      togglePlayButton("play");
   }
}

function endVideo() {
   pauseVideo();
   togglePlayButton("play");
   updateSeekBar();
}

function rewindFromInput() {
   let desiredFrame = parseInt(rewindTextBox.value);
   let convertedSMPTE = video.toSMPTE(desiredFrame);
   if (desiredFrame === 0) convertedSMPTE = '00:00:00:00';
   rewindVideo(convertedSMPTE);
}

function rewindVideo(SMPTE) {
   // Fix a bug in the toMilliseconds library conversion as off by one frame
   video.video.currentTime = video.toMilliseconds(SMPTE)/1000 + currentFramerate/1000;
}

function stepBack() {
   let backwardStep = stepBackwardBox.options[stepBackwardBox.selectedIndex].text;
   video.seekBackward(backwardStep, updateSeekBar());
   togglePlayButton("play");
}

function stepForward() {
   let forwardStep = stepForwardBox.options[stepForwardBox.selectedIndex].text;
   video.seekForward(forwardStep, updateSeekBar());
   togglePlayButton("play");
}

/*
function copyToClipboard(selection) {
   selection.select();
   document.execCommand("Copy");
}
*/

function displayHelpAlert() {
   const newLine = "\r\n";
   let helpMessage = "Shortcuts:";
   helpMessage += newLine;
   helpMessage += newLine;
   helpMessage += "Space bar : Play/pause video.";
   helpMessage += newLine;
   helpMessage += "Shift + Right Arrow : Step frames forward by selected amount.";
   helpMessage += newLine;
   helpMessage += "Shift + Left Arrow : Step frames backward by selected amount.";
   helpMessage += newLine;
   helpMessage += "Shift + Up Arrow : Increase frame step amount.";
   helpMessage += newLine;
   helpMessage += "Shift + Down Arrow : Decrease frame step amount.";
   helpMessage += newLine;
   helpMessage += "Shift + / : Reset video to specified frame.";
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

framerateSelect.addEventListener("change", function() {
   currentFramerate = parseFloat(framerateSelect.options[framerateSelect.selectedIndex].text);
   video.frameRate = currentFramerate;
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
   playButton.blur();
});

helpButton.addEventListener("click", function () {
   displayHelpAlert();
   helpButton.blur();
});

video.video.addEventListener("click", function () {
   toggleVideoPlayback();
});

muteButton.addEventListener("click", function () {
   if (video.video.muted === false) {
      video.video.muted = true;
      toggleVolumeButton("mute");
   } else {
      video.video.muted = false;
      toggleVolumeButton("unmute");
   }
   muteButton.blur();
});

rewindButton.addEventListener("click", function () {
   rewindFromInput();
   rewindButton.blur();
});

seekBackwardButton.addEventListener("click", function () {
   stepBack();
   seekBackwardButton.blur();
});

seekForwardButton.addEventListener("click", function () {
   stepForward();
   seekForwardButton.blur();
});

/*
copyFrameNumber.addEventListener("click", function () {
   pauseVideo();
   copyToClipboard(currentFrame);
   copyFrameNumber.blur();
});

copyTimeStamp.addEventListener("click", function () {
   pauseVideo();
   copyToClipboard(currentTime);
   copyTimeStamp.blur();
});
 */

// Keycodes for keypress event listeners
// 16 = shift, 32 = space, 37 = l arrow, 38 = up, 39 = right,
// 40 = down, 191 = forward slash
let keyCodeMap = {
   16: false,
   32: false,
   37: false,
   38: false,
   39: false,
   40: false,
   191: false
};
let keyIsDown = false;

// Check for keypress and fire appropriate shortcut functions
$(document).keydown(function (e) {
   if (!$("#rewind-value").is(':focus') && !$("#other-annotation").is(':focus')) {
      if (e.keyCode in keyCodeMap) {
         keyCodeMap[e.keyCode] = true;
         let backOption = stepBackwardBox.selectedIndex;
         let forwardOption = stepForwardBox.selectedIndex;
         if (keyCodeMap[16] && keyCodeMap[191]) {
            rewindFromInput();
         } else if (keyCodeMap[16] && keyCodeMap[37]) {
            stepBack();
         } else if (keyCodeMap[16] && keyCodeMap[39]) {
            stepForward();
         } else if (keyCodeMap[16] && keyCodeMap[38]) {
            stepBackwardBox.options[parseInt(backOption) + 1].selected = true;
            stepForwardBox.options[parseInt(forwardOption) + 1].selected = true;
         } else if (keyCodeMap[16] && keyCodeMap[40]) {
            stepBackwardBox.options[parseInt(backOption) - 1].selected = true;
            stepForwardBox.options[parseInt(forwardOption) - 1].selected = true;
         }
      }
      // Video play toggle should not repeat on key hold
      if (keyIsDown) return;
      keyIsDown = true;
      if (e.which === 32) {
         toggleVideoPlayback();
      }
   }
}).keyup(function (e) {
   keyIsDown = false;
   if (e.keyCode in keyCodeMap) {
      keyCodeMap[e.keyCode] = false;
   }
});

// Handle Camera Annotation buttons
$('button', $('#annotation-objects-list')).each(function () {
   $(this).click(function() {
      if ($(this).attr('id').indexOf('rewind') > -1) {
         rewindVideo(this.name);
      } else if ($(this).attr('id').indexOf('edit') > -1) {
         document.location.href = this.name;
      }
      this.blur();
   })
});
