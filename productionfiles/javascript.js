const header = document.querySelector("header");
      const hamburgerBtn = document.querySelector("#hamburger-btn");
      const closeMenuBtn = document.querySelector("#close-menu-btn");

      // Toggle mobile menu on hamburger button click
      hamburgerBtn.addEventListener("click", () => header.classList.toggle("show-mobile-menu"));

      // Close mobile menu on close button click
      closeMenuBtn.addEventListener("click", () => hamburgerBtn.click());

function updateVehicleSelection(checkbox) {
        var selectedVehicle = document.getElementById('selectedVehicle');
        if (checkbox.checked) {
            var busName = document.getElementById('busName_' + checkbox.id).innerText;
            selectedVehicle.innerText = busName;  // Display the bus name
        } else {
            selectedVehicle.innerText = '';
        }
    }