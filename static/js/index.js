function setDisplayClass() {
	const heading = document.getElementById("responsive-heading");

	if (window.matchMedia("(min-width: 1200px)").matches) {
		heading.classList.remove("display-5");
		heading.classList.add("display-1");
	} else if (window.matchMedia("(min-width: 768px)").matches) {
		heading.classList.remove("display-1");
		heading.classList.add("display-5");
	} else {
		heading.classList.remove("display-5");
		heading.classList.add("display-1");
	}
}

// Initial call to set the display class on page load
setDisplayClass();

// Event listener to update the display class when the window is resized
window.addEventListener("resize", setDisplayClass);
