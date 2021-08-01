




function userIDSubmitted() {
  alert('eh');
}

const user_id_form = document.getElementById('user-id-form')

thisForm.addEventListener('submit', async function (e) {
  e.preventDefault();
  alert('hey');
  
  const formData = new FormData(thisForm).entries()
      const response = await fetch('https://reqres.in/api/users', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(Object.fromEntries(formData))
  });

  const result = await response.json();
  console.log(result)
}