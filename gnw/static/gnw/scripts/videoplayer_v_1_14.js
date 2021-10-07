const myvideo = document.getElementById('myvideo');
const videoControls = document.getElementById('video-controls');

const videoWorks = !!document.createElement('video').canPlayType;
if (videoWorks) {
  myvideo.controls = false;
  videoControls.classList.remove('hidden');
}

const playButton = document.getElementById('play');

function togglePlay() {
    if (myvideo.paused || myvideo.ended) {
      myvideo.play();
    } else {
      myvideo.pause();
    }
}

playButton.addEventListener('click', togglePlay);

const playbackIcons = document.querySelectorAll('.playback-icons use');

function updatePlayButton() {
    playbackIcons.forEach(icon => icon.classList.toggle('hidden'));

    if (myvideo.paused) {
        playButton.setAttribute('data-title', 'Play')
      } else {
        playButton.setAttribute('data-title', 'Pause')
    }
}

myvideo.addEventListener('play', updatePlayButton);
myvideo.addEventListener('pause', updatePlayButton);

const timeElapsed = document.getElementById('time-elapsed');
const duration = document.getElementById('duration');

// formatTime takes a time length in seconds and returns the time in
// minutes and seconds
function formatTime(timeInSeconds) {
    const result = new Date(timeInSeconds * 1000).toISOString().substr(11, 8);
  
    return {
      minutes: result.substr(3, 2),
      seconds: result.substr(6, 2),
    };
};

// initializeVideo sets the video duration, and maximum value of the
// progressBar
const progressBar = document.getElementById('progress-bar');
const seek = document.getElementById('seek');

function initializeVideo() {
    const videoDuration = Math.floor(myvideo.duration);
    seek.setAttribute('max', videoDuration);
    progressBar.setAttribute('max', videoDuration);
    const time = formatTime(videoDuration);
    duration.innerText = `${time.minutes}:${time.seconds}`;
    duration.setAttribute('datetime', `${time.minutes}m ${time.seconds}s`)
}

myvideo.addEventListener('loadedmetadata', initializeVideo); 

// updateTimeElapsed indicates how far through the video
// the current playback is
function updateTimeElapsed() {
    const time = formatTime(Math.floor(myvideo.currentTime));
    timeElapsed.innerText = `${time.minutes}:${time.seconds}`;
    timeElapsed.setAttribute('datetime', `${time.minutes}m ${time.seconds}s`)
}

myvideo.addEventListener('timeupdate', updateTimeElapsed);

// updateProgress indicates how far through the video
// the current playback is by updating the progress bar
function updateProgress() {
    progressBar.value = Math.floor(myvideo.currentTime);
    seek.value = Math.floor(myvideo.currentTime);
}

myvideo.addEventListener('timeupdate', updateProgress);

seek.addEventListener("mousedown", mousedownDetected);
function mousedownDetected()
{
    if (!(myvideo.paused || myvideo.ended))
    {
      myvideo.pause();
      skipAhead.wasPlaying = true;
    }
}

const seekTooltip = document.getElementById('seek-tooltip');

// updateSeekTooltip uses the position of the mouse on the progress bar to
// roughly work out what point in the video the user will skip to if
// the progress bar is clicked at that point
function updateSeekTooltip(event) {
    const skipTo = Math.round((event.offsetX / event.target.clientWidth) * parseInt(event.target.getAttribute('max'), 10));
    seek.setAttribute('data-seek', skipTo)
    const t = formatTime(skipTo);
    seekTooltip.textContent = `${t.minutes}:${t.seconds}`;
    const rect = myvideo.getBoundingClientRect();
    seekTooltip.style.left = `${event.pageX - rect.left}px`;
}

seek.addEventListener('mousemove', updateSeekTooltip);

// skipAhead jumps to a different point in the video when
// the progress bar is clicked
function skipAhead(event) {
      const skipTo = event.target.dataset.seek ? event.target.dataset.seek : event.target.value;
      myvideo.currentTime = skipTo;
      progressBar.value = skipTo;
      seek.value = skipTo;
      if (skipAhead.wasPlaying)
      {
          skipAhead.wasPlaying = false;
          myvideo.play();
      }
}

seek.addEventListener('change', skipAhead);

const volumeButton = document.getElementById('volume-button');
const volumeIcons = document.querySelectorAll('.volume-button use');
const volumeMute = document.querySelector('use[href="#volume-mute"]');
const volumeLow = document.querySelector('use[href="#volume-low"]');
const volumeHigh = document.querySelector('use[href="#volume-high"]');
const volume = document.getElementById('volume');

