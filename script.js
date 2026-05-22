  function toggleDropdown(event) {
    event.preventDefault();
    document.getElementById("myDropdown").classList.toggle("show");
  }

  window.onclick = function (event) {
    if (!event.target.matches(".dropbtn")) {
      let dropdowns = document.getElementsByClassName("dropdown-content");
      for (let i = 0; i < dropdowns.length; i++) {
        dropdowns[i].classList.remove("show");
      }
    }
  };