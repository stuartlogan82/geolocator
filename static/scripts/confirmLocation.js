function handleConfirm(e) {
  //e.preventDefault();
  const token = fetchAccessToken(initializeSync)

  fetch('/dequeue', {
    method: "POST", // *GET, POST, PUT, DELETE, etc.
    mode: "cors", // no-cors, cors, *same-origin
    cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
    credentials: "same-origin", // include, *same-origin, omit
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      // "Content-Type": "application/x-www-form-urlencoded",
    },
    redirect: "follow", // manual, *follow, error
    referrer: "no-referrer", // no-referrer, *client
    body: JSON.stringify({
      identity: "{{identity}}"
    }), // body data type must match "Content-Type" header
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

//fetchAccessToken(initializeSync)

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