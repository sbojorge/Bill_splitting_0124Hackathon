function showAlert(message) {
    var alert = document.createElement('div');
    alert.className = 'alert alert-danger alert-dismissible fade show text-center';
    alert.role = 'alert';
    alert.innerHTML = message + '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>';
    alertPlaceholder.appendChild(alert);
  }

  document.addEventListener('DOMContentLoaded', function () {
    var eventNameInput = document.getElementById('eventName');
    var userNames = Array.from(document.getElementById('userList').children).map((div) => div.textContent.trim());
    var inputFields = document.querySelectorAll('.form-group .member');
    clearInputFields();
    var addButtons = document.querySelectorAll('.btn-secondary event-add-btn'); // Select all buttons with class 'btn-secondary event-add-btn'
    var alertPlaceholder = document.getElementById('alertPlaceholder');

    function clearInputFields() {
      for (inputField of inputFields) {
          eventNameInput.value = '';
          inputField.value='';
      }
    }
    function inputCheck(index) {
      var inputValue = inputFields[index].value.trim().toLowerCase();
      var closestMatch = userNames.find((name) => name.toLowerCase().includes(inputValue));
      if (closestMatch) {
        inputFields[index].value = closestMatch;
      } else {
        showAlert(inputValue + " wasn't found in the database");
        inputFields[index].value = '';
      }
    }

    inputFields.forEach((inputField, index) => {
      inputField.addEventListener('keydown', function (event) {
        if (event.key === 'Enter') {
          event.preventDefault(); // Prevent form submission on Enter key
          inputCheck(index);
        }
      });
    });

    addButtons.forEach((button, index) => {
      button.addEventListener('click', function () {
        inputCheck(index);
      });
    });

    document.getElementById('createEventButton').addEventListener('click', function (event) {
      if (eventNameInput.value.trim() === '') {
        showAlert('Please enter an event name.');
        event.preventDefault(); // Prevent the form from being submitted
        console.log('Event not created!');
      } else {
        console.log('Event Created');
      }
    });
  });