// updateVolume updates the video's volume
// and disables the muted state if active
function updateVolume() {
    if (myvideo.muted) {
      myvideo.muted = false;
    }
  
    myvideo.volume = volume.value;
}

volume.addEventListener('input', updateVolume);

// updateVolumeIcon updates the volume icon so that it correctly reflects
// the volume of the video
function updateVolumeIcon() {
    volumeIcons.forEach(icon => {
      icon.classList.add('hidden');
    });
  
    volumeButton.setAttribute('data-title', 'Mute')
  
    if (myvideo.muted || myvideo.volume === 0) {
      volumeMute.classList.remove('hidden');
      volumeButton.setAttribute('data-title', 'Unmute')
    } else if (myvideo.volume > 0 && myvideo.volume <= 0.5) {
      volumeLow.classList.remove('hidden');
    } else {
      volumeHigh.classList.remove('hidden');
    }
}
  
myvideo.addEventListener('volumechange', updateVolumeIcon);

// toggleMute mutes or unmutes the video when executed
// When the video is unmuted, the volume is returned to the value
// it was set to before the video was muted
function toggleMute() {
    myvideo.muted = !myvideo.muted;
  
    if (myvideo.muted) {
      volume.setAttribute('data-volume', volume.value);
      volume.value = 0;
    } else {
      volume.value = volume.dataset.volume;
    }
}

volumeButton.addEventListener('click', toggleMute);

myvideo.addEventListener('click', togglePlay);

const playbackAnimation = document.getElementById('playback-animation');

// animatePlayback displays an animation when
// the video is played or paused
function animatePlayback() {
    playbackAnimation.animate([
      {
        opacity: 1,
        transform: "scale(1)",
      },
      {
        opacity: 0,
        transform: "scale(1.3)",
      }], {
      duration: 500,
    });
}

myvideo.addEventListener('click', animatePlayback);

const fullscreenButton = document.getElementById('fullscreen-button');
const videoContainer = document.getElementById('videoBox');

// toggleFullScreen toggles the full screen state of the video
// If the browser is currently in fullscreen mode,
// then it should exit and vice versa.
function toggleFullScreen() 
{
    if (document.fullscreenElement) 
    {
      document.exitFullscreen();
    } 
    else if (document.webkitFullscreenElement) 
    {
      // Need this to support Safari
      document.webkitExitFullscreen();
    } 
    else if (videoContainer.requestFullscreen)
    {
       videoContainer.requestFullscreen();
    }
    else if (videoContainer.webkitRequestFullscreen) 
    {
      // Need this to support Safari
       videoContainer.webkitRequestFullscreen();
    } 
    else 
    {
       videoContainer.requestFullscreen();
    }
}

fullscreenButton.addEventListener('click', toggleFullScreen);

const fullscreenIcons = fullscreenButton.querySelectorAll('use');

// updateFullscreenButton changes the icon of the full screen button
// and tooltip to reflect the current full screen state of the video
function updateFullscreenButton() 
{
    fullscreenIcons.forEach(icon => icon.classList.toggle('hidden'));
  
    if (document.fullscreenElement || document.mozFullScreenElement || document.webkitCurrentFullScreenElement) 
    {
      fullscreenButton.setAttribute('data-title', 'Exit full screen');
    } 
    else 
    {
      fullscreenButton.setAttribute('data-title', 'Full screen');
    }
}

videoContainer.addEventListener('fullscreenchange', updateFullscreenButton);


//When the video ends, if it's in fullscreen mode, it should exit
//fullscreen mode.
function exit_fullscreen()
{
    if (document.fullscreenElement) 
    {
    document.exitFullscreen();
    } 
    else if (document.webkitFullscreenElement) 
    {
    // Need this to support Safari
    document.webkitExitFullscreen();
    } 
}

myvideo.addEventListener("ended", exit_fullscreen);

// hideControls hides the video controls when not in use
// if the video is paused, the controls must remain visible
function hideControls() 
{
    if (myvideo.paused) 
    {
      return;
    }
  
    videoControls.classList.add('hide');
}
  
// showControls displays the video controls
let timeoutID;
function showControls() 
{
    videoControls.classList.remove('hide');
    clearTimeout(timeoutID);
    timeoutID = setTimeout(hideControls, 3000);
}

videoContainer.addEventListener('mousemove', showControls);
videoContainer.addEventListener('mouseleave', hideControls);

myvideo.addEventListener("ended", showControls);
  
  

  

  
  
  
  



  
  




  
  
  
  

  
