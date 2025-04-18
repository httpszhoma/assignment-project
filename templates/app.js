const apiBaseUrl = 'http://localhost:8000/api/';

document.getElementById('loadSpectacles').addEventListener('click', loadSpectacles);
document.getElementById('loadTickets').addEventListener('click', loadTickets);

document.getElementById('ticketForm').addEventListener('submit', createTicket);

// Load spectacles from API
function loadSpectacles() {
  fetch(`${apiBaseUrl}spectacles-by-date/`, {
    method: 'GET',
  })
  .then(response => response.json())
  .then(data => {
    const spectacleList = document.getElementById('spectacleList');
    spectacleList.innerHTML = ''; // Clear previous data
    data.forEach(spectacle => {
      const spectacleDiv = document.createElement('div');
      spectacleDiv.innerHTML = `
        <h3>${spectacle.title}</h3>
        <p>${spectacle.description}</p>
        <p>Price: ${spectacle.price}</p>
        <p>Duration: ${spectacle.duration} minutes</p>
      `;
      spectacleList.appendChild(spectacleDiv);
    });
  })
  .catch(error => {
    console.error('Error fetching spectacles:', error);
  });
}

function loadTickets() {
  fetch(`${apiBaseUrl}tickets/`, {
    method: 'GET',
  })
  .then(response => response.json())
  .then(data => {
    const ticketList = document.getElementById('ticketList');
    ticketList.innerHTML = ''; // Clear previous data
    data.forEach(ticket => {
      const ticketDiv = document.createElement('div');
      ticketDiv.innerHTML = `
        <p>Ticket ID: ${ticket.id}</p>
        <p>Spectacle: ${ticket.spectacle.title}</p>
        <p>Seat: ${ticket.seat.row} ${ticket.seat.number}</p>
        <p>Price: ${ticket.price}</p>
      `;
      ticketList.appendChild(ticketDiv);
    });
  })
  .catch(error => {
    console.error('Error fetching tickets:', error);
  });
}

// Create a new ticket
function createTicket(event) {
  event.preventDefault();

  const spectacleId = document.getElementById('ticketSpectacle').value;
  const seatId = document.getElementById('ticketSeat').value;

  const ticketData = {
    spectacle: spectacleId,
    seat: seatId,
  };

  fetch(`${apiBaseUrl}tickets/create/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(ticketData),
  })
  .then(response => response.json())
  .then(data => {
    alert('Ticket created successfully!');
  })
  .catch(error => {
    console.error('Error creating ticket:', error);
  });
}
