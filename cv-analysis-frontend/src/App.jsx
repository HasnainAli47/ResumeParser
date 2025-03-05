import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import ResumeUpload from "./pages/ResumeUpload";
import ResumeSearch from "./pages/ResumeSearch";
import Chatbot from "./pages/Chatbot";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import Footer from "./components/Footer";

function App() {
  return (
    <Router>
      <Navbar />
        <Routes>
          <Route path="/" element={<ResumeUpload />} />
          <Route path="/search" element={<ResumeSearch />} />
          <Route path="/chatbot" element={<Chatbot />} />
        </Routes>
      <Footer />
      <ToastContainer position="top-right" autoClose={3000} />
    </Router>
  );
}

export default App;
