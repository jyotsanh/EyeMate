import React from 'react';
import './Log.css'

function Log() {
  return (
    <div>
      <form className="form">
        <div className="flex-column">
          <label>Email</label>
        </div>
        <div className="inputForm">
          <svg
            height="20"
            viewBox="0 0 32 32"
            width="20"
            xmlns="http://www.w3.org/2000/svg"
          >
            <g id="Layer_3" data-name="Layer 3">
              <path d="..." />
            </g>
          </svg>
          <input type="text" className="input" placeholder="Enter your Email" />
        </div>

        <div className="flex-column">
          <label>Password</label>
        </div>
        <div className="inputForm">
          <svg
            height="20"
            viewBox="-64 0 512 512"
            width="20"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path d="..." />
          </svg>
          <input type="password" className="input" placeholder="Enter your Password" />
          <svg viewBox="0 0 576 512" height="1em" xmlns="http://www.w3.org/2000/svg">
            <path d="..." />
          </svg>
        </div>

        <div className="flex-row">
          <div>
            <input type="checkbox" />
            <label>Remember me</label>
          </div>
          <span className="span">Forgot password?</span>
        </div>
        <button className="button-submit">Sign In</button>
        <p className="p">
          Don't have an account? <span className="span">Sign Up</span>
        </p>
        <p className="p line">Or With</p>
        <div className="flex-row">
          <button className="btn google">
            <svg
              version="1.1"
              width="20"
              id="Layer_1"
              xmlns="http://www.w3.org/2000/svg"
              xmlnsXlink="http://www.w3.org/1999/xlink"
              x="0px"
              y="0px"
              viewBox="0 0 512 512"
              style={{ enableBackground: 'new 0 0 512 512' }}
              xmlSpace="preserve"
            >
              <path d="..." />
            </svg>
            Google
          </button>
          <button className="btn apple">
            <svg
              version="1.1"
              height="20"
              width="20"
              id="Capa_1"
              xmlns="http://www.w3.org/2000/svg"
              xmlnsXlink="http://www.w3.org/1999/xlink"
              x="0px"
              y="0px"
              viewBox="0 0 22.773 22.773"
              style={{ enableBackground: 'new 0 0 22.773 22.773' }}
              xmlSpace="preserve"
            >
              <g>
                <g>
                  <path d="..." />
                  <path d="..." />
                </g>
              </g>
            </svg>
            Apple
          </button>
        </div>
      </form>
    </div>
  );
}

export default Log;
