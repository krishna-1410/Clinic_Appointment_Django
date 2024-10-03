document.addEventListener('DOMContentLoaded', function () {
    const servicesContainer = document.getElementById('services-container');
    const addServiceBtn = document.getElementById('add-service-btn');
    let serviceCount = 1; // Starts from 1 because the first set of fields already exists (id=0)

    // Function to create a new service input group
    function addServiceFields() {
        // Create a new div for the form-row
        const serviceRow = document.createElement('div');
        serviceRow.classList.add('form-row');

        // Service Name field
        const serviceNameDiv = document.createElement('div');
        serviceNameDiv.classList.add('form-group', 'col-md-6');
        const serviceNameLabel = document.createElement('label');
        serviceNameLabel.setAttribute('for', `service-name-${serviceCount}`);
        serviceNameLabel.innerText = 'Service Name';
        const serviceNameInput = document.createElement('input');
        serviceNameInput.setAttribute('type', 'text');
        serviceNameInput.setAttribute('id', `service-name-${serviceCount}`);
        serviceNameInput.setAttribute('name', 'service-name[]');
        serviceNameInput.setAttribute('placeholder', 'Service Name');
        serviceNameInput.classList.add('form-control');
        serviceNameDiv.appendChild(serviceNameLabel);
        serviceNameDiv.appendChild(serviceNameInput);

        // Treatment Cost field
        const treatmentCostDiv = document.createElement('div');
        treatmentCostDiv.classList.add('form-group', 'col-md-6');
        const treatmentCostLabel = document.createElement('label');
        treatmentCostLabel.setAttribute('for', `treatment-cost-${serviceCount}`);
        treatmentCostLabel.innerText = 'Cost of Treatment';
        const treatmentCostInput = document.createElement('input');
        treatmentCostInput.setAttribute('type', 'text');
        treatmentCostInput.setAttribute('id', `treatment-cost-${serviceCount}`);
        treatmentCostInput.setAttribute('name', 'treatment-cost[]');
        treatmentCostInput.setAttribute('placeholder', 'Cost of Treatment');
        treatmentCostInput.classList.add('form-control');
        treatmentCostDiv.appendChild(treatmentCostLabel);
        treatmentCostDiv.appendChild(treatmentCostInput);

        // Append both fields to the new row
        serviceRow.appendChild(serviceNameDiv);
        serviceRow.appendChild(treatmentCostDiv);

        // Append the new row to the services container
        servicesContainer.appendChild(serviceRow);

        // Increment the service count for unique IDs
        serviceCount++;
    }

    // Event listener to add new service fields when the button is clicked
    addServiceBtn.addEventListener('click', function (e) {
        e.preventDefault(); // Prevent form submission or page refresh
        addServiceFields();
    });
});
