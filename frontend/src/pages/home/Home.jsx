import React from 'react';
import './Home.css';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div className="home">
      {/* Image Slider Section */}
      <section className="image-slider">
        <div className="slide"><img src="Silde1.png" alt="Slide 1" /></div>
        <div className="slide"><img src="Silde2.png" alt="Slide 2" /></div>
        <div className="slide"><img src="silde3.png" alt="Slide 3" /></div>
        <div className="slide"><img src="Silde4.png" alt="Slide 4" /></div>
      </section>

      {/* Two-Image Section */}
      <section className="two-image-section">
        <h2>Elevate Your Look with Our Signature Features</h2>
        <div className="image-description">
          <div className="image-text">
            <img src="View1.png" alt="Image 1" />
            <div className="description">
              <h2>Ultra-lightweight Frames for Maximum Comfort</h2>
              {/* <p>Our frames are engineered for ultimate comfort and durability. Say goodbye to heavy glasses that slide off.</p> */}
              <Link to="/Sunglasses"><button>View More</button></Link>
            </div>
          </div>
          <div className="image-text">
            <img src="view2.png" alt="Image 2" />
            <div className="description">
              <h2>Trendy Designs with UV Protection</h2>
              <Link to="/Sunglasses"><button>View More</button></Link>
            </div>
          </div>
        </div>
      </section>

      {/* Top Trending Products Section */}
      <section className="top-trending-products">
        <h2>Top Trending Products</h2>
        <div className="products">
          <div className="product">
            <Link to="/Sunglasses">
              <img src="p1.png" alt="Product 1" />
              <p>Product 1</p>
            </Link>
            <p className="price">Rs 500</p>
          </div>
          <div className="product">
            <Link to="/Eyeglasses">
              <img src="p2.png" alt="Product 2" />
              <p className='Prod'>Product 2</p>
            </Link>
            <p className="price">Rs 500</p>
          </div>
          <div className="product">
            <Link to="/Contactlens">
              <img src="P3.png" alt="Product 3" />
              <p>Product 3</p>
            </Link>
            <p className="price">Rs 500</p>
          </div>
          <div className="product">
            <Link to="/Sunglasses">
              <img src="p4.png" alt="Product 4" />
              <p>Product 4</p>
            </Link>
            <p className="price">Rs 500</p>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
