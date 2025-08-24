let balance = 0;
let lastWithdraw = null;

// Show ad when clicking "Watch Ad"
document.getElementById("watchAdBtn").addEventListener("click", () => {
    let adContainer = document.getElementById("adContainer");
    adContainer.style.display = "block";

    // Simulate waiting 10 seconds for user to see ad
    setTimeout(() => {
        balance += 0.5;
        document.getElementById("balance").innerText = balance.toFixed(1);
        alert("✅ You earned 0.5 credits!");
        
        // Hide ad container again so it's clean
        adContainer.style.display = "none";
    }, 10000); // 10 sec "watch time"
});

// Withdraw system with 3-day lock
document.getElementById("withdrawBtn").addEventListener("click", () => {
    let now = new Date();

    if (lastWithdraw && (now - lastWithdraw) < (3 * 24 * 60 * 60 * 1000)) {
        document.getElementById("status").innerText = "❌ You can only withdraw once every 3 days!";
        return;
    }

    if (balance >= 5) { // Example threshold
        document.getElementById("status").innerText = "✅ Withdrawal request sent!";
        balance = 0;
        document.getElementById("balance").innerText = balance.toFixed(1);
        lastWithdraw = now;
    } else {
        document.getElementById("status").innerText = "❌ Minimum 5 credits required to withdraw.";
    }
});
