function handleConfirm(e) {
  const token = fetchAccessToken(initializeSync)
  fetch('/dequeue', {
    method: "POST",
    mode: "cors",
    cache: "no-cache",
    credentials: "same-origin",
    headers: {
      "Content-Type": "application/json; charset=utf-8",
    },
    redirect: "follow",
    referrer: "no-referrer",
    body: JSON.stringify({
      identity: "{{ identity }}"
    }),
  })
    .then(response => response.json())
    .then(responseJson => {
      console.log(responseJson);
      document.getElementById('confirm').innerHTML =
        '<p class="lead">We have your location and are putting you through to an agent, please return to the call on your phone!</p>';
    });
}

function fetchAccessToken(handler) {
  $.getJSON('/token?identity={{identity}}', function (tokenResponse) {
    console.log(tokenResponse.token)
    console.log(tokenResponse.identity)
    handler(tokenResponse);
  });
}

function initializeSync(tokenResponse) {
  var syncClient = new Twilio.Sync.Client(tokenResponse.token);
  navigator.geolocation.getCurrentPosition(function (position) {
    var pos = {
      lat: position.coords.latitude,
      lng: position.coords.longitude
    };
    console.log(pos);
    syncClient.document('{{identity}}').then(function (doc) {
      doc.set(pos);
    });
    syncClient.document('{{identity}}').then(function (doc) {
      doc.on('updated', function (data) {
        console.log('Document updated!', data);
      });
    });
  });

}