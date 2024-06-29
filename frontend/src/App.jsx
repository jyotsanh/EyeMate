import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { CartProvider } from './context/CartContext';
import Home from './pages/home/Home';
import Navbar from './Components/Navbar';
import Footer from './Components/Footer';
import Sunglasses from './pages/Sunglasses/Sunglasses';
import EyeGlasses from './pages/Eyeglasses/EyeGlasses';
import Contactlens from './pages/contactlens/Contactlens';
import Book from './pages/book/Book';
import FAQ from './pages/Faq/FAQ';
import Log from './pages/Login/Log';
import Sign from './pages/Sign/Sign';
import Cart from './pages/cart/cart';
import ProductPage from './Components/ProductPage';

function App() {
  return (
    <CartProvider>
      <BrowserRouter>
        <Navbar />
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/sunglasses" element={<Sunglasses />} />
            <Route path="/eyeglasses" element={<EyeGlasses />} />
            <Route path="/contactlens" element={<Contactlens />} />
            <Route path="/book" element={<Book />} />
            <Route path="/faq" element={<FAQ />} />
            <Route path="/login" element={<Log />} />
            <Route path="/sign" element={<Sign />} />
            <Route path="/cart" element={<Cart />} />
            <Route path="/productpage" element={<ProductPage />} />
          </Routes>
       
        <Footer />
      </BrowserRouter>
    </CartProvider>
  );
}

export default App;
