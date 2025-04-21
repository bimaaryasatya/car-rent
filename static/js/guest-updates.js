async function fetchCarStatus() {
  try {
    const response = await fetch('/mobil');
    if (!response.ok) {
      console.error('Failed to fetch car data');
      return;
    }
    const cars = await response.json();
    cars.forEach(car => {
      const carCard = document.querySelector(`.car-card[data-plat="${car.plat}"]`);
      if (carCard) {
        const statusTextElem = carCard.querySelector('.status-text span');
        const orderBtn = carCard.querySelector('.order-btn');
        if (car.status === 'tersedia') {
          statusTextElem.textContent = 'Tersedia';
          statusTextElem.className = 'text-success';
          if (orderBtn.tagName === 'A') {
            orderBtn.className = 'btn btn-success order-btn';
            orderBtn.href = `https://wa.me/6281234567890?text=Halo%20saya%20ingin%20sewa%20mobil%20${car.plat}`;
            orderBtn.removeAttribute('disabled');
            orderBtn.onclick = null;
          } else {
            // Replace button with link
            const link = document.createElement('a');
            link.className = 'btn btn-success order-btn';
            link.href = `https://wa.me/6281234567890?text=Halo%20saya%20ingin%20sewa%20mobil%20${car.plat}`;
            link.target = '_blank';
            link.textContent = 'Pesan Sekarang';
            orderBtn.parentNode.replaceChild(link, orderBtn);
          }
        } else {
          statusTextElem.textContent = 'Disewa';
          statusTextElem.className = 'text-danger';
          if (orderBtn.tagName === 'BUTTON') {
            orderBtn.className = 'btn btn-secondary order-btn';
            orderBtn.disabled = true;
            orderBtn.onclick = () => alert('Mobil sedang disewa');
          } else {
            // Replace link with button
            const button = document.createElement('button');
            button.className = 'btn btn-secondary order-btn';
            button.disabled = true;
            button.textContent = 'Tidak Tersedia';
            button.onclick = () => alert('Mobil sedang disewa');
            orderBtn.parentNode.replaceChild(button, orderBtn);
          }
        }
      }
    });
  } catch (error) {
    console.error('Error fetching car data:', error);
  }
}

// Initial fetch
fetchCarStatus();

// Poll every 5 seconds
setInterval(fetchCarStatus, 5000);
