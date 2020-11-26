var checking = function() {
    var status = document.getElementById('status');
    var statusText = document.getElementById("status-text");

    if ( navigator.onLine && status.classList.contains('off') ) {
      statusText.innerHTML = 'Online';
      status.classList.remove('off');
      status.classList.add('on');
      document.getElementById("myInput").disabled = false;
      document.getElementById("myInpBtn").disabled = false;
    }
    if ( ! navigator.onLine && status.classList.contains('on') ) {
      statusText.innerHTML = 'Offline';
      status.classList.remove('on');
      status.classList.add('off'); // can't use .replace() because of Chrome
      document.getElementById("myInput").disabled = true;
      document.getElementById("myInpBtn").disabled = true;
    }
  };

window.addEventListener('online', checking);
window.addEventListener('offline', checking);