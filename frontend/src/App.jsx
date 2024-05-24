import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from './pages/home/Home';
import Navbar from './Components/Navbar';
import Footer from './Components/Footer';
import Sunglasses from "./pages/Sunglasses/Sunglasses";
import EyeGlasses from "./pages/Eyeglasses/EyeGlasses";
import Contactlens from "./pages/contactlens/Contactlens";
import Book from "./pages/book/Book";
import FAQ from "./pages/Faq/FAQ";
import Login from './pages/Login/Log';

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/sunglasses" element={<Sunglasses />} />
        <Route path="/eyeglasses" element={<EyeGlasses />} />
        <Route path="/contactlens" element={<Contactlens />} />
        <Route path="/book" element={<Book />} />
        <Route path="/faq" element={<FAQ />} />
        <Route path="/login" component={Login} />
      </Routes>
      <Footer />
    </BrowserRouter>
  );
}

export default App;
