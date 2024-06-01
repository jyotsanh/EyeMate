import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import './Navbar.css';
import logo from '../assets/logo.png';
 // Assuming the login component is in 'Login/Log.jsx'

function Navbar() {
  const [showLoginForm, setShowLoginForm] = useState(false);

  const toggleLoginForm = () => {
    setShowLoginForm(!showLoginForm);
  };

  return (
    <div>
      <nav>
        <div className="logo">
          <img src={logo} alt="Logo" />
        </div>

        <div className="search-bar">
          <i className="fas fa-search"></i>
          <input type="text" placeholder="What are you searching for?" />
        </div>

        <div className="actions">
          <i className="far fa-heart"></i>
      
          {/* <NavLink to="/Log" activeClassName="active"> <i className="far fa-user" > </i></NavLink>     */}
          <NavLink to="#" onClick={toggleLoginForm}>
  <i className="far fa-user"></i>
</NavLink>

          <i className="fas fa-shopping-cart"></i>
        </div>
      </nav>

      <ul className="menu">
        <li><NavLink exact to="/" activeClassName="active">Home</NavLink></li>
        <li><NavLink to="/sunglasses" activeClassName="active">Sunglasses</NavLink></li>
        <li><NavLink to="/eyeglasses" activeClassName="active">Eyeglasses</NavLink></li>
        <li><NavLink to="/contactlens" activeClassName="active">Lens</NavLink></li>
        <li><NavLink to="/book" activeClassName="active">Book Appointment</NavLink></li>
        <li><NavLink to="/faq" activeClassName="active">FAQs</NavLink></li>
      </ul>

      {showLoginForm && (
        <div className="modal">
          <div className="modal-content">
            <Login />
          </div>
        </div>
      )}
    </div>
  );
}

export default Navbar;
