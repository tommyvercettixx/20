async function register() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
        });

        if (response.ok) {
            alert('Registration successful! You can now log in.');
        } else {
            const errorData = await response.json();
            alert(`Registration failed: ${errorData.message}`);
        }
    } catch (error) {
        console.error('Error during registration:', error);
    }
}

async function authenticate() {
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;

  try {
      const response = await fetch('/login', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify({ email, password }),
      });

      if (response.ok) {
          const data = await response.json();
          localStorage.setItem('token', data.access_token);

        
          if (data.access_level === 'admin') {
              getUsers();  
          }

          alert('Authentication successful!');
      } else {
          const errorData = await response.json();
          alert(`Authentication failed: ${errorData.message}`);
      }
  } catch (error) {
      console.error('Error during authentication:', error);
  }
}

async function getUsers() {
  const token = localStorage.getItem('token');

  try {
      const response = await fetch('/protected', {
          method: 'GET',
          headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`
          },
      });

      if (response.ok) {
          const data = await response.json();
          console.log('List of users:', data.users);
      } else {
          const errorData = await response.json();
          console.error('Failed to fetch users:', errorData.message);
      }
  } catch (error) {
      console.error('Error during fetching users:', error);
  }
}