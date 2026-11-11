import React, { useState } from 'react';
import './Register.css';

export default function Register() {
  const [form, setForm] = useState({userName: '', firstName: '', lastName: '', email: '', password: ''});
  const [error, setError] = useState('');
  const update = (event) => setForm({...form, [event.target.name]: event.target.value});
  const register = async (event) => {
    event.preventDefault();
    setError('');
    try {
      const response = await fetch('/djangoapp/register', {
        method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(form),
      });
      const result = await response.json();
      if (response.ok && result.status === 'Authenticated') {
        sessionStorage.setItem('username', result.userName);
        window.location.href = '/';
      } else {
        setError(result.error === 'Already Registered' ? 'This username is already registered.' : 'Unable to register.');
      }
    } catch (err) {
      setError('Unable to contact the server.');
    }
  };
  return (
    <div className="register_container">
      <h1>Sign Up</h1>
      <form onSubmit={register}>
        {[
          ['userName', 'Username', 'text'], ['firstName', 'First name', 'text'],
          ['lastName', 'Last name', 'text'], ['email', 'Email', 'email'],
          ['password', 'Password', 'password'],
        ].map(([name, label, type]) => (
          <label key={name}>{label}<input className="input_field" name={name} type={type} value={form[name]} onChange={update} required /></label>
        ))}
        {error && <p role="alert">{error}</p>}
        <div className="submit_panel"><button className="submit" type="submit">Register</button></div>
      </form>
      <a href="/">Cancel</a>
    </div>
  );
}
