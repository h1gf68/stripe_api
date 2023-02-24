fetch("/config/")
.then((result) => { return result.json(); })
.then((data) => {
  const stripe = Stripe(data.publicKey);
  let submitBtn = document.querySelector("#submitBtn");
  if (submitBtn !== null) {
    submitBtn.addEventListener("click", () => {
    checkout_path = "/create-checkout-session/"+document.location.pathname.split("/")[2]+"/"
    fetch(checkout_path)
      .then((result) => { return result.json(); })
      .then((data) => {
        console.log(data);
        return stripe.redirectToCheckout({sessionId: data.sessionId})
      })
      .then((res) => {
        console.log(res);
      });
    });
  }
});