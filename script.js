let username = "";
let balance = 0;
let adsWatched = 0;

document.getElementById("usernameForm").addEventListener("submit", function(e) {
  e.preventDefault();
  username = document.getElementById("username").value;
  document.getElementById("userDisplay").textContent = username;
  document.getElementById("usernameForm").style.display = "none";
  document.getElementById("dashboard").style.display = "block";
});

document.getElementById("watchAd").addEventListener("click", function() {
  // User must actually load the ad (we just simulate with button click)
  balance += 0.5;
  adsWatched++;
  document.getElementById("balance").textContent = balance.toFixed(2);
  document.getElementById("adsWatched").textContent = adsWatched;

  // Save to backend
  fetch("/save", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({username, balance, adsWatched})
  });
});

document.getElementById("withdraw").addEventListener("click", function() {
  fetch("/withdraw", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({username})
  })
  .then(res => res.json())
  .then(data => {
    document.getElementById("message").textContent = data.message;
  });
});
